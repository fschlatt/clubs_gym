"""Classes and functions to create and manipulate cards and lists of
cards from a standard 52 card poker deck"""
import random
from typing import Dict, List, Optional, Union

from clubs import error

STR_RANKS: str = "23456789TJQKA"
INT_RANKS: List[int] = list(range(13))
PRIMES: List[int] = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

# conversion string to int
CHAR_RANK_TO_INT_RANK: Dict[str, int] = dict(zip(list(STR_RANKS), INT_RANKS))
CHAR_SUIT_TO_INT_SUIT: Dict[str, int] = {
    "S": 1,  # spades
    "H": 2,  # hearts
    "D": 4,  # diamonds
    "C": 8,  # clubs
}

# pretty suits
PRETTY_SUITS: Dict[int, str] = {
    1: chr(9824),  # spades
    2: chr(9829),  # hearts
    4: chr(9830),  # diamonds
    8: chr(9827),  # clubs
}


class Card:
    """Cards are represented as 32-bit integers. Most of the bits are used
    and have a specific meaning, check the poker README for details:

                  bitrank  suit rank   prime
        +--------+--------+--------+--------+
        |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
        +--------+--------+--------+--------+

        1) p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
        2) r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
        3) cdhs = suit of card (bit turned on based on suit of card)
        4) b = bit turned on depending on rank of card
        5) x = unused

    Parameters
    ----------
    string : str
        card string of format '{rank}{suit}' where rank is from
        [2-9, T/t, J/j, Q/q, K/k, A/a] and suit is from
        [S/s, H/h, D/d, C/c]

    Examples
    ------
    Card('TC'), Card('7H'), Card('ad')...
    """

    def __init__(self, string: str) -> None:

        rank_char = string[0].upper()
        suit_char = string[1].upper()
        try:
            rank_int = CHAR_RANK_TO_INT_RANK[rank_char]
        except KeyError:
            raise error.InvalidRankError(
                (
                    f"invalid rank {rank_char}, choose one "
                    f"of {list(CHAR_RANK_TO_INT_RANK.keys())}"
                )
            )
        try:
            suit_int = CHAR_SUIT_TO_INT_SUIT[suit_char]
        except KeyError:
            raise error.InvalidSuitError(
                (
                    f"invalid suit {suit_char}, choose one "
                    f"of {list(CHAR_SUIT_TO_INT_SUIT.keys())}"
                )
            )

        rank_prime = PRIMES[rank_int]

        bitrank = 1 << rank_int << 16
        suit = suit_int << 12
        rank = rank_int << 8

        self._int: int = bitrank | suit | rank | rank_prime

    def __str__(self) -> str:
        suit_int = (self._int >> 12) & 0xF
        rank_int = (self._int >> 8) & 0xF

        suit = PRETTY_SUITS[suit_int]
        rank = STR_RANKS[rank_int]

        return f"{rank}{suit}"

    def __repr__(self) -> str:
        return f"Card ({id(self)}): {str(self)}"

    def __and__(self, other: Union["Card", int]) -> int:
        if isinstance(other, Card):
            other = other._int
        return self._int & other

    def __rand__(self, other: int) -> int:
        return other & self._int

    def __or__(self, other: Union["Card", int]) -> int:
        if isinstance(other, Card):
            other = other._int
        return self._int | other

    def __ror__(self, other: int) -> int:
        return other | self._int

    def __lshift__(self, other: int) -> int:
        return self._int << other

    def __rshift__(self, other: int) -> int:
        return self._int >> other

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Card):
            return bool(self._int == other._int)
        raise NotImplementedError("only comparisons of two cards allowed")


def prime_product_from_rankbits(rankbits: int) -> int:
    """Computes prime product from rankbits of cards, primarily used
    for evaluating flushes and straights. Expects 13 bit integer
    with bits of the cards in the hand flipped.

    Parameters
    ----------
    rankbits : int
        13 bit integer with flipped rank bits

    Returns
    -------
    int
        prime product of rank cards
    """

    product = 1
    for i in INT_RANKS:
        # if the ith bit is set
        if rankbits & (1 << i):
            product *= PRIMES[i]
    return product


def prime_product_from_hand(cards: List[Card]) -> int:
    """Computes unique prime product for a list of cards. Used for
    evaluating hands

    Parameters
    ----------
    cards : List[Card]
        list of cards

    Returns
    -------
    int
        prime product of cards
    """

    product = 1
    for card in cards:
        product *= card & 0xFF
    return product


