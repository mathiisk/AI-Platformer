import os
import sys
import random
import numpy as np
import pygame

from .level_load import load_level
from .level_draw import Level
from .player import Player
from .tiles import Block, Goal, Spike

class GameEngine:
    def __init__(self, headless=False, level_number=1, tile_size=64):
        self.headless = headless
        pygame.init()
        if not self.headless:
            # Create actual window
            lev, w, h = load_level(level_number, tile_size)
            self.screen = pygame.display.set_mode((w // 2, h))  # match original half-width
            pygame.display.set_caption("Platformer RL")
        else:
            # Off-screen surface for frame rendering
            _, w, h = load_level(level_number, tile_size)
            self.screen = pygame.Surface((w // 2, h))

        # Core state
        self.level_number = level_number
        self.tile_size = tile_size
        self._held_dir = 0
        self._setup_level()
        self._reset_state()

    def _setup_level(self):
        """Load level layout and create Level object."""
        layout, w, h = load_level(self.level_number, self.tile_size)
        # Level constructor: (layout_array, surface)
        self.level = Level(layout, self.screen)

    def _reset_state(self):
        """Initialize/reset game state for a new episode."""
        # Player spawns at fixed position or from layout
        spawn_pos = (128, 400)
        self.player = Player(spawn_pos, self.tile_size, self.screen.get_width() * 2, self.screen.get_height())
        self.player.reset_position()

        # After spawn/reset
        goal = next(iter(self.level.goals), None)
        if goal:
            gx, gy = goal.rect.center
            px, py = self.player.rect.center
            self._last_goal_dist = ((gx - px) ** 2 + (gy - py) ** 2) ** 0.5
        else:
            self._last_goal_dist = 0.0


        self.level.wordshift_on(0)
        self.timestep = 0
        # Track last x for progress reward
        self._last_x = self.player.rect.x
        self.done = False

    def reset(self):
        """Gym-style reset: returns initial observation."""
        self._setup_level()
        self._reset_state()
        return self._get_state()

    def step(self, action):
        """Gym-style step: apply action, advance one frame."""
        # 1) Apply action
        self._apply_action(action)

        self.player.rect.x += self.player.velocity.x
        self.player.hitbox.x += self.player.velocity.x

        # 2) Update physics & collisions
        self.player.apply_gravity()
        # Horizontal collision
        self.player.collide_with_tiles_horizontal(self.level.blocks)
        # Vertical collision
        self.player.collide_with_tiles_vertical(self.level.blocks)

        # 3) Update scrolling
        self.level.wordshift_on(0)
        # Advance world shift
        self.level.blocks.update(self.level.world_shift)
        self.level.goals.update(self.level.world_shift)
        self.level.spikes.update(self.level.world_shift)

        # 4) Check terminal conditions
        info = {}
        reward = 0.0
        # Death by falling off screen
        if self.player.has_fallen_off_screen():
            self.done = True
            info['reason'] = 'death'
        # Death by spike
        elif self.player.collide_with_spike(self.level.spikes):
            self.done = True
            info['reason'] = 'death'

        if self.player.rect.right < 0 or self.player.rect.left > self.screen.get_width():
            self.done = True
            info['reason'] = 'oob'  # out-of-bounds

        # Level complete
        elif self.player.collide_with_goal(self.level.goals):
            self.done = True
            info['reason'] = 'level_complete'

        # ──────────────────────────────────────────────────────────────────
        # 1) progress toward the goal (small, every frame)
        goal = next(iter(self.level.goals), None)
        if goal:
            gx, gy = goal.rect.center
            px, py = self.player.rect.center
            new_dist = ((gx - px) ** 2 + (gy - py) ** 2) ** 0.5
            progress_reward = (self._last_goal_dist - new_dist) * 0.02  # tune
            reward += progress_reward
            self._last_goal_dist = new_dist
        # ──────────────────────────────────────────────────────────────────

        # define a helper once
        SPIKE_RANGE = 80  # px considered “near”

        # distance to nearest spike (x-direction only)
        px, py = self.player.rect.center
        min_spike_dx = min(
            (abs(spike.rect.centerx - px) for spike in self.level.spikes),
            default=np.inf
        )

        # ─── 2) jump when near a spike ───────────────────────────────────
        if min_spike_dx < SPIKE_RANGE and action[2]:  # jump bit = 1
            jump_near_spike_bonus = 2.0
            reward += jump_near_spike_bonus
        # ──────────────────────────────────────────────────────────────────

        # ─── 3) reward successful jump-over spike ────────────────────────
        over_spike = any(
            spike.rect.collidepoint(self.player.rect.centerx,
                                    self.player.rect.bottom + 1)
            for spike in self.level.spikes
        )
        in_air = not self.player.on_ground
        moving_horiz = abs(self.player.velocity.x) > 0
        if over_spike and in_air and moving_horiz:
            jump_over_spike_bonus = 5.0
            reward += jump_over_spike_bonus

        if in_air and moving_horiz:  # holding L/R while airborne
            reward += 0.02
            # ──────────────────────────────────────────────────────────────────

        # ─── 4) penalise jumps nowhere near a spike ──────────────────────
        if min_spike_dx > SPIKE_RANGE and action[2]:
            unneeded_jump_penalty = -2
            reward += unneeded_jump_penalty
        # ──────────────────────────────────────────────────────────────────

        # ─── 5) out-of-bounds penalty (already counted as death) ─────────
        if self.player.has_fallen_off_screen():
            reward -= 25.0  # extra pain on top of death penalty
        # ──────────────────────────────────────────────────────────────────

        # Terminal bonuses/penalties
        if self.done:
            if info.get('reason') == 'level_complete':
                reward += 100.0
            elif info.get('reason') == 'death':
                reward -= 100.0
            elif info.get('reason') == 'oob':
                reward -= 1000.0

        # Time penalty each step
        # reward -= 0.001

        self.timestep += 1
        obs = self._get_state()
        return obs, reward, self.done, info

    def _apply_action(self, action):
        """Map discrete action to player inputs."""
        # 0: noop, 1: left, 2: right, 3: jump

        left, right, jump = map(int, action)

        # ─── Update direction “memory” ────────────────────────
        if left and not right:
            self._held_dir = -self.player.speed
        elif right and not left:
            self._held_dir = self.player.speed
        # if both or neither: keep previous value in _held_dir

        # ─── Apply velocity.x ────────────────────────────────
        if self.player.on_ground:
            # Allow braking when on ground
            self.player.velocity.x = self._held_dir if (left or right) else 0
        else:
            # Keep the remembered direction while airborne
            self.player.velocity.x = self._held_dir

        # ─── Jump key ────────────────────────────────────────
        if jump and self.player.on_ground:
            self.player.jump()

    def _get_state(self):
        """Return either image frame or feature vector."""
        if self.headless:
            return self._get_features()
        else:
            return self._get_frame()

    def _get_features(self):
        """Low-dimensional state: [x, y, vx, vy, dist_goal_x, dist_goal_y]."""
        px, py = self.player.rect.center
        vx, vy = self.player.velocity
        # Use first goal as reference
        goal = next(iter(self.level.goals), None)
        gx, gy = (goal.rect.center if goal else (px, py))
        dx = (gx - px) / (self.screen.get_width() * 2)
        dy = (gy - py) / self.screen.get_height()
        return [px / (self.screen.get_width() * 2), py / self.screen.get_height(), vx, vy, dx, dy]

    def _get_frame(self):
        """Render to off-screen Surface and return RGB array."""
        # Draw background
        self.screen.fill((43, 28, 89))
        # Draw level elements
        self.level.run()
        # Draw player
        self.screen.blit(self.player.image, self.player.rect)
        # Convert to array
        arr = pygame.surfarray.array3d(self.screen)
        return np.transpose(arr, (1, 0, 2))

    def render(self):
        """Blit the current game state to the display if not headless."""
        if not self.headless:
            # Clear background
            self.screen.fill((43, 28, 89))
            # Draw level and player
            self.level.run()
            self.screen.blit(self.player.image, self.player.rect)
            # Flip the display
            pygame.display.flip()


    def close(self):
        """Cleanup."""
        pygame.quit()
