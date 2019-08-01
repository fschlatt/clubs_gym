from operator import itemgetter
from random import shuffle

from .card import Card


class Deck:
    """
    Class representing a deck. The first time we create, we seed the static
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it
    """
    __FULL_DECK = []

    def __init__(self, num_suits, num_ranks, order=None):
        self.num_ranks = num_ranks
        self.num_suits = num_suits
        self.trick = False
        if order is not None:
            self.top_cards = itemgetter(*order)
            self.bottom_cards = itemgetter(
                *list(set(range(num_ranks * num_suits)).difference(set(order))))
            self.trick = True
        self.shuffle()

    def shuffle(self):
        self.cards = Deck.GetFullDeck(self.num_ranks, self.num_suits)
        if self.trick:
            top_cards = list(self.top_cards(self.cards))
            bottom_cards = list(self.bottom_cards(self.cards))
            shuffle(bottom_cards)
            self.cards = top_cards + bottom_cards
        else:
            shuffle(self.cards)
        return self

    def draw(self, n=1):
        cards = []
        for _ in range(n):
            cards.append(self.cards.pop(0))
        return cards

    def __str__(self):
        Card.print_pretty_cards(self.cards)
        return ''

    @staticmethod
    def GetFullDeck(num_ranks, num_suits):
        if Deck.__FULL_DECK:
            return list(Deck.__FULL_DECK)

        # create the standard deck
        ranks = Card.STR_RANKS[-num_ranks:]
        suits = list(Card.CHAR_SUIT_TO_INT_SUIT.keys())[:num_suits]
        for rank in ranks:
            for suit in suits:
                Deck.__FULL_DECK.append(Card.new(rank + suit))
        return list(Deck.__FULL_DECK)
