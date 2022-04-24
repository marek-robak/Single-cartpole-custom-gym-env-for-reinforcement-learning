from single_cartpole_custom_gym_env.event_handler import *
from single_cartpole_custom_gym_env.Cartpole import *

import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import random
import os

class SingleCartpoleEnv(gym.Env):
    """
    render_sim: (bool) if true, a graphic is generated
    n_steps: (int) number of time steps
    """

    def __init__(self, render_sim=False, n_steps=1000):
        self.render_sim = render_sim

        if self.render_sim is True:
            self.init_pygame()

        self.init_pymunk()

        #Parameters
        self.max_time_steps = n_steps
        self.force_scale = 1200

        #Initial values
        self.force = 0
        self.done = False
        self.first_step = True
        self.current_time_step = 0

        #Definitions of the action and observation space
        self.min_action = np.array([-1], dtype=np.float32)
        self.max_action = np.array([1], dtype=np.float32)
        self.action_space = spaces.Box(low=self.min_action, high=self.max_action, dtype=np.float32)

        self.min_observation = np.array([-1, -1, -1, -1], dtype=np.float32)
        self.max_observation = np.array([1, 1, 1, 1,], dtype=np.float32)
        self.observation_space = spaces.Box(low=self.min_observation, high=self.max_observation, dtype=np.float32)

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Single Cartpole Environment")
        self.clock = pygame.time.Clock()

        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join("img", "icon.png")
        icon_path = os.path.join(script_dir, icon_path)
        pygame.display.set_icon(pygame.image.load(icon_path))

    def init_pymunk(self):
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0, -1000)

        if self.render_sim is True:
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
            self.draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
            pymunk.pygame_util.positive_y_is_up = True

        #Starting position
        initial_x = 400
        initial_y = 400
        self.target = random.uniform(150, 650)

        self.track = Track(0, 400, 800, 400, 0, self.space)

        self.cart_mass = 1
        self.cart = Cart(initial_x, initial_y, 80, 40, self.cart_mass, (33, 93, 191), self.space)

        self.pole_mass = 1
        self.pole_length = 160
        pole_thickness = 15
        alpha = random.uniform(np.pi*25/18, np.pi*29/18)
        pole_x = initial_x + self.pole_length * np.cos(alpha)
        pole_y = initial_y + self.pole_length * np.sin(alpha)
        self.pole = Pole(pole_x, pole_y, initial_x, initial_y, pole_thickness, self.pole_mass, (66, 135, 245), self.space)

        self.left_slider = pymunk.GrooveJoint(self.track.body, self.cart.body, (0, 400), (800, 400), (-20, 0))
        self.left_slider.error_bias = 0
        self.left_slider.collide_bodies = False
        self.space.add(self.left_slider)

        self.right_slider = pymunk.GrooveJoint(self.track.body, self.cart.body, (0, 400), (800, 400), (20, 0))
        self.right_slider.error_bias = 0
        self.right_slider.collide_bodies = False
        self.space.add(self.right_slider)

        self.pivot_1 = pymunk.PivotJoint(self.cart.body, self.pole.body, (0, 0), (-self.pole_length/2, 0))
        self.pivot_1.error_bias = 0
        self.pivot_1.collide_bodies = False
        self.space.add(self.pivot_1)

    def step(self, action):
        self.force = action[0] * self.force_scale
        self.cart.body.apply_force_at_local_point((self.force, 0), (0, 0))

        #Friction
        pymunk.Body.update_velocity(self.pole.body, Vec2d(0, 0), 0.999, 1/60.0)
        pymunk.Body.update_velocity(self.cart.body, Vec2d(0, 0), 0.9999, 1/60.0)

        obs = self.get_observation()
        if np.abs(obs[1]) <= 1.0/18:
            stand = True
        else:
            stand = False

        self.space.step(1 / 60.0)
        self.current_time_step += 1

        #Reward function
        obs = self.get_observation()
        if np.abs(obs[1]) <= 1.0/18:
            reward = 10 + (-np.abs(obs[3])+1)*20
        else:
            reward = (-(18.0/17)*np.abs(obs[1])+(18.0/17)) + (-np.abs(obs[3])+1)*0.5

        #Penalty for loss of balance
        if np.abs(obs[1]) > 1.0/18 and stand == True:
            reward = -50

        #Stops episode when cart hits wall
        if np.abs(obs[3]) == 1:
            self.done = True
            reward = -100

        #Stops episode, when time is up
        if self.current_time_step == self.max_time_steps:
            self.done = True

        return obs, reward, self.done, {}

    def get_observation(self):
        cart_position_x = np.clip((1.0/360)*self.cart.body.position[0]-(10.0/9), -1, 1)
        cart_velocity = np.clip(self.cart.body.velocity_at_local_point((0, 0))[0]/850, -1, 1)
        pole_angle = (((self.pole.body.angle+np.pi/2) % (2*np.pi)) + (2*np.pi)) % (2*np.pi)
        pole_angle = np.clip(-pole_angle/np.pi + 1, -1, 1)
        pole_angular_velocity = np.clip(self.pole.body.angular_velocity/15, -1, 1)

        #calculatng distance from target line
        x = self.cart.body.position[0]
        if x < self.target:
            distance_x = np.clip((x/(self.target-40) - self.target/(self.target-40)) , -1, 0)
        else:
            distance_x = np.clip((-x/(self.target-760) + self.target/(self.target-760)) , 0, 1)

        return np.array([cart_velocity, pole_angle, pole_angular_velocity, distance_x])

    def render(self, mode='human', close=False):
        x, y = self.cart.body.position
        scale = 1.0/12

        pygame_events()

        self.screen.fill((243, 243, 243))
        pygame.draw.line(self.screen, (255, 26, 26), (self.target, 0), (self.target, 800), 2)

        self.space.debug_draw(self.draw_options)

        pivot_point = self.pole.body.local_to_world([-self.pole_length/2, 0])
        pygame.draw.circle(self.screen, (33, 93, 191), (pivot_point[0], 800-pivot_point[1]), 5)
        pygame.draw.line(self.screen, (179,179,179), (x-scale*self.force_scale, 399), (x+scale*self.force_scale, 399), 4)

        if self.force != 0:
            pygame.draw.line(self.screen, (255,0,0), (x, 399), (x+scale*self.force, 399), 4)

        pygame.display.flip()
        self.clock.tick(60)

    def reset(self):
        self.__init__(self.render_sim, self.max_time_steps)
        return self.get_observation()

    def close(self):
        pygame.quit()
