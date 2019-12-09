from operator import itemgetter
from random import shuffle

from .card import Card


class Deck:
    '''
    Class representing a deck. The first time we create, we seed the static
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it
    '''

    def __init__(self, num_suits, num_ranks, order=None):
        self.num_ranks = num_ranks
        self.num_suits = num_suits
        self.full_deck = []
        self.tricked = False
        self.top_cards = None
        self.bottom_cards = None
        if order is not None:
            self.top_cards = itemgetter(*order)
            self.bottom_cards = itemgetter(
                *list(set(range(num_ranks * num_suits)).difference(set(order))))
            self.tricked = True
        self.shuffle()

    def shuffle(self):
        self.cards = self.get_full_deck(self.num_ranks, self.num_suits)
        if self.tricked:
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

    def trick(self, order):
        self.top_cards = itemgetter(*order)
        self.bottom_cards = itemgetter(
            *list(set(range(num_ranks * num_suits)).difference(set(order))))
        self.tricked = True

    def untrick(self):
        self.top_cards = None
        self.bottom_cards = None
        self.tricked = False

    def get_full_deck(self, num_ranks, num_suits):
        if self.full_deck:
            return list(self.full_deck)

        # create the standard deck
        ranks = Card.STR_RANKS[-num_ranks:]
        suits = list(Card.CHAR_SUIT_TO_INT_SUIT.keys())[:num_suits]
        for rank in ranks:
            for suit in suits:
                self.full_deck.append(Card.new(rank + suit))
        return list(self.full_deck)

    def __str__(self):
        string = ','.join([Card.int_to_pretty_str(card)
                           for card in self.cards])
        string = f'[{string}]'
        return string
