import os
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback

# Import your environment
from .platformer_env import PlatformerEnv


def make_env(headless=True, feature_obs=True, level_number=1, tile_size=64):
    """Factory to create a fresh PlatformerEnv instance."""
    def _init():
        env = PlatformerEnv(headless=headless, feature_obs=feature_obs,
                             level_number=level_number, tile_size=tile_size)
        return env
    return _init


def main():
    # Configuration
    num_envs = 4            # parallel environments
    total_timesteps = 200_000
    log_dir = "./logs/ppo_platformer"
    os.makedirs(log_dir, exist_ok=True)

    # Create vectorized environments
    env_fns = [make_env() for _ in range(num_envs)]
    vec_env = SubprocVecEnv(env_fns)

    # Optional: evaluation env
    eval_env = DummyVecEnv([make_env()])

    # Callbacks: save checkpoints and evaluate
    checkpoint_callback = CheckpointCallback(save_freq=50_000, save_path=log_dir,
                                             name_prefix="ppo_ckpt")
    eval_callback = EvalCallback(eval_env, best_model_save_path=log_dir,
                                 log_path=log_dir, eval_freq=20_000,
                                 deterministic=True, render=False)

    # Instantiate the agent
    model = PPO(
        policy="MultiInputPolicy",
        env=vec_env,
        verbose=1,
        tensorboard_log=log_dir,
        n_steps=128,
        batch_size=64,
        learning_rate=0.001,
        gamma=0.99,
        ent_coef=0.01,
    )

    # Train the agent
    model.learn(total_timesteps=total_timesteps,
                callback=[checkpoint_callback, eval_callback],
                tb_log_name="PPO")

    # Save final model
    model_path = os.path.join(log_dir, "ppo_platformer_final")
    model.save(model_path)
    print(f"Training complete. Model saved to {model_path}.zip")

    # Close environments
    vec_env.close()
    eval_env.close()

if __name__ == '__main__':
    main()
