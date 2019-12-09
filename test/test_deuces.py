import pytest

from pyker import deuces


def test_1_card():
    # no community cards
    evaluator = deuces.Evaluator(1, 3, 1, 1, 0)
    hand1 = [deuces.Card('As')]
    hand2 = [deuces.Card('Ks')]
    assert evaluator.evaluate(hand1, []) < evaluator.evaluate(hand2, [])

    # 1 community card
    hand1 = [deuces.Card('As')]
    hand2 = [deuces.Card('Ks')]
    comm_cards = [deuces.Card('Qs')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    hand1 = [deuces.Card('Qs')]
    hand2 = [deuces.Card('Ks')]
    comm_cards = [deuces.Card('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) == evaluator.evaluate(hand2, comm_cards)

    # mandatory hole card
    evaluator = deuces.Evaluator(1, 3, 1, 1, 1)
    hand1 = [deuces.Card('Ks')]
    hand2 = [deuces.Card('Qs')]
    comm_cards = [deuces.Card('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 2 suits
    # 1 card for hand, no community cards
    evaluator = deuces.Evaluator(2, 3, 1, 1, 0)
    hand1 = [deuces.Card('Ah')]
    hand2 = [deuces.Card('As')]
    assert evaluator.evaluate(hand1, []) == evaluator.evaluate(hand2, [])


def test_2_card():
    # 1 suit
    evaluator = deuces.Evaluator(1, 3, 1, 2, 0)
    hand1 = [deuces.Card('Ks')]
    hand2 = [deuces.Card('Qs')]
    comm_cards = [deuces.Card('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 2 suits
    # pair > high card
    evaluator = deuces.Evaluator(2, 3, 1, 2, 0)
    hand1 = [deuces.Card('Qs')]
    hand2 = [deuces.Card('Ks')]
    comm_cards = [deuces.Card('Qh')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [deuces.Card('Ah')]
    hand2 = [deuces.Card('Ks')]
    comm_cards = [deuces.Card('Qs')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_3_card():
    # 1 suit
    # straight > high card
    evaluator = deuces.Evaluator(1, 13, 1, 3, 0)
    hand1 = [deuces.Card('Js')]
    hand2 = [deuces.Card('Qs')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [deuces.Card('Ks')]
    hand2 = [deuces.Card('Qs')]
    comm_cards = [deuces.Card('5s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [deuces.Card('As')]
    comm_cards1 = [deuces.Card('Qs'), deuces.Card('Ks')]
    comm_cards2 = [deuces.Card('2s'), deuces.Card('3s')]
    assert evaluator.evaluate(
        hand, comm_cards1) < evaluator.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    evaluator = deuces.Evaluator(2, 13, 1, 3, 0)
    hand1 = [deuces.Card('Js')]
    hand2 = [deuces.Card('Jc')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [deuces.Card('Jc')]
    hand2 = [deuces.Card('9c')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > flush
    hand1 = [deuces.Card('7c')]
    hand2 = [deuces.Card('As')]
    comm_cards = [deuces.Card('7s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > high card
    hand1 = [deuces.Card('9s')]
    hand2 = [deuces.Card('Ac')]
    comm_cards = [deuces.Card('7s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > straight
    evaluator = deuces.Evaluator(4, 13, 1, 3, 0)
    hand1 = [deuces.Card('Js')]
    hand2 = [deuces.Card('Jc')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [deuces.Card('Jc')]
    hand2 = [deuces.Card('9c')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [deuces.Card('As')]
    hand2 = [deuces.Card('7c')]
    comm_cards = [deuces.Card('7s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [deuces.Card('7c')]
    hand2 = [deuces.Card('Ac')]
    comm_cards = [deuces.Card('7s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_4_card():
    # 1 suit
    # straight > high card
    evaluator = deuces.Evaluator(1, 13, 2, 4, 0)
    hand1 = [deuces.Card('Js'), deuces.Card('Ts')]
    hand2 = [deuces.Card('Qs'), deuces.Card('3s')]
    comm_cards = [deuces.Card('8s'), deuces.Card('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [deuces.Card('Ks'), deuces.Card('2s')]
    hand2 = [deuces.Card('Qs'), deuces.Card('3s')]
    comm_cards = [deuces.Card('5s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [deuces.Card('As')]
    comm_cards1 = [deuces.Card('Js'), deuces.Card('Qs'), deuces.Card('Ks')]
    comm_cards2 = [deuces.Card('2s'), deuces.Card('3s'), deuces.Card('4s')]
    assert evaluator.evaluate(
        hand, comm_cards1) < evaluator.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > two pair
    evaluator = deuces.Evaluator(2, 13, 2, 4, 0)
    hand1 = [deuces.Card('Js'), deuces.Card('Ts')]
    hand2 = [deuces.Card('8h'), deuces.Card('9h')]
    comm_cards = [deuces.Card('8s'), deuces.Card('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > straight
    hand1 = [deuces.Card('8s'), deuces.Card('9h')]
    hand2 = [deuces.Card('Js'), deuces.Card('Ts')]
    comm_cards = [deuces.Card('8h'), deuces.Card('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > flush
    hand1 = [deuces.Card('Js'), deuces.Card('Ts')]
    hand2 = [deuces.Card('4h'), deuces.Card('6h')]
    comm_cards = [deuces.Card('8h'), deuces.Card('9h')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [deuces.Card('8s'), deuces.Card('7s')]
    hand2 = [deuces.Card('Th'), deuces.Card('2s')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [deuces.Card('8s'), deuces.Card('7h')]
    hand2 = [deuces.Card('Th'), deuces.Card('2s')]
    comm_cards = [deuces.Card('8h'), deuces.Card('9h')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 4 suits
    # four of a kind > straight flush
    evaluator = deuces.Evaluator(4, 13, 2, 4, 0)
    hand1 = [deuces.Card('As'), deuces.Card('Ac')]
    hand2 = [deuces.Card('Jh'), deuces.Card('Qh')]
    comm_cards = [deuces.Card('Kh'), deuces.Card('Ah'), deuces.Card('Ad')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight flush > three of a kind
    hand1 = [deuces.Card('Jh'), deuces.Card('Qh')]
    hand2 = [deuces.Card('As'), deuces.Card('Ac')]
    comm_cards = [deuces.Card('Kh'), deuces.Card('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # three of a kind > straight
    hand1 = [deuces.Card('As'), deuces.Card('Ac')]
    hand2 = [deuces.Card('Jd'), deuces.Card('Qd')]
    comm_cards = [deuces.Card('Kh'), deuces.Card('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [deuces.Card('Jd'), deuces.Card('Qd')]
    hand2 = [deuces.Card('As'), deuces.Card('Kc')]
    comm_cards = [deuces.Card('Kh'), deuces.Card('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [deuces.Card('9h'), deuces.Card('Qh')]
    hand2 = [deuces.Card('8s'), deuces.Card('7s')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Qs')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [deuces.Card('8s'), deuces.Card('7s')]
    hand2 = [deuces.Card('9h'), deuces.Card('2h')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Qs')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [deuces.Card('8s'), deuces.Card('7h')]
    hand2 = [deuces.Card('Ah'), deuces.Card('2s')]
    comm_cards = [deuces.Card('8h'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_5_card():
    # 1 suit
    # straight > high card
    evaluator = deuces.Evaluator(1, 13, 2, 5, 0)
    hand1 = [deuces.Card('Js'), deuces.Card('Ts')]
    hand2 = [deuces.Card('Qs'), deuces.Card('3s')]
    comm_cards = [deuces.Card('7s'), deuces.Card('8s'), deuces.Card('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [deuces.Card('Ks'), deuces.Card('2s')]
    hand2 = [deuces.Card('Qs'), deuces.Card('3s')]
    comm_cards = [deuces.Card('4s'), deuces.Card('5s'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [deuces.Card('As')]
    comm_cards1 = [deuces.Card('Ts'), deuces.Card(
        'Js'), deuces.Card('Qs'), deuces.Card('Ks')]
    comm_cards2 = [deuces.Card('2s'), deuces.Card(
        '3s'), deuces.Card('4s'), deuces.Card('5s')]
    assert evaluator.evaluate(
        hand, comm_cards1) < evaluator.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    evaluator = deuces.Evaluator(2, 13, 2, 5, 0)
    hand1 = [deuces.Card('Js'), deuces.Card('Ts')]
    hand2 = [deuces.Card('Jh'), deuces.Card('Th')]
    comm_cards = [deuces.Card('7s'), deuces.Card('8s'), deuces.Card('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [deuces.Card('Js'), deuces.Card('Ts')]
    hand2 = [deuces.Card('7h'), deuces.Card('8h')]
    comm_cards = [deuces.Card('7s'), deuces.Card('8s'), deuces.Card('9s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [deuces.Card('7h'), deuces.Card('8h')]
    hand2 = [deuces.Card('Js'), deuces.Card('Ts')]
    comm_cards = [deuces.Card('7s'), deuces.Card('8s'), deuces.Card('2s')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [deuces.Card('8s'), deuces.Card('7s')]
    hand2 = [deuces.Card('Th'), deuces.Card('2s')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Ts'), deuces.Card('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [deuces.Card('8s'), deuces.Card('7h')]
    hand2 = [deuces.Card('Th'), deuces.Card('2s')]
    comm_cards = [deuces.Card('8h'), deuces.Card('9h'), deuces.Card('As')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > four of a kind
    evaluator = deuces.Evaluator(4, 13, 2, 5, 0)
    hand1 = [deuces.Card('Jh'), deuces.Card('Qh')]
    hand2 = [deuces.Card('As'), deuces.Card('Ac')]
    comm_cards = [deuces.Card('Th'), deuces.Card(
        'Kh'), deuces.Card('Ah'), deuces.Card('Ad')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # four of a kind > full house
    hand1 = [deuces.Card('As'), deuces.Card('Ac')]
    hand2 = [deuces.Card('Kc'), deuces.Card('Kd')]
    comm_cards = [deuces.Card('Kh'), deuces.Card('Ah'), deuces.Card('Ad')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # full house > flush
    hand1 = [deuces.Card('Kc'), deuces.Card('Kd')]
    hand2 = [deuces.Card('Th'), deuces.Card('5h')]
    comm_cards = [deuces.Card('Kh'), deuces.Card(
        'Ah'), deuces.Card('Ad'), deuces.Card('2h')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > straight
    hand1 = [deuces.Card('Th'), deuces.Card('5h')]
    hand2 = [deuces.Card('Jd'), deuces.Card('Td')]
    comm_cards = [deuces.Card('Qh'), deuces.Card('Kh'), deuces.Card('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > three of a kind
    hand1 = [deuces.Card('Jd'), deuces.Card('Td')]
    hand2 = [deuces.Card('Qd'), deuces.Card('Qc')]
    comm_cards = [deuces.Card('Qh'), deuces.Card('Kh'), deuces.Card('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # three of a kind > two pair
    hand1 = [deuces.Card('Qd'), deuces.Card('Qc')]
    hand2 = [deuces.Card('Kd'), deuces.Card('Ad')]
    comm_cards = [deuces.Card('Qh'), deuces.Card('Kh'), deuces.Card('Ah')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > pair
    hand1 = [deuces.Card('9h'), deuces.Card('Qh')]
    hand2 = [deuces.Card('8s'), deuces.Card('7s')]
    comm_cards = [deuces.Card('9s'), deuces.Card('Qs'), deuces.Card('8d')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [deuces.Card('8s'), deuces.Card('7h')]
    hand2 = [deuces.Card('Ah'), deuces.Card('2s')]
    comm_cards = [deuces.Card('8h'), deuces.Card('9h'), deuces.Card('Ts')]
    assert evaluator.evaluate(
        hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

