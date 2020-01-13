from random import shuffle

from . import card


class Deck:
    '''
    Class representing a deck. The first time we create, we seed the static
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it
    '''

    def __init__(self, num_suits, num_ranks, top_cards=None):
        self.num_ranks = num_ranks
        self.num_suits = num_suits
        self.full_deck = []
        ranks = card.Card.STR_RANKS[-num_ranks:]
        suits = list(card.Card.CHAR_SUIT_TO_INT_SUIT.keys())[:num_suits]
        for rank in ranks:
            for suit in suits:
                self.full_deck.append(card.Card(rank + suit))
        self._tricked = False
        self._top_idcs = None
        self._bottom_idcs = None
        if top_cards is not None:
            self.trick(top_cards)
        self.shuffle()

    def shuffle(self):
        self.cards = list(self.full_deck)
        if self._tricked:
            top_cards = [self.full_deck[idx] for idx in self._top_idcs]
            bottom_cards = [self.full_deck[idx] for idx in self._bottom_idcs]
            shuffle(bottom_cards)
            self.cards = top_cards + bottom_cards
        else:
            shuffle(self.cards)
        return self

    def draw(self, n=1):
        cards = []
        for _ in range(n):
            if self.cards: 
                cards.append(self.cards.pop(0))
        return cards

    def trick(self, top_cards):
        if not top_cards:
            self._tricked = False
            return self
        self._top_idcs = [self.full_deck.index(card.Card(top_card))
                         for top_card in top_cards]
        all_idcs = set(range(self.num_ranks * self.num_suits))
        self._bottom_idcs = list(all_idcs.difference(set(self._top_idcs)))
        self._tricked = True
        return self

    def untrick(self):
        self._top_idcs = None
        self._bottom_idcs = None
        self._tricked = False
        return self

    def __str__(self):
        string = ','.join([card.Card.int_to_pretty_str(card)
                           for card in self.cards])
        string = f'[{string}]'
        return string
