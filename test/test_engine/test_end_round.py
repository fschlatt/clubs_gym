import random

import pytest

import clubs
from clubs import error


def test_all_but_one_fold():

    config = clubs.configs.NO_LIMIT_HOLDEM_SIX_PLAYER

    dealer = clubs.poker.Dealer(**config)

    obs = dealer.reset(reset_button=True, reset_stacks=True)

    bet = -1
    for _ in range(5):
        obs, payouts, done = dealer.step(bet)

    assert all(done)
    assert obs["pot"] == 3
    test_payouts = [0, -1, 1, 0, 0, 0]
    assert all(
        payout == test_payout for payout, test_payout in zip(payouts, test_payouts)
    )
    test_stacks = [200, 199, 201, 200, 200, 200]
    assert all(
        stack == test_stack for stack, test_stack in zip(obs["stacks"], test_stacks)
    )


def test_all_all_in():
    random.seed(42)

    config = clubs.configs.NO_LIMIT_HOLDEM_SIX_PLAYER

    dealer = clubs.poker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)

    bet = 200
    for _ in range(6):
        obs, payouts, done = dealer.step(bet)

    assert all(done)
    assert obs["pot"] == 1200
    test_payouts = [-200, -200, -200, -200, -200, 1000]
    assert all(
        payout == test_payout for payout, test_payout in zip(payouts, test_payouts)
    )
    test_stacks = [0, 0, 0, 0, 0, 1200]
    assert all(
        stack == test_stack for stack, test_stack in zip(obs["stacks"], test_stacks)
    )


def test_bet_after_round_end():

    random.seed(42)

    config = clubs.configs.NO_LIMIT_HOLDEM_SIX_PLAYER

    dealer = clubs.poker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)

    bet = 200
    for _ in range(6):
        obs, payouts, done = dealer.step(bet)

    assert all(done)
    assert obs["call"] == obs["min_raise"] == obs["max_raise"] == 0
    assert obs["action"] == -1

    obs, payouts, done = dealer.step(bet)

    assert all(done)
    assert obs["call"] == obs["min_raise"] == obs["max_raise"] == 0
    assert obs["action"] == -1


def test_too_few_players():

    random.seed(42)

    config = clubs.configs.NO_LIMIT_HOLDEM_SIX_PLAYER

    dealer = clubs.poker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)

    bet = 200
    for _ in range(6):
        obs, payouts, done = dealer.step(bet)

    assert all(done)
    assert obs["pot"] == 1200
    test_payouts = [-200, -200, -200, -200, -200, 1000]
    assert all(
        payout == test_payout for payout, test_payout in zip(payouts, test_payouts)
    )
    test_stacks = [0, 0, 0, 0, 0, 1200]
    assert all(
        stack == test_stack for stack, test_stack in zip(obs["stacks"], test_stacks)
    )

    with pytest.raises(error.TooFewActivePlayersError):
        dealer.reset()
