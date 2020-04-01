import clubs


def test_game():

    config = clubs.configs.LEDUC_2P_ENV

    dealer = clubs.Dealer(**config)

    dealer.deck = dealer.deck.trick(['Qs', 'Ks', 'Qh'])

    obs = dealer.reset(reset_button=True, reset_stacks=True)

    bet = 2
    _ = dealer.step(bet)
    bet = 4
    _ = dealer.step(bet)
    bet = 2
    _ = dealer.step(bet)
    bet = 0
    _ = dealer.step(bet)
    bet = 2
    _ = dealer.step(bet)
    bet = 2
    obs, payout, done = dealer.step(bet)

    assert all(done)
    assert payout[0] > payout[1]
    assert payout[0] == 7


def test_heads_up():

    config = clubs.configs.NOLIMIT_HOLDEM_2P_ENV

    dealer = clubs.Dealer(**config)

    obs = dealer.reset(reset_button=True, reset_stacks=True)

    assert obs['action'] == 0
    assert obs['call'] == 1
    assert obs['min_raise'] == 3
    assert obs['max_raise'] == 199

    bet = 1
    obs, *_ = dealer.step(bet)

    assert obs['call'] == 0
    assert obs['min_raise'] == 2
    assert obs['max_raise'] == 198
