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


class Unparsing(unittest.TestCase):
    def test_env(self):
        for i in range(2 * 7 * 8):
            print(ForgivingEnv._unparse_action(*ForgivingEnv._parse_action(i)))


class GenerateObservations(unittest.TestCase):
    def test_env(self):
        board = [
            [3, 3, 1, 3, 2, 1, 3, 1],
            [0, 0, 3, 3, 1, 3, 2, 1],
            [0, 1, 0, 1, 0, 3, 3, 2],
            [2, 3, 3, 0, 3, 1, 0, 1],
            [0, 0, 3, 3, 2, 1, 2, 3],
            [1, 0, 0, 1, 3, 0, 1, 0],
            [0, 1, 2, 3, 2, 1, 3, 0],
            [0, 2, 3, 1, 2, 3, 3, 1]]
        moves = [
            {"x1": 0, "y1": 3, "x2": 0, "y2": 4}, {"x1": 0, "y1": 4, "x2": 0, "y2": 5},
            {"x1": 0, "y1": 5, "x2": 1, "y2": 5}, {"x1": 0, "y1": 5, "x2": 0, "y2": 6},
            {"x1": 0, "y1": 6, "x2": 1, "y2": 6}, {"x1": 1, "y1": 0, "x2": 1, "y2": 1},
            {"x1": 1, "y1": 1, "x2": 1, "y2": 2}, {"x1": 1, "y1": 3, "x2": 1, "y2": 4},
            {"x1": 2, "y1": 0, "x2": 3, "y2": 0}, {"x1": 2, "y1": 0, "x2": 2, "y2": 1},
            {"x1": 2, "y1": 1, "x2": 2, "y2": 2}, {"x1": 2, "y1": 4, "x2": 2, "y2": 5},
            {"x1": 3, "y1": 2, "x2": 3, "y2": 3}, {"x1": 3, "y1": 3, "x2": 4, "y2": 3},
            {"x1": 3, "y1": 3, "x2": 3, "y2": 4}, {"x1": 3, "y1": 4, "x2": 4, "y2": 4},
            {"x1": 3, "y1": 5, "x2": 4, "y2": 5}, {"x1": 4, "y1": 1, "x2": 5, "y2": 1},
            {"x1": 4, "y1": 2, "x2": 4, "y2": 3}, {"x1": 4, "y1": 3, "x2": 5, "y2": 3},
            {"x1": 4, "y1": 3, "x2": 4, "y2": 4}, {"x1": 4, "y1": 4, "x2": 4, "y2": 5},
            {"x1": 5, "y1": 0, "x2": 6, "y2": 0}, {"x1": 5, "y1": 1, "x2": 6, "y2": 1},
            {"x1": 5, "y1": 5, "x2": 6, "y2": 5}, {"x1": 5, "y1": 5, "x2": 5, "y2": 6},
            {"x1": 7, "y1": 2, "x2": 7, "y2": 3}]
        print(ForgivingEnv._generate_obs(board, moves))


if __name__ == '__main__':
    unittest.main()
