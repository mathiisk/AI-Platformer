from platformer_env import PlatformerEnv

env = PlatformerEnv(headless=True, feature_obs=True)
obs = env.reset()
print('Initial obs:', obs)
for _ in range(10):
    action = env.action_space.sample()
    obs, rew, done, info = env.step(action)
    print('Step:', action, 'Reward:', rew, 'Done:', done)
    if done:
        obs = env.reset()
env.close()
