import pytest

import clubs
from clubs import error


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


def test_init():

    config = {**clubs.configs.NOLIMIT_HOLDEM_2P_ENV}

    blinds = config['blinds']
    antes = config['antes']
    raise_sizes = config['raise_sizes']
    num_raises = config['num_raises']
    num_community_cards = config['num_community_cards']

    config['blinds'] = [0]
    with pytest.raises(error.InvalidConfigError):
        clubs.Dealer(**config)
    config['blinds'] = blinds

    config['antes'] = [0]
    with pytest.raises(error.InvalidConfigError):
        clubs.Dealer(**config)
    config['antes'] = antes

    config['raise_sizes'] = [0]
    with pytest.raises(error.InvalidConfigError):
        clubs.Dealer(**config)
    config['raise_sizes'] = raise_sizes

    config['num_raises'] = [0]
    with pytest.raises(error.InvalidConfigError):
        clubs.Dealer(**config)
    config['num_raises'] = num_raises

    config['num_community_cards'] = [0]
    with pytest.raises(error.InvalidConfigError):
        clubs.Dealer(**config)
    config['num_community_cards'] = num_community_cards

    config['blinds'] = 0
    config['antes'] = 0
    config['raise_sizes'] = 0
    config['num_raises'] = 0
    config['num_community_cards'] = 0

    dealer = clubs.Dealer(**config)

    assert list(dealer.blinds) == [0, 0]
    assert list(dealer.antes) == [0, 0]
    assert list(dealer.raise_sizes) == [0, 0, 0, 0]
    assert list(dealer.num_raises) == [0, 0, 0, 0]
    assert list(dealer.num_community_cards) == [0, 0, 0, 0]

    config['blinds'] = blinds
    config['antes'] = antes
    config['raise_sizes'] = raise_sizes
    config['num_raises'] = num_raises
    config['num_community_cards'] = num_community_cards

    config['raise_sizes'] = 'lala'
    with pytest.raises(error.InvalidRaiseSizeError):
        clubs.Dealer(**config)
    config['raise_sizes'] = raise_sizes


def test_str_repr():

    config = clubs.configs.NOLIMIT_HOLDEM_2P_ENV

    dealer = clubs.Dealer(**config)

    assert len(str(dealer)) == 1242
    string = (
        f'Dealer ({id(dealer)}) - num players: {dealer.num_players}, '
        f'num streets: {dealer.num_streets}'
    )
    assert repr(dealer) == string


def test_init_step():

    config = clubs.configs.NOLIMIT_HOLDEM_2P_ENV

    dealer = clubs.Dealer(**config)

    with pytest.raises(error.TableResetError):
        dealer.step(0)
