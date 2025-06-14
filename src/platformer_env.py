import gym
import numpy as np
from gym import spaces
from engine import GameEngine

class PlatformerEnv(gym.Env):
    """
    OpenAI Gym wrapper for the Pygame platformer GameEngine.
    Supports both pixel and feature observations.
    """
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, headless=True, feature_obs=True, level_number=1, tile_size=64):
        super(PlatformerEnv, self).__init__()
        self.headless = headless
        self.feature_obs = feature_obs
        self.engine = GameEngine(headless=headless, level_number=level_number, tile_size=tile_size)

        # Determine observation space
        if feature_obs:
            # 6-dimensional feature vector wrapped in Dict for MultiInputPolicy
            low = np.array([0.0, 0.0, -np.inf, -np.inf, -1.0, -1.0], dtype=np.float32)
            high = np.array([1.0, 1.0, np.inf, np.inf, 1.0, 1.0], dtype=np.float32)
            self.observation_space = spaces.Dict({
                "obs": spaces.Box(low, high, dtype=np.float32)
            })
        else:
            # Pixel input
            frame = self.engine._get_frame()
            shape = frame.shape
            self.observation_space = spaces.Box(0, 255, shape, dtype=np.uint8)

        # MultiBinary actions: [left, right, jump]
        self.action_space = spaces.MultiBinary(3)

    def reset(self):
        """Reset environment state and return initial observation."""
        obs = self.engine.reset()
        return {"obs": np.array(obs, dtype=np.float32)}

    def step(self, action):
        """Apply action, step the engine, and return obs, reward, done, info."""
        action = action.tolist()  # Ensure it's list of 0/1
        obs, reward, done, info = self.engine.step(action)
        obs = {"obs": np.array(obs, dtype=np.float32)}
        return obs, reward, done, info

    def render(self, mode='human'):
        """Render the game. Return RGB array if mode='rgb_array'."""
        if mode == 'rgb_array':
            frame = self.engine._get_frame()
            return frame
        elif mode == 'human':
            if hasattr(self.engine, 'screen'):
                self.engine.render()
        else:
            raise ValueError(f"Unsupported render mode: {mode}")

    def close(self):
        """Clean up resources."""
        self.engine.close()
