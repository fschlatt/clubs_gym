from pyker import error

STR_RANKS = '23456789TJQKA'
INT_RANKS = list(range(13))
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

# conversion string to int
CHAR_RANK_TO_INT_RANK = dict(zip(list(STR_RANKS), INT_RANKS))
CHAR_SUIT_TO_INT_SUIT = {
    'S': 1,  # spades
    'H': 2,  # hearts
    'D': 4,  # diamonds
    'C': 8,  # clubs
}

# pretty suits
PRETTY_SUITS = {
    1: chr(9824),   # spades
    2: chr(9829),   # hearts
    4: chr(9830),   # diamonds
    8: chr(9827)    # clubs
}


class Card:
    '''
    Class that represents card in deck. Initialize using cards string
    representation '{rank}{suit}' where rank is from [2-9, T/t, J/j, 
    Q/q, K/k, A/a] and suit is from [S/s, H/h, D/d, C/c]. 
    Examples: Card('TC'), Card('7H'), Card('ad')...

    Cards are represented as 32-bit integers. Most of the bits are used,
    and have a specific meaning, check the deuces README for details:

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
    '''

    def __init__(self, string: str):
        rank_char = string[0].upper()
        suit_char = string[1].upper()
        try:
            rank_int = CHAR_RANK_TO_INT_RANK[rank_char]
        except KeyError:
            raise error.InvalidRankError(
                (f'invalid rank {rank_char}, choose one '
                 f'of {list(CHAR_RANK_TO_INT_RANK.keys())}'))
        try:
            suit_int = CHAR_SUIT_TO_INT_SUIT[suit_char]
        except KeyError:
            raise error.InvalidSuitError(
                (f'invalid suit {suit_char}, choose one '
                 f'of {list(CHAR_SUIT_TO_INT_SUIT.keys())}'))

        rank_prime = PRIMES[rank_int]

        bitrank = 1 << rank_int << 16
        suit = suit_int << 12
        rank = rank_int << 8

        self._int = bitrank | suit | rank | rank_prime

    def __str__(self):
        suit_int = (self._int >> 12) & 0xF
        rank_int = (self._int >> 8) & 0xF

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
