import pytest

from pyker.deuces import card, evaluator


def test_1_card():
    # no community cards
    hand_eval = evaluator.Evaluator(1, 3, 1, 1, 0)
    hand1 = [card.Card.new('As')]
    hand2 = [card.Card.new('Ks')]
    assert hand_eval.evaluate(hand1, []) < hand_eval.evaluate(hand2, [])

    # 1 community card
    hand1 = [card.Card.new('As')]
    hand2 = [card.Card.new('Ks')]
    comm_cards = [card.Card.new('Qs')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    hand1 = [card.Card.new('Qs')]
    hand2 = [card.Card.new('Ks')]
    comm_cards = [card.Card.new('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) == hand_eval.evaluate(hand2, comm_cards)

    # mandatory hole card
    hand_eval = evaluator.Evaluator(1, 3, 1, 1, 1)
    hand1 = [card.Card.new('Ks')]
    hand2 = [card.Card.new('Qs')]
    comm_cards = [card.Card.new('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 2 suits
    # 1 card for hand, no community cards
    hand_eval = evaluator.Evaluator(2, 3, 1, 1, 0)
    hand1 = [card.Card.new('Ah')]
    hand2 = [card.Card.new('As')]
    assert hand_eval.evaluate(hand1, []) == hand_eval.evaluate(hand2, [])


def test_2_card():
    # 1 suit
    hand_eval = evaluator.Evaluator(1, 3, 1, 2, 0)
    hand1 = [card.Card.new('Ks')]
    hand2 = [card.Card.new('Qs')]
    comm_cards = [card.Card.new('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 2 suits
    # pair > high card
    hand_eval = evaluator.Evaluator(2, 3, 1, 2, 0)
    hand1 = [card.Card.new('Qs')]
    hand2 = [card.Card.new('Ks')]
    comm_cards = [card.Card.new('Qh')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [card.Card.new('Ah')]
    hand2 = [card.Card.new('Ks')]
    comm_cards = [card.Card.new('Qs')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)


def test_3_card():
    # 1 suit
    # straight > high card
    hand_eval = evaluator.Evaluator(1, 13, 1, 3, 0)
    hand1 = [card.Card.new('Js')]
    hand2 = [card.Card.new('Qs')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [card.Card.new('Ks')]
    hand2 = [card.Card.new('Qs')]
    comm_cards = [card.Card.new('5s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [card.Card.new('As')]
    comm_cards1 = [card.Card.new('Qs'), card.Card.new('Ks')]
    comm_cards2 = [card.Card.new('2s'), card.Card.new('3s')]
    assert hand_eval.evaluate(
        hand, comm_cards1) < hand_eval.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    hand_eval = evaluator.Evaluator(2, 13, 1, 3, 0)
    hand1 = [card.Card.new('Js')]
    hand2 = [card.Card.new('Jc')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [card.Card.new('Jc')]
    hand2 = [card.Card.new('9c')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > flush
    hand1 = [card.Card.new('7c')]
    hand2 = [card.Card.new('As')]
    comm_cards = [card.Card.new('7s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > high card
    hand1 = [card.Card.new('9s')]
    hand2 = [card.Card.new('Ac')]
    comm_cards = [card.Card.new('7s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > straight
    hand_eval = evaluator.Evaluator(4, 13, 1, 3, 0)
    hand1 = [card.Card.new('Js')]
    hand2 = [card.Card.new('Jc')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [card.Card.new('Jc')]
    hand2 = [card.Card.new('9c')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [card.Card.new('As')]
    hand2 = [card.Card.new('7c')]
    comm_cards = [card.Card.new('7s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card.new('7c')]
    hand2 = [card.Card.new('Ac')]
    comm_cards = [card.Card.new('7s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)


def test_4_card():
    # 1 suit
    # straight > high card
    hand_eval = evaluator.Evaluator(1, 13, 2, 4, 0)
    hand1 = [card.Card.new('Js'), card.Card.new('Ts')]
    hand2 = [card.Card.new('Qs'), card.Card.new('3s')]
    comm_cards = [card.Card.new('8s'), card.Card.new('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [card.Card.new('Ks'), card.Card.new('2s')]
    hand2 = [card.Card.new('Qs'), card.Card.new('3s')]
    comm_cards = [card.Card.new('5s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [card.Card.new('As')]
    comm_cards1 = [card.Card.new('Js'), card.Card.new('Qs'), card.Card.new('Ks')]
    comm_cards2 = [card.Card.new('2s'), card.Card.new('3s'), card.Card.new('4s')]
    assert hand_eval.evaluate(
        hand, comm_cards1) < hand_eval.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > two pair
    hand_eval = evaluator.Evaluator(2, 13, 2, 4, 0)
    hand1 = [card.Card.new('Js'), card.Card.new('Ts')]
    hand2 = [card.Card.new('8h'), card.Card.new('9h')]
    comm_cards = [card.Card.new('8s'), card.Card.new('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # two pair > straight
    hand1 = [card.Card.new('8s'), card.Card.new('9h')]
    hand2 = [card.Card.new('Js'), card.Card.new('Ts')]
    comm_cards = [card.Card.new('8h'), card.Card.new('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > flush
    hand1 = [card.Card.new('Js'), card.Card.new('Ts')]
    hand2 = [card.Card.new('4h'), card.Card.new('6h')]
    comm_cards = [card.Card.new('8h'), card.Card.new('9h')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [card.Card.new('8s'), card.Card.new('7s')]
    hand2 = [card.Card.new('Th'), card.Card.new('2s')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card.new('8s'), card.Card.new('7h')]
    hand2 = [card.Card.new('Th'), card.Card.new('2s')]
    comm_cards = [card.Card.new('8h'), card.Card.new('9h')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 4 suits
    # four of a kind > straight flush
    hand_eval = evaluator.Evaluator(4, 13, 2, 4, 0)
    hand1 = [card.Card.new('As'), card.Card.new('Ac')]
    hand2 = [card.Card.new('Jh'), card.Card.new('Qh')]
    comm_cards = [card.Card.new('Kh'), card.Card.new('Ah'), card.Card.new('Ad')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight flush > three of a kind
    hand1 = [card.Card.new('Jh'), card.Card.new('Qh')]
    hand2 = [card.Card.new('As'), card.Card.new('Ac')]
    comm_cards = [card.Card.new('Kh'), card.Card.new('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # three of a kind > straight
    hand1 = [card.Card.new('As'), card.Card.new('Ac')]
    hand2 = [card.Card.new('Jd'), card.Card.new('Qd')]
    comm_cards = [card.Card.new('Kh'), card.Card.new('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [card.Card.new('Jd'), card.Card.new('Qd')]
    hand2 = [card.Card.new('As'), card.Card.new('Kc')]
    comm_cards = [card.Card.new('Kh'), card.Card.new('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [card.Card.new('9h'), card.Card.new('Qh')]
    hand2 = [card.Card.new('8s'), card.Card.new('7s')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Qs')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [card.Card.new('8s'), card.Card.new('7s')]
    hand2 = [card.Card.new('9h'), card.Card.new('2h')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Qs')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card.new('8s'), card.Card.new('7h')]
    hand2 = [card.Card.new('Ah'), card.Card.new('2s')]
    comm_cards = [card.Card.new('8h'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)


def test_5_card():
    # 1 suit
    # straight > high card
    hand_eval = evaluator.Evaluator(1, 13, 2, 5, 0)
    hand1 = [card.Card.new('Js'), card.Card.new('Ts')]
    hand2 = [card.Card.new('Qs'), card.Card.new('3s')]
    comm_cards = [card.Card.new('7s'), card.Card.new('8s'), card.Card.new('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [card.Card.new('Ks'), card.Card.new('2s')]
    hand2 = [card.Card.new('Qs'), card.Card.new('3s')]
    comm_cards = [card.Card.new('4s'), card.Card.new('5s'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [card.Card.new('As')]
    comm_cards1 = [card.Card.new('Ts'), card.Card.new(
        'Js'), card.Card.new('Qs'), card.Card.new('Ks')]
    comm_cards2 = [card.Card.new('2s'), card.Card.new(
        '3s'), card.Card.new('4s'), card.Card.new('5s')]
    assert hand_eval.evaluate(
        hand, comm_cards1) < hand_eval.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    hand_eval = evaluator.Evaluator(2, 13, 2, 5, 0)
    hand1 = [card.Card.new('Js'), card.Card.new('Ts')]
    hand2 = [card.Card.new('Jh'), card.Card.new('Th')]
    comm_cards = [card.Card.new('7s'), card.Card.new('8s'), card.Card.new('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [card.Card.new('Js'), card.Card.new('Ts')]
    hand2 = [card.Card.new('7h'), card.Card.new('8h')]
    comm_cards = [card.Card.new('7s'), card.Card.new('8s'), card.Card.new('9s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [card.Card.new('7h'), card.Card.new('8h')]
    hand2 = [card.Card.new('Js'), card.Card.new('Ts')]
    comm_cards = [card.Card.new('7s'), card.Card.new('8s'), card.Card.new('2s')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [card.Card.new('8s'), card.Card.new('7s')]
    hand2 = [card.Card.new('Th'), card.Card.new('2s')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Ts'), card.Card.new('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card.new('8s'), card.Card.new('7h')]
    hand2 = [card.Card.new('Th'), card.Card.new('2s')]
    comm_cards = [card.Card.new('8h'), card.Card.new('9h'), card.Card.new('As')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > four of a kind
    hand_eval = evaluator.Evaluator(4, 13, 2, 5, 0)
    hand1 = [card.Card.new('Jh'), card.Card.new('Qh')]
    hand2 = [card.Card.new('As'), card.Card.new('Ac')]
    comm_cards = [card.Card.new('Th'), card.Card.new(
        'Kh'), card.Card.new('Ah'), card.Card.new('Ad')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # four of a kind > full house
    hand1 = [card.Card.new('As'), card.Card.new('Ac')]
    hand2 = [card.Card.new('Kc'), card.Card.new('Kd')]
    comm_cards = [card.Card.new('Kh'), card.Card.new('Ah'), card.Card.new('Ad')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # full house > flush
    hand1 = [card.Card.new('Kc'), card.Card.new('Kd')]
    hand2 = [card.Card.new('Th'), card.Card.new('5h')]
    comm_cards = [card.Card.new('Kh'), card.Card.new(
        'Ah'), card.Card.new('Ad'), card.Card.new('2h')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # flush > straight
    hand1 = [card.Card.new('Th'), card.Card.new('5h')]
    hand2 = [card.Card.new('Jd'), card.Card.new('Td')]
    comm_cards = [card.Card.new('Qh'), card.Card.new('Kh'), card.Card.new('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # straight > three of a kind
    hand1 = [card.Card.new('Jd'), card.Card.new('Td')]
    hand2 = [card.Card.new('Qd'), card.Card.new('Qc')]
    comm_cards = [card.Card.new('Qh'), card.Card.new('Kh'), card.Card.new('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # three of a kind > two pair
    hand1 = [card.Card.new('Qd'), card.Card.new('Qc')]
    hand2 = [card.Card.new('Kd'), card.Card.new('Ad')]
    comm_cards = [card.Card.new('Qh'), card.Card.new('Kh'), card.Card.new('Ah')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # two pair > pair
    hand1 = [card.Card.new('9h'), card.Card.new('Qh')]
    hand2 = [card.Card.new('8s'), card.Card.new('7s')]
    comm_cards = [card.Card.new('9s'), card.Card.new('Qs'), card.Card.new('8d')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [card.Card.new('8s'), card.Card.new('7h')]
    hand2 = [card.Card.new('Ah'), card.Card.new('2s')]
    comm_cards = [card.Card.new('8h'), card.Card.new('9h'), card.Card.new('Ts')]
    assert hand_eval.evaluate(
        hand1, comm_cards) < hand_eval.evaluate(hand2, comm_cards)
