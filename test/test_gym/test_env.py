import gym

import clubs
from clubs import configs


def test_env():
    env = gym.make('NoLimitHoldemTwoPlayer-v0')
    dealer = clubs.Dealer(configs.NOLIMIT_HOLDEM_TWO_PLAYER_ENV)

    env_obs = env.reset()
    dealer_obs = dealer.reset()

    assert list(env_obs.keys()) == list(dealer_obs.keys())
    assert env_obs['stacks'] == dealer_obs['stacks']

    bet = 10
    env_obs, *_ = env.step(bet)
    dealer_obs, *_ = dealer.step(bet)

    assert env_obs['pot'] == dealer_obs['pot']

    assert env.render()

    assert env.close() is None

