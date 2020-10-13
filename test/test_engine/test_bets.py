import clubs


def test_limit_bet_size():

    config = clubs.configs.LIMIT_HOLDEM_SIX_PLAYER

    dealer = clubs.poker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)
    bet = 2.1
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 5
    assert sum(obs["street_commits"]) == obs["pot"]

    bet = 10
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 9
    assert sum(obs["street_commits"]) == obs["pot"]

    bet = 6
    _ = dealer.step(bet)
    bet = 8
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 23
    assert obs["max_raise"] == 0
    assert obs["call"] == 7
    bet = 7
    obs, *_ = dealer.step(bet)

    bet = -1
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 30
    assert not obs["active"].all()


def test_all_in_bet_size():
    config = clubs.configs.NO_LIMIT_HOLDEM_TWO_PLAYER

    dealer = clubs.poker.Dealer(**config)

    dealer.stacks[0] -= 150
    dealer.stacks[1] += 150

    obs = dealer.reset(reset_button=True, reset_stacks=False)

    bet = 100
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 52
    bet = 1000
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 400


def test_incomplete_raise():

    config = dict(**clubs.configs.NO_LIMIT_HOLDEM_SIX_PLAYER)

    dealer = clubs.poker.Dealer(**config)

    dealer.stacks[1] = dealer.stacks[1] - 190
    dealer.stacks[2] = dealer.stacks[2] + 190

    obs = dealer.reset(reset_button=True, reset_stacks=False)

    bet = -1
    _ = dealer.step(bet)
    _ = dealer.step(bet)
    _ = dealer.step(bet)
    bet = 8
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 11
    assert obs["call"] == 7
    assert obs["min_raise"] == 9
    assert obs["max_raise"] == 9

    bet = 9
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 20
    assert obs["call"] == 8
    assert obs["min_raise"] == 14  # call 8 + 6 largest valid raise

    bet = 8
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 28
    assert obs["call"] == 2
    assert obs["min_raise"] == 0
    assert obs["max_raise"] == 0


def test_pot_limit_bet_size():

    config = clubs.configs.POT_LIMIT_OMAHA_SIX_PLAYER

    dealer = clubs.poker.Dealer(**config)

    obs = dealer.reset(reset_button=True, reset_stacks=True)
    assert obs["min_raise"] == 4
    assert obs["max_raise"] == 7

    bet = 4
    obs, *_ = dealer.step(bet)
    assert obs["pot"] == 7
    assert obs["call"] == 4
    assert obs["min_raise"] == 6
    assert obs["max_raise"] == 15  # call + call + pot (2 * 4 + 7)

    bet = 4
    _ = dealer.step(bet)
    bet = 4
    _ = dealer.step(bet)
    bet = 4


def test_bet_rounding():

    config = clubs.configs.NO_LIMIT_HOLDEM_NINE_PLAYER

    dealer = clubs.poker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)

    bet = 1
    obs, *_ = dealer.step(bet)
    assert obs["street_commits"][3] == 0

    bet = 6
    obs, *_ = dealer.step(bet)
    assert obs["street_commits"][4] == 6

    bet = 3
    obs, *_ = dealer.step(bet)
    assert obs["street_commits"][5] == 0
    assert not obs["active"][5]

    bet = 4
    obs, *_ = dealer.step(bet)
    assert obs["street_commits"][6] == 6

    bet = 8
    obs, *_ = dealer.step(bet)
    assert obs["street_commits"][7] == 6

    bet = 9
    obs, *_ = dealer.step(bet)
    assert obs["street_commits"][8] == 10


def test_big_blind_raise_chance():

    config = clubs.configs.NO_LIMIT_HOLDEM_SIX_PLAYER

    dealer = clubs.poker.Dealer(**config)

    _ = dealer.reset(reset_button=True, reset_stacks=True)

    bet = 2  # all call
    for _ in range(5):
        obs, *_ = dealer.step(bet)

    assert obs["action"] == 2
    assert obs["call"] == 0
    assert obs["min_raise"] == 2
