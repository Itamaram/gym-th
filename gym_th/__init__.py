from gym.envs.registration import register

register(
    id='th-v0',
    entry_point='gym_th.envs:ForgivingEnv',
)

register(
    id='th-single',
    entry_point='gym_th.envs:ForgivingEnv',
    kwargs={'critical_success': True, 'failure_reward': -0.1},
)
