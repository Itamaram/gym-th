from gym.envs.registration import register

register(
    id='th-v0',
    entry_point='gym_th.envs:ForgivingEnv',
)