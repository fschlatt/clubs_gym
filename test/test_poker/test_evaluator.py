import pytest

from clubs import error, poker


def test_init():

    with pytest.raises(error.InvalidHandSizeError):
        poker.Evaluator(4, 13, 0)
    with pytest.raises(error.InvalidHandSizeError):
        poker.Evaluator(4, 13, 6)
    with pytest.raises(error.InvalidOrderError):
        poker.LookupTable(4, 13, 5, order=["lala"])


def test_str_repr():

    evaluator = poker.Evaluator(4, 13, 5)

    string = (
        "straight flush (0.0015%) > four of a kind (0.0240%) > "
        "full house (0.1441%) > flush (0.1965%) > straight (0.3925%) > "
        "three of a kind (2.1128%) > two pair (4.7539%) > "
        "pair (42.2569%) > high card (50.1177%)"
    )
    repr_string = (
        f"Evaluator ({id(evaluator)}): straight flush (0.0015%) > "
        f"four of a kind (0.0240%) > full house (0.1441%) > "
        f"flush (0.1965%) > straight (0.3925%) > "
        f"three of a kind (2.1128%) > two pair (4.7539%) > "
        f"pair (42.2569%) > high card (50.1177%)"
    )

    assert str(evaluator) == string
    assert repr(evaluator) == repr_string


def test_hand_rank():

    evaluator = poker.Evaluator(4, 13, 5)

    assert evaluator.get_rank_class(0) == "straight flush"
    assert evaluator.get_rank_class(7462) == "high card"
    with pytest.raises(error.InvalidHandRankError):
        evaluator.get_rank_class(-1)
    with pytest.raises(error.InvalidHandRankError):
        evaluator.get_rank_class(7463)


