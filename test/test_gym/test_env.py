import io
from contextlib import redirect_stdout


import gym

import clubs
from clubs import configs


def test_env():
    env = gym.make('NoLimitHoldemTwoPlayer-v0')
    dealer = clubs.Dealer(**configs.NO_LIMIT_HOLDEM_TWO_PLAYER)

    env_obs = env.reset()
    dealer_obs = dealer.reset()

    assert list(env_obs.keys()) == list(dealer_obs.keys())
    assert all(env_obs['stacks'] == dealer_obs['stacks'])

    bet = 10
    env_obs, *_ = env.step(bet)
    dealer_obs, *_ = dealer.step(bet)

    assert env_obs['pot'] == dealer_obs['pot']

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        env.render()
    string = stdout.getvalue()

    assert 'Action on Player 1' in string

    assert env.close() is None
