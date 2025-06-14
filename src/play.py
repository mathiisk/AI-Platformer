# play.py
import time
import pygame
from stable_baselines3 import PPO
from platformer_env import PlatformerEnv

def main():
    obs_env = PlatformerEnv(headless=True, feature_obs=True)
    render_env = PlatformerEnv(headless=False, feature_obs=True)

    model = PPO.load("logs/ppo_platformer/ppo_platformer_final.zip")

    clock = pygame.time.Clock()

    obs = obs_env.reset()
    _ = render_env.reset()
    total_reward = 0.0
    done = False

    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, info = obs_env.step(action)
        _, _, _, _ = render_env.step(action)

        render_env.render()
        clock.tick(30)

        total_reward += reward

        if done:
            print(f"Episode return: {total_reward:.2f}")
            total_reward = 0.0
            obs = obs_env.reset()
            _ = render_env.reset()

if __name__ == "__main__":
    main()
