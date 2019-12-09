import pytest

from pyker.deuces import card, evaluator


def test_1_card():
    # no community cards
    hand_eval = evaluator.Evaluator(1, 3, 1, 1, 0)
    hand1 = [card.Card('As')]
    hand2 = [card.Card('Ks')]
    assert hand_eval.evaluate(hand1, []) < hand_eval.evaluate(hand2, [])

    # 1 community card
    hand1 = [card.Card('As')]
    hand2 = [card.Card('Ks')]
    comm_cards = [card.Card('Qs')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    hand1 = [card.Card('Qs')]
    hand2 = [card.Card('Ks')]
    comm_cards = [card.Card('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) == hand_eval.evaluate(hand2, comm_cards)

    # mandatory hole card
    hand_eval = evaluator.Evaluator(1, 3, 1, 1, 1)
    hand1 = [card.Card('Ks')]
    hand2 = [card.Card('Qs')]
    comm_cards = [card.Card('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 2 suits
    # 1 card for hand, no community cards
    hand_eval = evaluator.Evaluator(2, 3, 1, 1, 0)
    hand1 = [card.Card('Ah')]
    hand2 = [card.Card('As')]
    assert hand_eval.evaluate(hand1, []) == hand_eval.evaluate(hand2, [])


def test_2_card():
    # 1 suit
    hand_eval = evaluator.Evaluator(1, 3, 1, 2, 0)
    hand1 = [card.Card('Ks')]
    hand2 = [card.Card('Qs')]
    comm_cards = [card.Card('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 2 suits
    # pair > high card
    hand_eval = evaluator.Evaluator(2, 3, 1, 2, 0)
    hand1 = [card.Card('Qs')]
    hand2 = [card.Card('Ks')]
    comm_cards = [card.Card('Qh')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [card.Card('Ah')]
    hand2 = [card.Card('Ks')]
    comm_cards = [card.Card('Qs')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)


def test_3_card():
    # 1 suit
    # straight > high card
    hand_eval = evaluator.Evaluator(1, 13, 1, 3, 0)
    hand1 = [card.Card('Js')]
    hand2 = [card.Card('Qs')]
    comm_cards = [card.Card('9s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [card.Card('Ks')]
    hand2 = [card.Card('Qs')]
    comm_cards = [card.Card('5s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [card.Card('As')]
    comm_cards1 = [card.Card('Qs'), card.Card('Ks')]
    comm_cards2 = [card.Card('2s'), card.Card('3s')]
    assert hand_eval.evaluate(
        hand, comm_cards1) < hand_eval.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    hand_eval = evaluator.Evaluator(2, 13, 1, 3, 0)
    hand1 = [card.Card('Js')]
    hand2 = [card.Card('Jc')]
    comm_cards = [card.Card('9s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [card.Card('Jc')]
    hand2 = [card.Card('9c')]
    comm_cards = [card.Card('9s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > flush
    hand1 = [card.Card('7c')]
    hand2 = [card.Card('As')]
    comm_cards = [card.Card('7s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > high card
    hand1 = [card.Card('9s')]
    hand2 = [card.Card('Ac')]
    comm_cards = [card.Card('7s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > straight
    hand_eval = evaluator.Evaluator(4, 13, 1, 3, 0)
    hand1 = [card.Card('Js')]
    hand2 = [card.Card('Jc')]
    comm_cards = [card.Card('9s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [card.Card('Jc')]
    hand2 = [card.Card('9c')]
    comm_cards = [card.Card('9s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [card.Card('As')]
    hand2 = [card.Card('7c')]
    comm_cards = [card.Card('7s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card('7c')]
    hand2 = [card.Card('Ac')]
    comm_cards = [card.Card('7s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)


def test_4_card():
    # 1 suit
    # straight > high card
    hand_eval = evaluator.Evaluator(1, 13, 2, 4, 0)
    hand1 = [card.Card('Js'), card.Card('Ts')]
    hand2 = [card.Card('Qs'), card.Card('3s')]
    comm_cards = [card.Card('8s'), card.Card('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [card.Card('Ks'), card.Card('2s')]
    hand2 = [card.Card('Qs'), card.Card('3s')]
    comm_cards = [card.Card('5s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [card.Card('As')]
    comm_cards1 = [card.Card('Js'), card.Card('Qs'), card.Card('Ks')]
    comm_cards2 = [card.Card('2s'), card.Card('3s'), card.Card('4s')]
    assert hand_eval.evaluate(
        hand, comm_cards1) < hand_eval.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > two pair
    hand_eval = evaluator.Evaluator(2, 13, 2, 4, 0)
    hand1 = [card.Card('Js'), card.Card('Ts')]
    hand2 = [card.Card('8h'), card.Card('9h')]
    comm_cards = [card.Card('8s'), card.Card('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # two pair > straight
    hand1 = [card.Card('8s'), card.Card('9h')]
    hand2 = [card.Card('Js'), card.Card('Ts')]
    comm_cards = [card.Card('8h'), card.Card('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > flush
    hand1 = [card.Card('Js'), card.Card('Ts')]
    hand2 = [card.Card('4h'), card.Card('6h')]
    comm_cards = [card.Card('8h'), card.Card('9h')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [card.Card('8s'), card.Card('7s')]
    hand2 = [card.Card('Th'), card.Card('2s')]
    comm_cards = [card.Card('9s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card('8s'), card.Card('7h')]
    hand2 = [card.Card('Th'), card.Card('2s')]
    comm_cards = [card.Card('8h'), card.Card('9h')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 4 suits
    # four of a kind > straight flush
    hand_eval = evaluator.Evaluator(4, 13, 2, 4, 0)
    hand1 = [card.Card('As'), card.Card('Ac')]
    hand2 = [card.Card('Jh'), card.Card('Qh')]
    comm_cards = [card.Card('Kh'), card.Card('Ah'), card.Card('Ad')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight flush > three of a kind
    hand1 = [card.Card('Jh'), card.Card('Qh')]
    hand2 = [card.Card('As'), card.Card('Ac')]
    comm_cards = [card.Card('Kh'), card.Card('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # three of a kind > straight
    hand1 = [card.Card('As'), card.Card('Ac')]
    hand2 = [card.Card('Jd'), card.Card('Qd')]
    comm_cards = [card.Card('Kh'), card.Card('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [card.Card('Jd'), card.Card('Qd')]
    hand2 = [card.Card('As'), card.Card('Kc')]
    comm_cards = [card.Card('Kh'), card.Card('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [card.Card('9h'), card.Card('Qh')]
    hand2 = [card.Card('8s'), card.Card('7s')]
    comm_cards = [card.Card('9s'), card.Card('Qs')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [card.Card('8s'), card.Card('7s')]
    hand2 = [card.Card('9h'), card.Card('2h')]
    comm_cards = [card.Card('9s'), card.Card('Qs')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card('8s'), card.Card('7h')]
    hand2 = [card.Card('Ah'), card.Card('2s')]
    comm_cards = [card.Card('8h'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)


def test_5_card():
    # 1 suit
    # straight > high card
    hand_eval = evaluator.Evaluator(1, 13, 2, 5, 0)
    hand1 = [card.Card('Js'), card.Card('Ts')]
    hand2 = [card.Card('Qs'), card.Card('3s')]
    comm_cards = [card.Card('7s'), card.Card('8s'), card.Card('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [card.Card('Ks'), card.Card('2s')]
    hand2 = [card.Card('Qs'), card.Card('3s')]
    comm_cards = [card.Card('4s'), card.Card('5s'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [card.Card('As')]
    comm_cards1 = [card.Card('Ts'), card.Card(
        'Js'), card.Card('Qs'), card.Card('Ks')]
    comm_cards2 = [card.Card('2s'), card.Card(
        '3s'), card.Card('4s'), card.Card('5s')]
    assert hand_eval.evaluate(
        hand, comm_cards1) < hand_eval.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    hand_eval = evaluator.Evaluator(2, 13, 2, 5, 0)
    hand1 = [card.Card('Js'), card.Card('Ts')]
    hand2 = [card.Card('Jh'), card.Card('Th')]
    comm_cards = [card.Card('7s'), card.Card('8s'), card.Card('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [card.Card('Js'), card.Card('Ts')]
    hand2 = [card.Card('7h'), card.Card('8h')]
    comm_cards = [card.Card('7s'), card.Card('8s'), card.Card('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [card.Card('7h'), card.Card('8h')]
    hand2 = [card.Card('Js'), card.Card('Ts')]
    comm_cards = [card.Card('7s'), card.Card('8s'), card.Card('2s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [card.Card('8s'), card.Card('7s')]
    hand2 = [card.Card('Th'), card.Card('2s')]
    comm_cards = [card.Card('9s'), card.Card('Ts'), card.Card('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card('8s'), card.Card('7h')]
    hand2 = [card.Card('Th'), card.Card('2s')]
    comm_cards = [card.Card('8h'), card.Card('9h'), card.Card('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > four of a kind
    hand_eval = evaluator.Evaluator(4, 13, 2, 5, 0)
    hand1 = [card.Card('Jh'), card.Card('Qh')]
    hand2 = [card.Card('As'), card.Card('Ac')]
    comm_cards = [card.Card('Th'), card.Card(
        'Kh'), card.Card('Ah'), card.Card('Ad')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # four of a kind > full house
    hand1 = [card.Card('As'), card.Card('Ac')]
    hand2 = [card.Card('Kc'), card.Card('Kd')]
    comm_cards = [card.Card('Kh'), card.Card('Ah'), card.Card('Ad')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # full house > flush
    hand1 = [card.Card('Kc'), card.Card('Kd')]
    hand2 = [card.Card('Th'), card.Card('5h')]
    comm_cards = [card.Card('Kh'), card.Card(
        'Ah'), card.Card('Ad'), card.Card('2h')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > straight
    hand1 = [card.Card('Th'), card.Card('5h')]
    hand2 = [card.Card('Jd'), card.Card('Td')]
    comm_cards = [card.Card('Qh'), card.Card('Kh'), card.Card('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > three of a kind
    hand1 = [card.Card('Jd'), card.Card('Td')]
    hand2 = [card.Card('Qd'), card.Card('Qc')]
    comm_cards = [card.Card('Qh'), card.Card('Kh'), card.Card('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # three of a kind > two pair
    hand1 = [card.Card('Qd'), card.Card('Qc')]
    hand2 = [card.Card('Kd'), card.Card('Ad')]
    comm_cards = [card.Card('Qh'), card.Card('Kh'), card.Card('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # two pair > pair
    hand1 = [card.Card('9h'), card.Card('Qh')]
    hand2 = [card.Card('8s'), card.Card('7s')]
    comm_cards = [card.Card('9s'), card.Card('Qs'), card.Card('8d')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card('8s'), card.Card('7h')]
    hand2 = [card.Card('Ah'), card.Card('2s')]
    comm_cards = [card.Card('8h'), card.Card('9h'), card.Card('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)
