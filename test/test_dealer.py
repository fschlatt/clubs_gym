from pyker.poker.dealer import Dealer
from pyker.poker.deck import Deck
from pyker.poker.deck import Card
from pyker.poker import configs


def test_game():

    config = configs.LEDUC_2P_ENV

    dealer = Dealer(**config)

    deck = Deck(2, 3, order=[0, 2, 1])

    dealer.deck = deck
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
    assert reward[0] == 14


def test_limit_betting_size():

    config = configs.LIMIT_HOLDEM_6P_ENV

    dealer = Dealer(**config)

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

    dealer = Dealer(**config)

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

    dealer = Dealer(**config)

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

    dealer = Dealer(**config)

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

    dealer = Dealer(**config)

    deck = Deck()

    