from pyker import configs, deuces, engine


def test_game():

    config = configs.LEDUC_2P_ENV

    dealer = engine.Dealer(**config)

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
    obs, reward, done, info = dealer.step(action)

    assert all(done)
    assert reward[0] > reward[1]
    assert reward[0] == 7


def test_limit_betting_size():

    config = configs.LIMIT_HOLDEM_6P_ENV

    dealer = engine.Dealer(**config)

    _ = dealer.reset(reset_stacks=True, reset_button=True)
    action = {'fold': 0, 'bet': 2.1}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 5
    assert obs['street_commits'].sum() == obs['pot']

    action = {'fold': 0, 'bet': 10}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 9
    assert obs['street_commits'].sum() == obs['pot']

    action = {'fold': 1, 'bet': 4}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 9
    assert not obs['active'].all()


def test_heads_up():

    config = configs.NOLIMIT_HOLDEM_2P_ENV

    dealer = engine.Dealer(**config)

    obs = dealer.reset(reset_stacks=True, reset_button=True)

    assert obs['call'] == 1
    assert obs['min_raise'] == 3
    assert obs['max_raise'] == 199

    action = {'fold': 0, 'bet': 1}
    obs, *_ = dealer.step(action)

    assert obs['call'] == 0
    assert obs['min_raise'] == 2
    assert obs['max_raise'] == 198


def test_incomplete_raise():

    config = configs.NOLIMIT_HOLDEM_6P_ENV
    config['num_players'] = 3

    dealer = engine.Dealer(**config)

    dealer.stacks[1] = dealer.stacks[1] - 190
    dealer.stacks[2] = dealer.stacks[2] + 190

    obs = dealer.reset(reset_stacks=False, reset_button=True)

    action = {'fold': 0, 'bet': 8}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 11
    assert obs['call'] == 7
    assert obs['min_raise'] == 9
    assert obs['max_raise'] == 9

    action = {'fold': 0, 'bet': 9}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 20
    assert obs['call'] == 8
    assert obs['min_raise'] == 14  # call 8 + 6 largest valid raise

    action = {'fold': 0, 'bet': 8}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 28
    assert obs['call'] == 2
    assert obs['min_raise'] == 0
    assert obs['max_raise'] == 0


def test_pot_limit_betting_size():

    config = configs.POT_LIMIT_OMAHA_6P_ENV

    dealer = engine.Dealer(**config)

    obs = dealer.reset(reset_stacks=True, reset_button=True)
    assert obs['min_raise'] == 4
    assert obs['max_raise'] == 7

    action = {'fold': 0, 'bet': 4}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 7
    assert obs['call'] == 4
    assert obs['min_raise'] == 6
    assert obs['max_raise'] == 15  # call + call + pot (2 * 4 + 7)

    action = {'fold': 0, 'bet': 4}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 4}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 4}


def test_split_pot():

    config = configs.NOLIMIT_HOLDEM_9P_ENV

    dealer = engine.Dealer(**config)

    hands = [
        ['6c', '8s'], ['Ac', 'Ad'], ['Kd', '2h'], ['Th', '9c'], ['Js', 'Jc'],
        ['6h', '8d'], ['5c', '7d'], ['Qh', '2c'], ['3d', '4s']]
    comm_cards = ['4d', '5h', '7c', 'Ac', 'Kh']
    top_cards = [card for hand in hands for card in hand] + comm_cards
    dealer.deck = dealer.deck.trick(top_cards)

    obs = dealer.reset(reset_stacks=True, reset_button=True)

    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 5}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 5}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 5}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 5}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 4}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 27
    # flop
    action = {'fold': 0, 'bet': 4}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 4}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 4}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 4}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 43

    while True:
        action = {'fold': 0, 'bet': 0}
        obs, reward, done, _ = dealer.step(action)
        if all(done):
            break
    assert not sum(reward)
    assert_payout = [12, -9, -2, 0, -5, 13, -9, 0, 0]
    assert all(rew == ass_pay for rew, ass_pay in zip(reward, assert_payout))