def test_1_card():
    # no community cards
    evaluator = poker.Evaluator(1, 3, 1)
    hand1 = [poker.Card("As")]
    hand2 = [poker.Card("Ks")]
    assert evaluator.evaluate(hand1, []) < evaluator.evaluate(hand2, [])

    # 1 community card
    hand1 = [poker.Card("As")]
    hand2 = [poker.Card("Ks")]
    comm_cards = [poker.Card("Qs")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    hand1 = [poker.Card("Qs")]
    hand2 = [poker.Card("Ks")]
    comm_cards = [poker.Card("As")]
    assert evaluator.evaluate(hand1, comm_cards) == evaluator.evaluate(
        hand2, comm_cards
    )

    # mandatory hole card
    evaluator = poker.Evaluator(1, 3, 1, 1)
    hand1 = [poker.Card("Ks")]
    hand2 = [poker.Card("Qs")]
    comm_cards = [poker.Card("As")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 2 suits
    # 1 card for hand, no community cards
    evaluator = poker.Evaluator(2, 3, 1)
    hand1 = [poker.Card("Ah")]
    hand2 = [poker.Card("As")]
    assert evaluator.evaluate(hand1, []) == evaluator.evaluate(hand2, [])


def test_2_card():
    # 1 suit
    evaluator = poker.Evaluator(1, 3, 2)
    hand1 = [poker.Card("Ks")]
    hand2 = [poker.Card("Qs")]
    comm_cards = [poker.Card("As")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 2 suits
    # pair > high card
    evaluator = poker.Evaluator(2, 3, 2)
    hand1 = [poker.Card("Qs")]
    hand2 = [poker.Card("Ks")]
    comm_cards = [poker.Card("Qh")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [poker.Card("Ah")]
    hand2 = [poker.Card("Ks")]
    comm_cards = [poker.Card("Qs")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_3_card():
    # 1 suit
    # straight > high card
    evaluator = poker.Evaluator(1, 13, 3)
    hand1 = [poker.Card("Js")]
    hand2 = [poker.Card("Qs")]
    comm_cards = [poker.Card("9s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [poker.Card("Ks")]
    hand2 = [poker.Card("Qs")]
    comm_cards = [poker.Card("5s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [poker.Card("As")]
    comm_cards1 = [poker.Card("Qs"), poker.Card("Ks")]
    comm_cards2 = [poker.Card("2s"), poker.Card("3s")]
    assert evaluator.evaluate(hand, comm_cards1) < evaluator.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    evaluator = poker.Evaluator(2, 13, 3)
    hand1 = [poker.Card("Js")]
    hand2 = [poker.Card("Jc")]
    comm_cards = [poker.Card("9s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [poker.Card("Jc")]
    hand2 = [poker.Card("9c")]
    comm_cards = [poker.Card("9s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > flush
    hand1 = [poker.Card("7c")]
    hand2 = [poker.Card("As")]
    comm_cards = [poker.Card("7s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > high card
    hand1 = [poker.Card("9s")]
    hand2 = [poker.Card("Ac")]
    comm_cards = [poker.Card("7s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > straight
    evaluator = poker.Evaluator(4, 13, 3)
    hand1 = [poker.Card("Js")]
    hand2 = [poker.Card("Jc")]
    comm_cards = [poker.Card("9s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > pair
    hand1 = [poker.Card("Jc")]
    hand2 = [poker.Card("9c")]
    comm_cards = [poker.Card("9s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [poker.Card("As")]
    hand2 = [poker.Card("7c")]
    comm_cards = [poker.Card("7s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [poker.Card("7c")]
    hand2 = [poker.Card("Ac")]
    comm_cards = [poker.Card("7s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_4_card():
    # 1 suit
    # straight > high card
    evaluator = poker.Evaluator(1, 13, 4)
    hand1 = [poker.Card("Js"), poker.Card("Ts")]
    hand2 = [poker.Card("Qs"), poker.Card("3s")]
    comm_cards = [poker.Card("8s"), poker.Card("9s")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [poker.Card("Ks"), poker.Card("2s")]
    hand2 = [poker.Card("Qs"), poker.Card("3s")]
    comm_cards = [poker.Card("5s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [poker.Card("As")]
    comm_cards1 = [poker.Card("Js"), poker.Card("Qs"), poker.Card("Ks")]
    comm_cards2 = [poker.Card("2s"), poker.Card("3s"), poker.Card("4s")]
    assert evaluator.evaluate(hand, comm_cards1) < evaluator.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > two pair
    evaluator = poker.Evaluator(2, 13, 4)
    hand1 = [poker.Card("Js"), poker.Card("Ts")]
    hand2 = [poker.Card("8h"), poker.Card("9h")]
    comm_cards = [poker.Card("8s"), poker.Card("9s")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > straight
    hand1 = [poker.Card("8s"), poker.Card("9h")]
    hand2 = [poker.Card("Js"), poker.Card("Ts")]
    comm_cards = [poker.Card("8h"), poker.Card("9s")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > flush
    hand1 = [poker.Card("Js"), poker.Card("Ts")]
    hand2 = [poker.Card("4h"), poker.Card("6h")]
    comm_cards = [poker.Card("8h"), poker.Card("9h")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [poker.Card("8s"), poker.Card("7s")]
    hand2 = [poker.Card("Th"), poker.Card("2s")]
    comm_cards = [poker.Card("9s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [poker.Card("8s"), poker.Card("7h")]
    hand2 = [poker.Card("Th"), poker.Card("2s")]
    comm_cards = [poker.Card("8h"), poker.Card("9h")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 4 suits
    # four of a kind > straight flush
    evaluator = poker.Evaluator(4, 13, 4)
    hand1 = [poker.Card("As"), poker.Card("Ac")]
    hand2 = [poker.Card("Jh"), poker.Card("Qh")]
    comm_cards = [poker.Card("Kh"), poker.Card("Ah"), poker.Card("Ad")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight flush > three of a kind
    hand1 = [poker.Card("Jh"), poker.Card("Qh")]
    hand2 = [poker.Card("As"), poker.Card("Ac")]
    comm_cards = [poker.Card("Kh"), poker.Card("Ah")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # three of a kind > straight
    hand1 = [poker.Card("As"), poker.Card("Ac")]
    hand2 = [poker.Card("Jd"), poker.Card("Qd")]
    comm_cards = [poker.Card("Kh"), poker.Card("Ah")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [poker.Card("Jd"), poker.Card("Qd")]
    hand2 = [poker.Card("As"), poker.Card("Kc")]
    comm_cards = [poker.Card("Kh"), poker.Card("Ah")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [poker.Card("9h"), poker.Card("Qh")]
    hand2 = [poker.Card("8s"), poker.Card("7s")]
    comm_cards = [poker.Card("9s"), poker.Card("Qs")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [poker.Card("8s"), poker.Card("7s")]
    hand2 = [poker.Card("9h"), poker.Card("2h")]
    comm_cards = [poker.Card("9s"), poker.Card("Qs")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [poker.Card("8s"), poker.Card("7h")]
    hand2 = [poker.Card("Ah"), poker.Card("2s")]
    comm_cards = [poker.Card("8h"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_5_card():
    # 1 suit
    # straight > high card
    evaluator = poker.Evaluator(1, 13, 5)
    hand1 = [poker.Card("Js"), poker.Card("Ts")]
    hand2 = [poker.Card("Qs"), poker.Card("3s")]
    comm_cards = [poker.Card("7s"), poker.Card("8s"), poker.Card("9s")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # high card > low card
    hand1 = [poker.Card("Ks"), poker.Card("2s")]
    hand2 = [poker.Card("Qs"), poker.Card("3s")]
    comm_cards = [poker.Card("4s"), poker.Card("5s"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # ace high straight > ace low straight
    hand = [poker.Card("As")]
    comm_cards1 = [
        poker.Card("Ts"),
        poker.Card("Js"),
        poker.Card("Qs"),
        poker.Card("Ks"),
    ]
    comm_cards2 = [
        poker.Card("2s"),
        poker.Card("3s"),
        poker.Card("4s"),
        poker.Card("5s"),
    ]
    assert evaluator.evaluate(hand, comm_cards1) < evaluator.evaluate(hand, comm_cards2)

    # 2 suits
    # straight flush > straight
    evaluator = poker.Evaluator(2, 13, 5)
    hand1 = [poker.Card("Js"), poker.Card("Ts")]
    hand2 = [poker.Card("Jh"), poker.Card("Th")]
    comm_cards = [poker.Card("7s"), poker.Card("8s"), poker.Card("9s")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [poker.Card("Js"), poker.Card("Ts")]
    hand2 = [poker.Card("7h"), poker.Card("8h")]
    comm_cards = [poker.Card("7s"), poker.Card("8s"), poker.Card("9s")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > flush
    hand1 = [poker.Card("7h"), poker.Card("8h")]
    hand2 = [poker.Card("Js"), poker.Card("Ts")]
    comm_cards = [poker.Card("7s"), poker.Card("8s"), poker.Card("2s")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > pair
    hand1 = [poker.Card("8s"), poker.Card("7s")]
    hand2 = [poker.Card("Th"), poker.Card("2s")]
    comm_cards = [poker.Card("9s"), poker.Card("Ts"), poker.Card("As")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [poker.Card("8s"), poker.Card("7h")]
    hand2 = [poker.Card("Th"), poker.Card("2s")]
    comm_cards = [poker.Card("8h"), poker.Card("9h"), poker.Card("As")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 3 suits
    # straight flush > four of a kind
    evaluator = poker.Evaluator(3, 13, 5)
    hand1 = [poker.Card("Jh"), poker.Card("Qh")]
    hand2 = [poker.Card("Kc"), poker.Card("Kd")]
    comm_cards = [
        poker.Card("Th"),
        poker.Card("Kh"),
        poker.Card("Ah"),
        poker.Card("Ad"),
    ]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # full house > three of a kind
    hand1 = [poker.Card("Kc"), poker.Card("Kd")]
    hand2 = [poker.Card("Ac"), poker.Card("Qh")]
    comm_cards = [
        poker.Card("Th"),
        poker.Card("Kh"),
        poker.Card("Ah"),
        poker.Card("Ad"),
    ]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # three of a kind > straight
    hand1 = [poker.Card("Ac"), poker.Card("Qh")]
    hand2 = [poker.Card("Qc"), poker.Card("Jd")]
    comm_cards = [
        poker.Card("Th"),
        poker.Card("Kh"),
        poker.Card("Ah"),
        poker.Card("Ad"),
    ]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > two pair
    hand1 = [poker.Card("Jd"), poker.Card("Td")]
    hand2 = [poker.Card("Qd"), poker.Card("Kd")]
    comm_cards = [poker.Card("Qh"), poker.Card("Kh"), poker.Card("Ah")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > pair
    hand1 = [poker.Card("Qd"), poker.Card("Kd")]
    hand2 = [poker.Card("Qc"), poker.Card("Td")]
    comm_cards = [poker.Card("Qh"), poker.Card("Kh"), poker.Card("Ah")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [poker.Card("8s"), poker.Card("7h")]
    hand2 = [poker.Card("Ah"), poker.Card("2s")]
    comm_cards = [poker.Card("8h"), poker.Card("9h"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # 4 suits
    # straight flush > four of a kind
    evaluator = poker.Evaluator(4, 13, 5)
    hand1 = [poker.Card("Jh"), poker.Card("Qh")]
    hand2 = [poker.Card("As"), poker.Card("Ac")]
    comm_cards = [
        poker.Card("Th"),
        poker.Card("Kh"),
        poker.Card("Ah"),
        poker.Card("Ad"),
    ]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # four of a kind > full house
    hand1 = [poker.Card("As"), poker.Card("Ac")]
    hand2 = [poker.Card("Kc"), poker.Card("Kd")]
    comm_cards = [poker.Card("Kh"), poker.Card("Ah"), poker.Card("Ad")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # full house > flush
    hand1 = [poker.Card("Kc"), poker.Card("Kd")]
    hand2 = [poker.Card("Th"), poker.Card("5h")]
    comm_cards = [
        poker.Card("Kh"),
        poker.Card("Ah"),
        poker.Card("Ad"),
        poker.Card("2h"),
    ]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # flush > straight
    hand1 = [poker.Card("Th"), poker.Card("5h")]
    hand2 = [poker.Card("Jd"), poker.Card("Td")]
    comm_cards = [poker.Card("Qh"), poker.Card("Kh"), poker.Card("Ah")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # straight > three of a kind
    hand1 = [poker.Card("Jd"), poker.Card("Td")]
    hand2 = [poker.Card("Qd"), poker.Card("Qc")]
    comm_cards = [poker.Card("Qh"), poker.Card("Kh"), poker.Card("Ah")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # three of a kind > two pair
    hand1 = [poker.Card("Qd"), poker.Card("Qc")]
    hand2 = [poker.Card("Kd"), poker.Card("Ad")]
    comm_cards = [poker.Card("Qh"), poker.Card("Kh"), poker.Card("Ah")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # two pair > pair
    hand1 = [poker.Card("9h"), poker.Card("Qh")]
    hand2 = [poker.Card("8s"), poker.Card("7s")]
    comm_cards = [poker.Card("9s"), poker.Card("Qs"), poker.Card("8d")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)

    # pair > high card
    hand1 = [poker.Card("8s"), poker.Card("7h")]
    hand2 = [poker.Card("Ah"), poker.Card("2s")]
    comm_cards = [poker.Card("8h"), poker.Card("9h"), poker.Card("Ts")]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_short_deck():

    order = ["sf", "fk", "fl", "fh", "st", "tk", "tp", "pa", "hc"]

    evaluator = poker.Evaluator(4, 9, 5, 0, order=order)

    # flush > full house
    hand1 = [poker.Card("8h"), poker.Card("7h")]
    hand2 = [poker.Card("Jd"), poker.Card("As")]
    comm_cards = [
        poker.Card("Jh"),
        poker.Card("9h"),
        poker.Card("Ah"),
        poker.Card("Ac"),
    ]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)


def test_mandatory_hole_cards():

    evaluator = poker.Evaluator(4, 13, 5, 2)

    # mandatory hole cards
    hand1 = [poker.Card("Th"), poker.Card("Jc"), poker.Card("2c"), poker.Card("5c")]
    hand2 = [poker.Card("Ah"), poker.Card("Qc"), poker.Card("2h"), poker.Card("5s")]
    comm_cards = [
        poker.Card("9s"),
        poker.Card("8c"),
        poker.Card("7d"),
        poker.Card("6c"),
        poker.Card("5d"),
    ]
    assert evaluator.evaluate(hand1, comm_cards) < evaluator.evaluate(hand2, comm_cards)
