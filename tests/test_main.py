import unittest
import gym
import gym_th
import numpy

from gym_th.envs import ForgivingEnv


class Environments(unittest.TestCase):
    def test_env(self):
        env = gym.make('th-v0')
        env.reset()
        m = env.moves[0]
        env.step(m)
        env.step(numpy.int64(m))


class Parsing(unittest.TestCase):
    def test_env(self):
        for i in range(2 * 7 * 8):
            print(ForgivingEnv._parse_action(i))


class Unarsing(unittest.TestCase):
    def test_env(self):
        for i in range(2 * 7 * 8):
            print(ForgivingEnv._unparse_action(*ForgivingEnv._parse_action(i)))


if __name__ == '__main__':
    unittest.main()
