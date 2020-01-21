# the basics
STR_RANKS = '23456789TJQKA'
INT_RANKS = range(13)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

# conversion from string => int
CHAR_RANK_TO_INT_RANK = dict(zip(list(STR_RANKS), INT_RANKS))
CHAR_SUIT_TO_INT_SUIT = {
    's': 1,  # spades
    'h': 2,  # hearts
    'd': 4,  # diamonds
    'c': 8,  # clubs
}
INT_SUIT_TO_CHAR_SUIT = 'xshxdxxxc'

# for pretty printing
PRETTY_SUITS = {
    1: chr(9824),   # spades
    2: chr(9829),   # hearts
    4: chr(9830),   # diamonds
    8: chr(9827)    # clubs
}


class Card:
    '''
    Static class that handles cards. Cards are represented as 32-bit
    integers, so there is no object instantiation, just ints. Most of 
    the bits are used, and have a specific meaning. See below: 

                                    Card:

                          bitrank     suit rank   prime
                    +--------+--------+--------+--------+
                    |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
                    +--------+--------+--------+--------+

        1) p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
        2) r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
        3) cdhs = suit of card (bit turned on based on suit of card)
        4) b = bit turned on depending on rank of card
        5) x = unused

    This representation will allows things like:
    - Making a unique prime product for each hand
    - Detecting flushes
    - Detecting straights

    and is also quite performant.
    '''

    def __init__(self, string: str):
        '''Converts card string into binary int representation

        Args:
            string (str): card string e.g. ('5d', 'Th', 'As'...)

        Returns:
            int: binary card int
        '''

        rank_char = string[0]
        suit_char = string[1]
        try:
            rank_int = CHAR_RANK_TO_INT_RANK[rank_char]
        except KeyError:
            raise KeyError(
                (f'invalid rank {rank_char}, choose one '
                 f'of {list(CHAR_RANK_TO_INT_RANK.keys())}'))
        try:
            suit_int = CHAR_SUIT_TO_INT_SUIT[suit_char]
        except KeyError:
            raise KeyError(
                (f'invalid suit {suit_char}, choose one '
                 f'of {list(CHAR_SUIT_TO_INT_SUIT.keys())}'))

        rank_prime = PRIMES[rank_int]

        bitrank = 1 << rank_int << 16
        suit = suit_int << 12
        rank = rank_int << 8

        self._int = bitrank | suit | rank | rank_prime

    @staticmethod
    def _get_rank_int(card_int: int) -> int:
        '''Grabs rank int from binary card int

        Args:
            card_int (int): binary card int

        Returns:
            int: rank int
        '''
        return (card_int >> 8) & 0xF

    @staticmethod
    def _get_suit_int(card_int: int) -> int:
        '''Grabs suit int from binary card int

        Args:
            card_int (int): binary card int

        Returns:
            int: suit in
        '''
        return (card_int >> 12) & 0xF

    def __str__(self):

        # suit and rank
        suit_int = self._get_suit_int(self._int)
        rank_int = self._get_rank_int(self._int)

        suit = PRETTY_SUITS[suit_int]
        rank = STR_RANKS[rank_int]

        return f'{rank}{suit}'

    def __repr__(self):
        return str(self)

    def __and__(self, other):
        return self._int & other

    def __rand__(self, other):
        return other & self._int

    def __or__(self, other):
        return self._int | other
    
    def __ror__(self, other):
        return other | self._int

    def __lshift__(self, other):
        return self._int << other

    def __rshift__(self, other):
        return self._int >> other

    def __eq__(self, other):
        return self._int == other


def prime_product_from_rankbits(rankbits: int) -> int:
    '''Computes prime product from rankbits of cards, primarily used
    for evaluating flushes and straights. Expects 13 bit integer 
    with bits of the cards in the hand flipped.

    Args:
        rankbits (int): 13 bit integer with flipped rank bits

    Returns:
        int: prime product if bit flipped cards
    '''
    product = 1
    for i in INT_RANKS:
        # if the ith bit is set
        if rankbits & (1 << i):
            product *= PRIMES[i]

    return product


def prime_product_from_hand(cards: list) -> int:
    '''Computes unique prime product for a list of cards. Used for
    evaluating hands

    Args:
        card_ints (list): list of cards

    Returns:
        int: prime product of cards
    '''
    product = 1
    for card in cards:
        product *= (card & 0xFF)
    return product
