import pytest

from nl_gym.poker.deck import Card, Evaluator


# def test_general():
#     # too few cards
#     evaluator = Evaluator(1, 13, 2, 5, 0)
#     hand1 = [Card.new('As'), Card.new('Ks')]
#     comm_cards = [Card.new('Ts')]
#     with pytest.raises(Exception):
#         evaluator.evaluate(hand1, comm_cards)

def test_1_card():
    # no community cards
    evaluator = Evaluator(1, 3, 1, 1, 0)
    hand1 = [Card.new('As')]
    hand2 = [Card.new('Ks')]
    assert evaluator.evaluate(hand1, []) < evaluator.evaluate(hand2, [])

    # 1 community card
    hand1 = [Card.new('As')]
    hand2 = [Card.new('Ks')]
    comm_cards = [Card.new('Qs')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    hand1 = [Card.new('Qs')]
    hand2 = [Card.new('Ks')]
    comm_cards = [Card.new('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) == evaluator.evaluate(hand2, comm_cards)

    # mandatory hole card
    evaluator = Evaluator(1, 3, 1, 1, 1)
    hand1 = [Card.new('Ks')]
    hand2 = [Card.new('Qs')]
    comm_cards = [Card.new('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 2 suits
    # 1 card for hand, no community cards
    evaluator = Evaluator(2, 3, 1, 1, 0)
    hand1 = [Card.new('Ah')]
    hand2 = [Card.new('As')]
    assert evaluator.evaluate(hand1, []) == evaluator.evaluate(hand2, [])


def test_2_card():
    # 1 suit
    evaluator = Evaluator(1, 3, 1, 2, 0)
    hand1 = [Card.new('Ks')]
    hand2 = [Card.new('Qs')]
    comm_cards = [Card.new('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 2 suits
    # pair > high card
    evaluator = Evaluator(2, 3, 1, 2, 0)
    hand1 = [Card.new('Qs')]
    hand2 = [Card.new('Ks')]
    comm_cards = [Card.new('Qh')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [Card.new('Ah')]
    hand2 = [Card.new('Ks')]
    comm_cards = [Card.new('Qs')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_3_card():
    # 1 suit
    # straight > high card
    evaluator = Evaluator(1, 13, 1, 3, 0)
    hand1 = [Card.new('Js')]
    hand2 = [Card.new('Qs')]
    comm_cards = [Card.new('9s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [Card.new('Ks')]
    hand2 = [Card.new('Qs')]
    comm_cards = [Card.new('5s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [Card.new('As')]
    comm_cards1 = [Card.new('Qs'), Card.new('Ks')]
    comm_cards2 = [Card.new('2s'), Card.new('3s')]
    assert evaluator.evaluate(
        hand, comm_cards1) < evaluator.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    evaluator = Evaluator(2, 13, 1, 3, 0)
    hand1 = [Card.new('Js')]
    hand2 = [Card.new('Jc')]
    comm_cards = [Card.new('9s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [Card.new('Jc')]
    hand2 = [Card.new('9c')]
    comm_cards = [Card.new('9s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > flush
    hand1 = [Card.new('7c')]
    hand2 = [Card.new('As')]
    comm_cards = [Card.new('7s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > high card
    hand1 = [Card.new('9s')]
    hand2 = [Card.new('Ac')]
    comm_cards = [Card.new('7s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > straight
    evaluator = Evaluator(4, 13, 1, 3, 0)
    hand1 = [Card.new('Js')]
    hand2 = [Card.new('Jc')]
    comm_cards = [Card.new('9s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [Card.new('Jc')]
    hand2 = [Card.new('9c')]
    comm_cards = [Card.new('9s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [Card.new('As')]
    hand2 = [Card.new('7c')]
    comm_cards = [Card.new('7s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [Card.new('7c')]
    hand2 = [Card.new('Ac')]
    comm_cards = [Card.new('7s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_4_card():
    # 1 suit
    # straight > high card
    evaluator = Evaluator(1, 13, 2, 4, 0)
    hand1 = [Card.new('Js'), Card.new('Ts')]
    hand2 = [Card.new('Qs'), Card.new('3s')]
    comm_cards = [Card.new('8s'), Card.new('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [Card.new('Ks'), Card.new('2s')]
    hand2 = [Card.new('Qs'), Card.new('3s')]
    comm_cards = [Card.new('5s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [Card.new('As')]
    comm_cards1 = [Card.new('Js'), Card.new('Qs'), Card.new('Ks')]
    comm_cards2 = [Card.new('2s'), Card.new('3s'), Card.new('4s')]
    assert evaluator.evaluate(
        hand, comm_cards1) < evaluator.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > two pair
    evaluator = Evaluator(2, 13, 2, 4, 0)
    hand1 = [Card.new('Js'), Card.new('Ts')]
    hand2 = [Card.new('8h'), Card.new('9h')]
    comm_cards = [Card.new('8s'), Card.new('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > straight
    hand1 = [Card.new('8s'), Card.new('9h')]
    hand2 = [Card.new('Js'), Card.new('Ts')]
    comm_cards = [Card.new('8h'), Card.new('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > flush
    hand1 = [Card.new('Js'), Card.new('Ts')]
    hand2 = [Card.new('4h'), Card.new('6h')]
    comm_cards = [Card.new('8h'), Card.new('9h')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [Card.new('8s'), Card.new('7s')]
    hand2 = [Card.new('Th'), Card.new('2s')]
    comm_cards = [Card.new('9s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [Card.new('8s'), Card.new('7h')]
    hand2 = [Card.new('Th'), Card.new('2s')]
    comm_cards = [Card.new('8h'), Card.new('9h')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 4 suits
    # four of a kind > straight flush
    evaluator = Evaluator(4, 13, 2, 4, 0)
    hand1 = [Card.new('As'), Card.new('Ac')]
    hand2 = [Card.new('Jh'), Card.new('Qh')]
    comm_cards = [Card.new('Kh'), Card.new('Ah'), Card.new('Ad')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight flush > three of a kind
    hand1 = [Card.new('Jh'), Card.new('Qh')]
    hand2 = [Card.new('As'), Card.new('Ac')]
    comm_cards = [Card.new('Kh'), Card.new('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # three of a kind > straight
    hand1 = [Card.new('As'), Card.new('Ac')]
    hand2 = [Card.new('Jd'), Card.new('Qd')]
    comm_cards = [Card.new('Kh'), Card.new('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [Card.new('Jd'), Card.new('Qd')]
    hand2 = [Card.new('As'), Card.new('Kc')]
    comm_cards = [Card.new('Kh'), Card.new('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [Card.new('9h'), Card.new('Qh')]
    hand2 = [Card.new('8s'), Card.new('7s')]
    comm_cards = [Card.new('9s'), Card.new('Qs')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [Card.new('8s'), Card.new('7s')]
    hand2 = [Card.new('9h'), Card.new('2h')]
    comm_cards = [Card.new('9s'), Card.new('Qs')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [Card.new('8s'), Card.new('7h')]
    hand2 = [Card.new('Ah'), Card.new('2s')]
    comm_cards = [Card.new('8h'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_5_card():
    # 1 suit
    # straight > high card
    evaluator = Evaluator(1, 13, 2, 5, 0)
    hand1 = [Card.new('Js'), Card.new('Ts')]
    hand2 = [Card.new('Qs'), Card.new('3s')]
    comm_cards = [Card.new('7s'), Card.new('8s'), Card.new('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [Card.new('Ks'), Card.new('2s')]
    hand2 = [Card.new('Qs'), Card.new('3s')]
    comm_cards = [Card.new('4s'), Card.new('5s'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [Card.new('As')]
    comm_cards1 = [Card.new('Ts'), Card.new(
        'Js'), Card.new('Qs'), Card.new('Ks')]
    comm_cards2 = [Card.new('2s'), Card.new(
        '3s'), Card.new('4s'), Card.new('5s')]
    assert evaluator.evaluate(
        hand, comm_cards1) < evaluator.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    evaluator = Evaluator(2, 13, 2, 5, 0)
    hand1 = [Card.new('Js'), Card.new('Ts')]
    hand2 = [Card.new('Jh'), Card.new('Th')]
    comm_cards = [Card.new('7s'), Card.new('8s'), Card.new('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [Card.new('Js'), Card.new('Ts')]
    hand2 = [Card.new('7h'), Card.new('8h')]
    comm_cards = [Card.new('7s'), Card.new('8s'), Card.new('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [Card.new('7h'), Card.new('8h')]
    hand2 = [Card.new('Js'), Card.new('Ts')]
    comm_cards = [Card.new('7s'), Card.new('8s'), Card.new('2s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [Card.new('8s'), Card.new('7s')]
    hand2 = [Card.new('Th'), Card.new('2s')]
    comm_cards = [Card.new('9s'), Card.new('Ts'), Card.new('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [Card.new('8s'), Card.new('7h')]
    hand2 = [Card.new('Th'), Card.new('2s')]
    comm_cards = [Card.new('8h'), Card.new('9h'), Card.new('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > four of a kind
    evaluator = Evaluator(4, 13, 2, 5, 0)
    hand1 = [Card.new('Jh'), Card.new('Qh')]
    hand2 = [Card.new('As'), Card.new('Ac')]
    comm_cards = [Card.new('Th'), Card.new(
        'Kh'), Card.new('Ah'), Card.new('Ad')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # four of a kind > full house
    hand1 = [Card.new('As'), Card.new('Ac')]
    hand2 = [Card.new('Kc'), Card.new('Kd')]
    comm_cards = [Card.new('Kh'), Card.new('Ah'), Card.new('Ad')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # full house > flush
    hand1 = [Card.new('Kc'), Card.new('Kd')]
    hand2 = [Card.new('Th'), Card.new('5h')]
    comm_cards = [Card.new('Kh'), Card.new(
        'Ah'), Card.new('Ad'), Card.new('2h')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > straight
    hand1 = [Card.new('Th'), Card.new('5h')]
    hand2 = [Card.new('Jd'), Card.new('Td')]
    comm_cards = [Card.new('Qh'), Card.new('Kh'), Card.new('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > three of a kind
    hand1 = [Card.new('Jd'), Card.new('Td')]
    hand2 = [Card.new('Qd'), Card.new('Qc')]
    comm_cards = [Card.new('Qh'), Card.new('Kh'), Card.new('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # three of a kind > two pair
    hand1 = [Card.new('Qd'), Card.new('Qc')]
    hand2 = [Card.new('Kd'), Card.new('Ad')]
    comm_cards = [Card.new('Qh'), Card.new('Kh'), Card.new('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > pair
    hand1 = [Card.new('9h'), Card.new('Qh')]
    hand2 = [Card.new('8s'), Card.new('7s')]
    comm_cards = [Card.new('9s'), Card.new('Qs'), Card.new('8d')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [Card.new('8s'), Card.new('7h')]
    hand2 = [Card.new('Ah'), Card.new('2s')]
    comm_cards = [Card.new('8h'), Card.new('9h'), Card.new('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)
