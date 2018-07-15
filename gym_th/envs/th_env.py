import gym
import numpy as np
import requests
from gym import spaces


class ForgivingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.endpoint = 'http://th.local/api/th/'
        self.action_space = spaces.Discrete(7 * 8 * 2)
        self.observation_space = spaces.Box(low=0, high=8, shape=(8, 8), dtype=np.uint8)
        self.board = None
        self.turnsLeft = None
        self.turnsPlayed = None

    def step(self, action):
        x1, y1, x2, y2 = ForgivingEnv._parse_action(action)
        payload = {
            'state': {'turnsPlayed': self.turnsPlayed, 'turnsLeft': self.turnsLeft, 'board': self.board.tolist()},
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        # TODO: Error handling
        j = requests.post(self.endpoint + 'move', json=payload).json()
        self._save_game_state(j['state'])
        reward = 1 if j['isSuccess'] else 0

        return self.board, reward, self.turnsLeft <= 0, {}

    def reset(self):
        r = requests.get(self.endpoint + 'new', params={'turns': 5})
        self._save_game_state(r.json())
        return self.board

    def _save_game_state(self, j):
        self.board = np.array(j['board'], dtype=np.uint8)
        self.turnsLeft = j['turnsLeft']
        self.turnsPlayed = j['turnsPlayed']

    def render(self, mode='human', close=False):
        pass

    @staticmethod
    def _parse_action(action):
        a = np.asscalar(action) if isinstance(action, np.generic) else action
        if a < 56:
            x1 = a // 8
            y1 = a % 8
            x2 = x1 + 1
            y2 = y1
        else:
            x1 = (a - 56) % 8
            y1 = (a - 56) // 8
            x2 = x1
            y2 = y1 + 1
        return x1, y1, x2, y2
