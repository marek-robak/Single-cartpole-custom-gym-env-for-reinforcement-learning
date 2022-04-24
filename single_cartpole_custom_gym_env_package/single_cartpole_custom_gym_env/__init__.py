from single_cartpole_custom_gym_env.single_cartpole_env import *
from gym.envs.registration import register

register(
    id='single-cartpole-custom-v0',
    entry_point='single_cartpole_custom_gym_env:SingleCartpoleEnv',
    kwargs={'render_sim': False, 'n_steps': 1000}
)
