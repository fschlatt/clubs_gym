import random

from pyker import deuces


def test_draw():

    deck = deuces.Deck(2, 3)

    cards = deck.draw(1)
    assert len(cards) == 1

    cards = deck.draw(3)
    assert len(cards) == 3

    cards = deck.draw(4)
    assert len(cards) == 2

    cards = deck.draw(1)
    assert len(cards) == 0


def test_trick():
    random.seed(42)

    deck = deuces.Deck(4, 13).trick(['Ah', '2s'])

    cards = deck.draw(2)
    assert cards[0] == deuces.Card('Ah')
    assert cards[1] == deuces.Card('2s')

    deck = deck.shuffle()
    cards = deck.draw(2)
    assert cards[0] == deuces.Card('Ah')
    assert cards[1] == deuces.Card('2s')

    deck = deck.untrick().shuffle()
    cards = deck.draw(2)
    assert cards[0] != deuces.Card('Ah')
    assert cards[1] != deuces.Card('2s')
