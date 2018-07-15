import unittest
import gym
import gym_th


class Environments(unittest.TestCase):
    def test_env(self):
        env = gym.make('th-v0')
        env.reset()
        env.step(0)
        env.step(1)