class Deck:
    """A deck contains at most 52 cards, 13 ranks 4 suits. Any "subdeck"
    of the standard 52 card deck is valid, i.e. the number of suits
    must be between 1 and 4 and number of ranks between 1 and 13. A
    deck can be tricked to ensure a certain order of cards.

    Parameters
    ----------
    num_suits : int
        number of suits to use in deck
    num_ranks : int
        number of ranks to use in deck
    """

    def __init__(self, num_suits: int, num_ranks: int) -> None:
        if num_ranks < 1 or num_ranks > 13:
            raise error.InvalidRankError(
                f"Invalid number of suits, expected number of suits "
                f"between 1 and 13, got {num_ranks}"
            )
        if num_suits < 1 or num_suits > 4:
            raise error.InvalidSuitError(
                f"Invalid number of suits, expected number of suits "
                f"between 1 and 4, got {num_suits}"
            )
        self.num_ranks = num_ranks
        self.num_suits = num_suits
        self.full_deck: List[Card] = []
        ranks = STR_RANKS[-num_ranks:]
        suits = list(CHAR_SUIT_TO_INT_SUIT.keys())[:num_suits]
        for rank in ranks:
            for suit in suits:
                self.full_deck.append(Card(rank + suit))
        self._tricked = False
        self._top_idcs: List[int] = []
        self._bottom_idcs: List[int] = []
        self.shuffle()

    def __str__(self) -> str:
        string = ",".join([str(card) for card in self.cards])
        string = f"[{string}]"
        return string

    def __repr__(self) -> str:
        return f"Deck ({id(self)}): {str(self)}"

    def draw(self, n: int = 1) -> List[Card]:
        """Draws cards from the top of the deck. If the number of cards
        to draw exceeds the number of cards in the deck, all cards
        left in the deck are returned.

        Parameters
        ----------
        n : int, optional
            number of cards to draw, by default 1

        Returns
        -------
        List[Card]
            cards drawn from the deck
        """
        cards = []
        for _ in range(n):
            if self.cards:
                cards.append(self.cards.pop(0))
            else:
                break
        return cards

    def shuffle(self) -> "Deck":
        """Shuffles the deck. If a tricking order is given, the desired
        cards are placed on the top of the deck after shuffling.

        Returns
        -------
        Deck
            self
        """
        self.cards = list(self.full_deck)
        if self._tricked and self._top_idcs and self._bottom_idcs:
            top_cards = [self.full_deck[idx] for idx in self._top_idcs]
            bottom_cards = [self.full_deck[idx] for idx in self._bottom_idcs]
            random.shuffle(bottom_cards)
            self.cards = top_cards + bottom_cards
        else:
            random.shuffle(self.cards)
        return self

    def trick(
        self, top_cards: Optional[List[Union[str, Card]]] = None, shuffle: bool = True
    ) -> "Deck":
        """Tricks the deck by placing a fixed order of cards on the top
        of the deck and shuffling the rest. E.g.
        deck.trick(['AS', '2H']) places the ace of spades and deuce of
        hearts on the top of the deck. The order of tricked cards
        persists even after untricking. That is, calling
        deck.trick(...).untrick().trick() will keep the deck tricked
        in the order given in the first trick call.

        Parameters
        ----------
        top_cards : Optional[List[Union[str, Card]]], optional
            list of cards to be placed on the top of the deck, by
            default None, by default None
        shuffle : bool, optional
            shuffles the deck after tricking, by default True

        Returns
        -------
        Deck
            self
        """
        if top_cards is None and not self._top_idcs:
            self._tricked = False
            return self.shuffle()
        if top_cards:
            cards = [
                Card(top_card) if isinstance(top_card, str) else top_card
                for top_card in top_cards
            ]
            self._top_idcs = [self.full_deck.index(top_card) for top_card in cards]
            all_idcs = set(range(self.num_ranks * self.num_suits))
            self._bottom_idcs = list(all_idcs.difference(set(self._top_idcs)))
        self._tricked = True
        return self.shuffle()

    def untrick(self) -> "Deck":
        """Removes the tricked cards from the top of the deck. The order
        of tricked cards persists even after untricking. That is,
        calling deck.trick(...).untrick().trick() will keep the deck
        tricked in the order given in the first trick call.

        Returns
        -------
        Deck
            self
        """
        self._tricked = False
        return self
