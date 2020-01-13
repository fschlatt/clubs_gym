import pyker


def test_game():

    config = pyker.configs.LEDUC_2P_ENV

    dealer = pyker.Dealer(**config)

    dealer.deck = dealer.deck.trick(['Qs', 'Ks', 'Qh'])

    obs = dealer.reset(reset_stacks=True, reset_button=True)

    action = {'fold': 0, 'bet': 2}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 4}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 2}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 2}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 2}
    obs, payout, done, info = dealer.step(action)

    assert all(done)
    assert payout[0] > payout[1]
    assert payout[0] == 7


def test_heads_up():

    config = pyker.configs.NOLIMIT_HOLDEM_2P_ENV

    dealer = pyker.Dealer(**config)

    obs = dealer.reset(reset_stacks=True, reset_button=True)

    assert obs['action'] == 0
    assert obs['call'] == 1
    assert obs['min_raise'] == 3
    assert obs['max_raise'] == 199

    action = {'fold': 0, 'bet': 1}
    obs, *_ = dealer.step(action)

    assert obs['call'] == 0
    assert obs['min_raise'] == 2
    assert obs['max_raise'] == 198
