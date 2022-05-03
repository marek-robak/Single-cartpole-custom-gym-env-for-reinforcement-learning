# Single-cartpole-custom-gym-env-for-reinforcement-learning

This repository contains OpenAI Gym environment designed for teaching RL
agents the ability to bring the cartpole upright and its further balancing.
To make this easy to use, the environment has been packed into a Python package,
which automatically registers the environment in the Gym library when the package
is included in the code. As a result, it can be easily used in conjunction with
reinforcement learning libraries such as StableBaselines3. There is also a sample
code for training and evaluating agents in this environment.

<p align="center">
  <img src="media/cartpole_540.gif"/>
</p>

## Installation

These instructions will guide you through installation of the environment and
show you how to use it for your projects. Whichever method of installation you
choose I recommend running it in a virtual environment created by Miniconda.
This program is used to simplify package management and deployment.

So, to get started, install Miniconda, [here](https://docs.conda.io/en/latest/miniconda.html)
is the official installation guide along with a detailed description.

In the following way you can create and activate virtual environment:

```
conda create -n <environment_name> python=3.9
conda activate <environment_name>
```

### Installation via pip - package installer for Python

You just need to type

```
pip install single-cartpole-custom-gym-env
```

### Installation via source code from GitHub repository

If you want to make specific changes to the source code or extend it with your
own functionalities this method will suit you.

```
git clone https://github.com/marek-robak/Single-cartpole-custom-gym-env-for-reinforcement-learning.git
cd Single-cartpole-custom-gym-env-for-reinforcement-learning/single_cartpole_custom_gym_env_package
pip install -e .
```

### How to use it in your code

Now all you need to do to use this environment in your code is import the package.
After that, you can use it with Gym and StableBaselines3 library via its
id: single-cartpole-custom-v0.

```
from stable_baselines3 import PPO
import gym

import single_cartpole_custom_gym_env

env = gym.make('single-cartpole-custom-v0')

model = PPO("MlpPolicy", env)

model.learn(total_timesteps=1500000)
model.save('new_agent')
```

### Environment prerequisites

Environment to run needs Python3 with Gym, Pygame, Pymunk, Numpy and StableBaselines3
libraries. All of them are automatically installed when the package is installed.

## Environment details

This environment consists of a cart attached to a straight rail and an inertial
pendulum loosely attached to the cart. The RL agent can control the force acting
on the cart. This force influences the movement of the cart, which then translates
into the swing angle of the pendulum. The pendulum and the cart separately are
rigid bodies with the same mass. The agent's goal is to learn how to place the
pendulum vertically and then transport the cartpole to a randomly designated point
on the rail. Both the forces acting on the cart and the target point on the rail
are marked with red lines.

The physics engine for this environment runs at 60fps.

### Initial episode conditions

At the beginning of each episode, the cartpole is placed in the center of the
available space. Then, the initial inclination of the pendulum to the vertical axis
from 0° to 20° is drawn. The location of the target is also randomized.

### Ending episode conditions

Each episode ends if the cart goes off-screen or if the set number of timesteps
has passed.

### Agent action and observation space

The space of actions made available to the RL agent consists of one value from -1
to 1. It is correlated with the force acting on the cart, -1 and 1 are maximum forces,
0 is no force acting.

The observation space consists of fours values, all ranging from -1 to 1.
- The first one carries information about the distance of the cart from the walls
and the target point. A 0 is returned when the cart is at the target point
and values -1 and 1 when the cart touches the left or right wall.
- The second number informs about the current swing angle of the pendulum.
It is scaled to return 0 for a vertically upward pendulum, and -1 and 1 for a
downward pendulum.
- The third number contains information about the speed at which the cart is moving.
It has been graduated so that the values -1 and 1 represent the maximum possible
speed that the cart can develop in the available space.
- The fourth number contains information about the angular velocity of the pendulum.
It has been scaled so that the values -1 and 1 represent the maximum achievable values.

### Reward function

The task that the agent must perform consists of two phases. In the first one, it has to
swing the pendulum vertically. In the second, while keeping the balance, it has to move the cart
to the target point. For this reason, the reward function has been split into two expressions.
The first is the weighted sum of the linear dependencies of the pendulum deflection angle and
its distance from the target. It is awarded when the pendulum is inclined from the vertical
by an angle of more than 10°. The values ​​of the parameters of this sum were selected to
promote the swing of the pendulum more than to transport the cart to its destination. The
second formula works when the angle of the pendulum to the vertical is less than 10°. In
this phase, the agent must be concerned mainly with not losing his balance and transporting
the cart closer to the target point. For this reason, this part of the function is a linear
dependence of only the distance of the cart from the target plus a penalty for loss of
balance. The agent is also penalized for hitting a cart against a wall.

<img src="https://camo.githubusercontent.com/e93f9a8c3de5a22348ead470a04d5b8b439edba972f984568b1f4d57fde1a706/68747470733a2f2f6c617465782e636f6465636f67732e636f6d2f7376672e696d6167653f7b5c6c617267655c636f6c6f727b626c61636b7d5228782c5c616c706861293d5c6c6566745c7b5c626567696e7b6d61747269787d285c667261637b31387d7b31377d29282d5c6c6566747c5c616c7068615c72696768747c2b31292b285c667261637b317d7b327d29282d5c6c6566747c785c72696768747c2b31292c265c616c7068613e5c667261637b317d7b31387d5c5c31302b3230282d5c6c6566747c785c72696768747c2b31292c265c616c7068615c6c65715c667261637b317d7b31387d5c5c2d3130302c265c7465787475707b77616c6c2673706163653b636f6c6c6973696f6e2673706163653b70656e616c74797d5c5c2d35302c265c7465787475707b70656e616c74792673706163653b666f722673706163653b6c6f73732673706163653b6f662673706163653b62616c616e63657d5c656e647b6d61747269787d5c72696768742e7d2367682d6c696768742d6d6f64652d6f6e6c79#gh-light-mode-only">

<img src="https://camo.githubusercontent.com/17641dd11fa7f4059cdb47659f240e6e1abbe48bb6a10eefc102c6c26035a202/68747470733a2f2f6c617465782e636f6465636f67732e636f6d2f7376672e696d6167653f7b5c6c617267655c636f6c6f727b77686974657d5228782c5c616c706861293d5c6c6566745c7b5c626567696e7b6d61747269787d285c667261637b31387d7b31377d29282d5c6c6566747c5c616c7068615c72696768747c2b31292b285c667261637b317d7b327d29282d5c6c6566747c785c72696768747c2b31292c265c616c7068613e5c667261637b317d7b31387d5c5c31302b3230282d5c6c6566747c785c72696768747c2b31292c265c616c7068615c6c65715c667261637b317d7b31387d5c5c2d3130302c265c7465787475707b77616c6c2673706163653b636f6c6c6973696f6e2673706163653b70656e616c74797d5c5c2d35302c265c7465787475707b70656e616c74792673706163653b666f722673706163653b6c6f73732673706163653b6f662673706163653b62616c616e63657d5c656e647b6d61747269787d5c72696768742e7d2367682d6461726b2d6d6f64652d6f6e6c79#gh-dark-mode-only">

Variables x and 𝛼 are the first and second values from the agent observation space.

### Environment parameters

This environment provides two parameters that can change the way it works.

- render_sim: (bool) if true, a graphic is generated
- n_steps: (int) number of time steps

```
env = gym.make('single-cartpole-custom-v0', render_sim=True, n_steps=1000)
```

## See also

Everything available in this repository was created for the needs of my bachelor thesis.
If you can read in Polish and you are interested in it, you can find it
[here](https://www.ap.uj.edu.pl/diplomas/151837/?_s=1). It includes details on the
training process for sample agents and a description of the reward function selection process.

You may also be interested in other environments I have created. Go to the repositories
where they are located by clicking on the gifs below.

<p align="center">
  <a href="https://github.com/mareo1208/Drone-2d-custom-gym-env-for-reinforcement-learning.git">
    <img src="media/drone_360.gif"/>
  </a>
  <a href="https://github.com/mareo1208/Double-cartpole-custom-gym-env-for-reinforcement-learning">
    <img src="media/double_cartpole_360.gif"/>
  </a>
</p>
