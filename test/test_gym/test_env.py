import io
from contextlib import redirect_stdout

import clubs
import gym
import pytest

import clubs_gym
from clubs_gym import error


def test_env():
    env = gym.make("NoLimitHoldemTwoPlayer-v0")
    dealer = clubs.poker.Dealer(**clubs.configs.NO_LIMIT_HOLDEM_TWO_PLAYER)

    env_obs = env.reset()
    dealer_obs = dealer.reset()

    assert list(env_obs.keys()) == list(dealer_obs.keys())
    iterator = zip(env_obs["stacks"], dealer_obs["stacks"])
    assert all(stack_1 == stack_2 for stack_1, stack_2 in iterator)

    bet = 10
    env_obs, *_ = env.step(bet)
    dealer_obs, *_ = dealer.step(bet)

    assert env_obs["pot"] == dealer_obs["pot"]

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        env.render("ascii")
    string = stdout.getvalue()

    assert "Action on Player 1" in string

    assert env.close() is None


def test_register():
    env = gym.make("KuhnTwoPlayer-v0")

    with pytest.raises(error.NoRegisteredAgentsError):
        env.act({})

    env.register_agents(
        [clubs_gym.agent.kuhn.NashKuhnAgent(0), clubs_gym.agent.kuhn.NashKuhnAgent(0)]
    )

    with pytest.raises(error.EnvironmentResetError):
        env.act({})

    env.register_agents(
        {
            0: clubs_gym.agent.kuhn.NashKuhnAgent(0),
            1: clubs_gym.agent.kuhn.NashKuhnAgent(0),
        }
    )

    obs = env.reset()
    action = env.act(obs)
    _ = env.step(action)


def test_errors():
    env = gym.make("NoLimitHoldemTwoPlayer-v0")
    with pytest.raises(error.InvalidAgentConfigurationError):
        env.register_agents(None)

    with pytest.raises(error.InvalidAgentConfigurationError):
        env.register_agents([None, None])

    with pytest.raises(error.InvalidAgentConfigurationError):
        env.register_agents([None])

    with pytest.raises(error.InvalidAgentConfigurationError):
        env.register_agents(
            {
                4: clubs_gym.agent.kuhn.NashKuhnAgent(0),
                5: clubs_gym.agent.kuhn.NashKuhnAgent(0),
            }
        )
