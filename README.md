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

<picture> 
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?%5CLarge%5Ccolor%7Bwhite%7D%20R_1%28x%29%3DA%28-%7C%5Calpha%7C%2B1%29%2BB%28-%7Cx%7C%2B1%29%2C%5Cquad%20A%3E%20B">
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?%5CLarge%5Ccolor%7Bblack%7D%20R_1%28x%29%3DA%28-%7C%5Calpha%7C%2B1%29%2BB%28-%7Cx%7C%2B1%29%2C%5Cquad%20A%3E%20B">
  <img alt="R₁(x) = A(−|α| + 1) + B(−|x| + 1),    A > B">
</picture>

<picture> 
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?%5CLarge%5Ccolor%7Bwhite%7D%20R_2%28x%29%3DC%2BD%28-%7Cx%7C%2B1%29%2C%5Cquad%20D%3E%20C%3E%5Cmax%28R_1%28x%29%29">
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?%5CLarge%5Ccolor%7Bblack%7D%20R_2%28x%29%3DC%2BD%28-%7Cx%7C%2B1%29%2C%5Cquad%20D%3E%20C%3E%5Cmax%28R_1%28x%29%29">
  <img alt="R₂(x) = C + D(−|x| + 1),    D > C > max(R₁(x))">
</picture>

Variables x and 𝛼 are the first and second values from the agent observation space.

<picture> 
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?%5CLarge%5Ccolor%7Bwhite%7D%20R%28x%29%3D%5Cbegin%7Bcases%7D%5Cfrac%7B18%7D%7B17%7D%28-%7C%5Calpha%7C%2B1%29%2B%5Cfrac%7B1%7D%7B2%7D%28-%7Cx%7C%2B1%29%20%26%5Cquad%5Calpha%3E%5Cfrac%7B1%7D%7B18%7D%5C%5C10%2B20%28-%7Cx%7C%2B1%29%20%26%5Cquad%5Calpha%5Cle%5Cfrac%7B1%7D%7B18%7D%5C%5C-100%20%26%5Cquad%7Cx%7C%3D1%5Ctext%7B%2C%20Penalty%20for%20colliding%20the%20cart%20with%20a%20wall%7D%5C%5C-50%20%26%5Cquad%5Ctext%7BPenalty%20for%20losing%20balance%7D%5Cend%7Bcases%7D">
  <source media="(prefers-color-scheme: dark)" srcset="https://latex.codecogs.com/svg.latex?%5CLarge%5Ccolor%7Bblack%7D%20R%28x%29%3D%5Cbegin%7Bcases%7D%5Cfrac%7B18%7D%7B17%7D%28-%7C%5Calpha%7C%2B1%29%2B%5Cfrac%7B1%7D%7B2%7D%28-%7Cx%7C%2B1%29%20%26%5Cquad%5Calpha%3E%5Cfrac%7B1%7D%7B18%7D%5C%5C10%2B20%28-%7Cx%7C%2B1%29%20%26%5Cquad%5Calpha%5Cle%5Cfrac%7B1%7D%7B18%7D%5C%5C-100%20%26%5Cquad%7Cx%7C%3D1%5Ctext%7B%2C%20Penalty%20for%20colliding%20the%20cart%20with%20a%20wall%7D%5C%5C-50%20%26%5Cquad%5Ctext%7BPenalty%20for%20losing%20balance%7D%5Cend%7Bcases%7D">
  <img alt="R(x) = {(18/17) * (−|α| + 1) + (1/2) * (−|x| + 1), if α > 1/18}, {10 + 20 * (−|x| + 1), if α ≤ 1/18}, {−100, if |x| = 1 (Penalty for colliding the cart with a wall)}, {−50 (Penalty for losing balance)}">
</picture>

Final function with selected parameter values.

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
