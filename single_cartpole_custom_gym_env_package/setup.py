from setuptools import setup, find_packages
import os

DESCRIPTION = 'OpenAI Gym environment designed for training RL agents to bring CartPole upright and its further balancing.'
LONG_DESCRIPTION = ('This package contains OpenAI Gym environment designed for training RL agents to bring CartPole upright '
                    'and its further balancing. The environment is automatically registered under id: single-cartpole-custom-v0, '
                    'so it can be easily used by RL agent training libraries, such as StableBaselines3.<br /><br />At the '
                    'https://github.com/mareo1208/Single-cartpole-custom-gym-env-for-reinforcement-learning.git you can find a '
                    'detailed description of the environment, along with a description of the package installation and sample '
                    'code made to train and evaluate agents in this environment.<br /><br />This environment was created for '
                    'the needs of my bachelor\'s thesis, available at https://www.ap.uj.edu.pl/diplomas/151837/ site.')

setup(
    name='single_cartpole_custom_gym_env',
    version='1.2.3',
    author='Marek Robak',
    author_email='maro.robak@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/marek-robak/Single-cartpole-custom-gym-env-for-reinforcement-learning.git',
    download_url='https://pypi.org/project/single-cartpole-custom-gym-env/',
    packages=find_packages(),
    include_package_data = True,
    install_requires=['gym', 'pygame', 'pymunk', 'numpy', 'stable-baselines3[extra]'],
    keywords=['reinforcement learning', 'gym environment', 'StableBaselines3', 'OpenAI Gym']
)
