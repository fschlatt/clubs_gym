import pyker

def test_limit_bet_size():

    config = pyker.configs.LIMIT_HOLDEM_6P_ENV

    dealer = pyker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)
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

def test_all_in_bet_size():
    config = pyker.configs.NOLIMIT_HOLDEM_2P_ENV

    dealer = pyker.Dealer(**config)

    dealer.stacks[0] -= 150
    dealer.stacks[1] += 150

    obs = dealer.reset(reset_button=True, reset_stacks=False)

    action = {'fold': 0, 'bet': 100}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 52
    action = {'fold': 0, 'bet': 1000}
    obs, *_ = dealer.step(action)
    assert obs['pot'] == 400

def test_incomplete_raise():

    config = dict(**pyker.configs.NOLIMIT_HOLDEM_6P_ENV)

    dealer = pyker.Dealer(**config)

    dealer.stacks[1] = dealer.stacks[1] - 190
    dealer.stacks[2] = dealer.stacks[2] + 190

    obs = dealer.reset(reset_button=True, reset_stacks=False)

    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    _ = dealer.step(action)
    _ = dealer.step(action)
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


def test_pot_limit_bet_size():

    config = pyker.configs.POT_LIMIT_OMAHA_6P_ENV

    dealer = pyker.Dealer(**config)

    obs = dealer.reset(reset_button=True, reset_stacks=True)
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

def test_bet_rounding():

    config = pyker.configs.NOLIMIT_HOLDEM_9P_ENV

    dealer = pyker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)

    action = {'fold': 0, 'bet': 1}
    obs, *_ = dealer.step(action)
    assert obs['street_commits'][3] == 0

    action = {'fold': 0, 'bet': 6}
    obs, *_ = dealer.step(action)
    assert obs['street_commits'][4] == 6

    action = {'fold': 0, 'bet': 3}
    obs, *_ = dealer.step(action)
    assert obs['street_commits'][5] == 0
    assert not obs['active'][5]

    action = {'fold': 0, 'bet': 4}
    obs, *_ = dealer.step(action)
    assert obs['street_commits'][6] == 6

    action = {'fold': 0, 'bet': 8}
    obs, *_ = dealer.step(action)
    assert obs['street_commits'][7] == 6

    action = {'fold': 0, 'bet': 9}
    obs, *_ = dealer.step(action)
    assert obs['street_commits'][8] == 10
