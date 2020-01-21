import pyker


def test_split_pot():

    config = pyker.configs.NOLIMIT_HOLDEM_9P_ENV

    dealer = pyker.Dealer(**config)

    hands = [
        ['6c', '8s'], ['Ac', 'Ad'], ['Kd', '2h'], ['Th', '9c'], ['Js', 'Jc'],
        ['6h', '8d'], ['5c', '7d'], ['Qh', '2c'], ['3d', '4s']]
    comm_cards = ['4d', '5h', '7c', 'Ac', 'Kh']
    top_cards = [card for hand in hands for card in hand] + comm_cards
    dealer.deck = dealer.deck.trick(top_cards)

    obs = dealer.reset(reset_button=True, reset_stacks=True)

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
        obs, payouts, done, _ = dealer.step(action)
        if all(done):
            break
    assert not sum(payouts)
    test_payouts = [12, -9, -2, 0, -5, 13, -9, 0, 0]
    assert all(payout == test_payout 
    for payout, test_payout in zip(payouts, test_payouts))


def test_all_in():

    config = pyker.configs.NOLIMIT_HOLDEM_9P_ENV

    dealer = pyker.Dealer(**config)

    hands = [
        ['6c', '8s'], ['Ac', 'Ad'], ['Kd', '2h'], ['Th', '9c'], ['Js', 'Jc'],
        ['6h', '8d'], ['5c', '7d'], ['Qh', '2c'], ['3d', '4s']]
    comm_cards = ['4d', '5h', '7c', 'Ac', 'Kh']
    top_cards = [card for hand in hands for card in hand] + comm_cards
    dealer.deck = dealer.deck.trick(top_cards)

    dealer.stacks[0] = dealer.stacks[0] - 180
    dealer.stacks[1] = dealer.stacks[1] + 180

    obs = dealer.reset(reset_button=True, reset_stacks=False)

    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 50}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 20}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 49}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    obs, *_ = dealer.step(action)

    assert obs['pot'] == 122

    while True:
        action = {'fold': 0, 'bet': 0}
        obs, payouts, done, _ = dealer.step(action)
        if all(done):
            break

    assert not sum(payouts)
    test_payouts = [42, 10, -2, 0, -50, 0, 0, 0, 0]
    assert all(payout == test_payout
               for payout, test_payout in zip(payouts, test_payouts))


def test_all_in_split_pot():

    config = pyker.configs.NOLIMIT_HOLDEM_9P_ENV

    dealer = pyker.Dealer(**config)

    hands = [
        ['6c', '8s'], ['Ac', 'Ad'], ['Kd', '2h'], ['Th', '9c'], ['6d', '8h'],
        ['6h', '8d'], ['5c', '7d'], ['Qh', '2c'], ['3d', '4s']]
    comm_cards = ['4d', '5h', '7c', 'Ac', 'Kh']
    top_cards = [card for hand in hands for card in hand] + comm_cards
    dealer.deck = dealer.deck.trick(top_cards)

    dealer.stacks[0] = dealer.stacks[0] - 180
    dealer.stacks[1] = dealer.stacks[1] + 180
    dealer.stacks[5] = dealer.stacks[5] - 165
    dealer.stacks[7] = dealer.stacks[7] + 165

    obs = dealer.reset(reset_button=True, reset_stacks=False)

    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 45}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 35}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 20}
    _ = dealer.step(action)
    action = {'fold': 0, 'bet': 44}
    _ = dealer.step(action)
    action = {'fold': 1, 'bet': 0}
    obs, *_ = dealer.step(action)

    assert obs['pot'] == 147

    while True:
        action = {'fold': 0, 'bet': 0}
        obs, payouts, done, _ = dealer.step(action)
        if all(done):
            break

    # main pot 82 (27 per person, 1 remainder)
    # first side pot 45 (22 per person, 1 remainder)
    # second side pot 20
    # [27-20, -45, -2, 0, 27+22+20+2-45, 27+22-35, 0, 0, 0]

    assert not sum(payouts)
    test_payouts = [7, -45, -2, 0, 26, 14, 0, 0, 0]
    assert all(payout == test_payout
               for payout, test_payout in zip(payouts, test_payouts))
