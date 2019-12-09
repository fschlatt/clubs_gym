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

    # hearts and diamonds
    PRETTY_REDS = [2, 4]

    @staticmethod
    def new(string: str) -> int:
        '''Converts card string into binary int representation

        Args:
            string (str): card string e.g. ('5d', 'Th', 'As'...)

        Returns:
            int: binary card int
        '''

        rank_char = string[0]
        suit_char = string[1]
        rank_int = Card.CHAR_RANK_TO_INT_RANK[rank_char]
        suit_int = Card.CHAR_SUIT_TO_INT_SUIT[suit_char]
        rank_prime = Card.PRIMES[rank_int]

        bitrank = 1 << rank_int << 16
        suit = suit_int << 12
        rank = rank_int << 8

        return bitrank | suit | rank | rank_prime

    @staticmethod
    def get_rank_int(card_int: int) -> int:
        '''Grabs rank int from binary card int

        Args:
            card_int (int): binary card int

        Returns:
            int: rank int
        '''
        return (card_int >> 8) & 0xF

    @staticmethod
    def get_suit_int(card_int: int) -> int:
        '''Grabs suit int from binary card int

        Args:
            card_int (int): binary card int

        Returns:
            int: suit in
        '''
        return (card_int >> 12) & 0xF

    @staticmethod
    def prime_product_from_hand(card_ints: list) -> int:
        '''Computes unique prime product for a list of cards. Used for
        evaluating hands

        Args:
            card_ints (list): list of card ints

        Returns:
            int: prime product of cards
        '''
        product = 1
        for card_int in card_ints:
            product *= (card_int & 0xFF)
        return product

    @staticmethod
    def prime_product_from_rankbits(rankbits: int) -> int:
        '''Computes prime product from rankbits of cards, primarily used
        for evaluating flushes and straights. Expects 
        
        Args:
            rankbits (int): [description]
        
        Returns:
            int: [description]
        '''        
        product = 1
        # '''
        # Returns the prime product using the bitrank (b)
        # bits of the hand. Each 1 in the sequence is converted
        # to the correct prime and multiplied in.

        # Params:
        #     rankbits = a single 32-bit (only 13-bits set) integer representing
        #             the ranks of 5 _different_ ranked cards
        #             (5 of 13 bits are set)

        # Primarily used for evaulating flushes and straights,
        # two occasions where we know the ranks are *ALL* different.

        # Assumes that the input is in form (set bits):

        #                       rankbits
        #                 +--------+--------+
        #                 |xxxbbbbb|bbbbbbbb|
        #                 +--------+--------+

        # '''
        for i in Card.INT_RANKS:
            # if the ith bit is set
            if rankbits & (1 << i):
                product *= Card.PRIMES[i]

        return product

    @staticmethod
    def int_to_pretty_str(card_int):
        '''
        Prints a single card
        '''

        color = False
        try:
            from colorama import init
            from termcolor import colored

            init()
            # for mac, linux: http://pypi.python.org/pypi/termcolor
            # can use for windows: http://pypi.python.org/pypi/colorama
            color = True

        except ImportError:
            pass

        # suit and rank
        suit_int = Card.get_suit_int(card_int)
        rank_int = Card.get_rank_int(card_int)

        # if we need to color red
        suit = Card.PRETTY_SUITS[suit_int]
        if color and suit_int in Card.PRETTY_REDS:
            suit = colored(suit, 'red')

        rank = Card.STR_RANKS[rank_int]

        return f'{rank}{suit}'
