import gym
import numpy as np
import requests
from gym import spaces
from requests.adapters import HTTPAdapter


class ForgivingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,
                 critical_success=False,
                 critical_failure=False,
                 success_reward=1,
                 failure_reward=0,
                 starting_turns=10):
        self.critical_success = critical_success
        self.critical_failure = critical_failure
        self.success_reward = success_reward
        self.failure_reward = failure_reward
        self.starting_turns = starting_turns
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        self.endpoint = 'http://th.local/api/th/'
        self.action_space = spaces.Discrete(7 * 8 * 2)
        self.observation_space = spaces.Box(low=0, high=2, shape=(10, 8, 8), dtype=np.uint8)
        self.board = None
        self.turnsLeft = None
        self.turnsPlayed = None
        self.moves = []
        self.num_envs = 1

    def step(self, action):
        a = np.asscalar(action) if isinstance(action, np.generic) else action
        if a not in self.moves:
            return self.obs, -0.1, False, {}

        x1, y1, x2, y2 = ForgivingEnv._parse_action(action)
        payload = {
            'state': {'turnsPlayed': self.turnsPlayed, 'turnsLeft': self.turnsLeft, 'board': self.board},
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        # TODO: Error handling
        j = requests.post(self.endpoint + 'move', json=payload).json()
        self._save_game_state(j['state'])
        reward = self.success_reward if j['isSuccess'] else self.failure_reward
        done = self.turnsLeft <= 0 or (j['isSuccess'] and self.critical_success) or (not j['isSuccess'] and self.critical_failure)
        return self.obs, reward, done, {}

    def reset(self):
        r = requests.get(self.endpoint + 'new', params={'turns': self.starting_turns})
        self._save_game_state(r.json())
        return self.obs

    def _save_game_state(self, j):
        self.board = j['board']
        self.turnsLeft = j['turnsLeft']
        self.turnsPlayed = j['turnsPlayed']
        self.moves = [ForgivingEnv._unparse_action(m['x1'], m['y1'], m['x2'], m['y2']) for m in j['availableMoves']]
        self.obs = np.array(ForgivingEnv._generate_obs(j['board'], j['availableMoves']), dtype=np.uint8)

    def render(self, mode='human', close=False):
        pass

    @staticmethod
    def _generate_obs(board, moves):
        b = [[[1 if i == t else 0 for i in line] for line in board] for t in range(8)]
        mhorz = [x[:] for x in [[0] * 8] * 8]
        mvert = [x[:] for x in [[0] * 8] * 8]
        for m in moves:
            if m['x2'] - m['x1']:
                mhorz[m['x1']][m['y1']] = 1
            elif m['y2'] - m['y1']:
                mvert[m['x1']][m['y1']] = 1

        return b + [mhorz] + [mvert]

    @staticmethod
    def _parse_action(action):
        a = np.asscalar(action) if isinstance(action, np.generic) else action
        if a < 56:
            x1 = a // 8
            y1 = a % 8
            x2 = x1 + 1
            y2 = y1
        else:
            x1 = (a - 56) // 7
            y1 = (a - 56) % 7
            x2 = x1
            y2 = y1 + 1
        return x1, y1, x2, y2

    @staticmethod
    def _unparse_action(x1, y1, x2, y2):
        if x2 - x1:
            return x1 * 8 + y1
        elif y2 - y1:
            return x1 * 7 + y1 + 56
        return -1
