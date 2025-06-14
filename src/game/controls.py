import pygame
from .level_draw import Level

def Controls(event, player, states, lev, screen, lv):
    level_changed = False
    """
    This function handles some game controls such as restarting and pausing the game.
    It checks if certain keys are pressed and the current state of the game, along with
    information about the level and allows the player to perform functions using those keys.
    """

    if event.type == pygame.KEYDOWN:

        # Restart level - Press 'R'
        if event.key == pygame.K_r:
            if states["IN_GAME"]:
                lv = Level(lev, screen)
                player.is_active = True
                player.reset_position()
                player.reset_position()
                states["GAME_OVER"] = False
                states["GAME_WON"] = False
                states["PAUSED"] = False
                level_changed = True

        # Pause - Press 'ESC'
        if event.key == pygame.K_ESCAPE and states["IN_GAME"]:
                states["PAUSED"] = not states["PAUSED"]
                player.is_active = not player.is_active

    return lv, level_changed
