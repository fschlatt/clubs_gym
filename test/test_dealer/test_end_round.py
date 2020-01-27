import random

import pyker

def test_all_but_one_fold():

    config = pyker.configs.NOLIMIT_HOLDEM_6P_ENV

    dealer = pyker.Dealer(**config)

    obs = dealer.reset(reset_button=True, reset_stacks=True)

    action = {'fold': 1, 'bet': 0}
    for _ in range(5):
        obs, payouts, done, _ = dealer.step(action)
    
    assert all(done)
    assert obs['pot'] == 3
    test_payouts = [0, -1, 1, 0, 0, 0]
    assert all(payout == test_payout
               for payout, test_payout in zip(payouts, test_payouts))
    test_stacks = [200, 199, 201, 200, 200, 200]
    assert all(stack == test_stack
               for stack, test_stack in zip(obs['stacks'], test_stacks))

def test_all_all_in():
    random.seed(42)

    config = pyker.configs.NOLIMIT_HOLDEM_6P_ENV

    dealer = pyker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)

    action = {'fold': 0, 'bet': 200}
    for _ in range(6):
        obs, payouts, done, _ = dealer.step(action)
    
    assert all(done)
    assert obs['pot'] == 1200
    test_payouts = [-200, -200, -200, -200, -200, 1000]
    assert all(payout == test_payout
               for payout, test_payout in zip(payouts, test_payouts))
    test_stacks = [0, 0, 0, 0, 0, 1200]
    assert all(stack == test_stack
               for stack, test_stack in zip(obs['stacks'], test_stacks))


def test_action_after_round_end():

    random.seed(42)

    config = pyker.configs.NOLIMIT_HOLDEM_6P_ENV

    dealer = pyker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)

    action = {'fold': 0, 'bet': 200}
    for _ in range(6):
        obs, payouts, done, _ = dealer.step(action)
    
    assert all(done)
    assert obs['call'] == obs['min_raise'] == obs['max_raise'] == 0
    assert obs['action'] == -1

    obs, payouts, done, _ = dealer.step(action)

    assert all(done)
    assert obs['call'] == obs['min_raise'] == obs['max_raise'] == 0
    assert obs['action'] == -1
