import unittest
import gym
import gym_th
import numpy


class Environments(unittest.TestCase):
    def test_env(self):
        env = gym.make('th-v0')
        env.reset()
        env.step(0)
        env.step(numpy.int64(1))


if __name__ == '__main__':
    unittest.main()
