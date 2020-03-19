'''Classes and functions to evaluate poker hands'''
import functools
import itertools
import operator

from pyker import error

from . import card


class Evaluator(object):
    '''Evalutes poker hands using hole and community cards

    Args:
        suits (int): number of suits
        ranks (int): number of ranks
        cards_for_hand (int): number of cards used for a poker hand
        mandatory_hole_cards (int): number of hole cards which must be
                                    be used for a hand
        low_end_straight (bool, optional): toggle to include straights
                                           where ace is the lowest
                                           card. defaults to True.
        order (list, optional): custom hand rank order, if None hands 
                                are ranked by rarity. defaults to None.
    '''

    def __init__(self, suits: int, ranks: int, cards_for_hand: int,
                 mandatory_hole_cards: int, low_end_straight: bool = True,
                 order: list = None):

        if cards_for_hand < 0 or cards_for_hand > 5:
            raise error.InvalidHandSizeError(
                f'Evaluation for {cards_for_hand} card hands is not supported. '
                f'pyker currently supports 1-5 card poker hands'
            )

        self.suits = suits
        self.ranks = ranks
        self.cards_for_hand = cards_for_hand
        self.mandatory_hole_cards = mandatory_hole_cards

        self.table = LookupTable(
            suits, ranks, cards_for_hand,
            low_end_straight=low_end_straight, order=order
        )

        total = sum(
            self.table.hand_dict[hand]['suited']
            for hand in self.table.ranked_hands
        )

        hands = [
            '{} ({:.4%})'.format(
                hand, self.table.hand_dict[hand]['suited'] / total)
            for hand in self.table.ranked_hands
        ]
        self.hand_ranks = ' > '.join(hands)

    def __str__(self):
        return self.hand_ranks

    def __repr__(self):
        return str(self)

    def evaluate(self, hole_cards: list, community_cards: list):
        '''Evaluates the hand rank of a poker hand from a list of hole
        and a list of community cards. Empty hole and community cards
        are supported as well as requiring a minimum number of hole
        cards to be used.

        Args:
            hole_cards (list): list of hole cards of a player
            community_cards (list): list of community cards

        Returns:
            int: hand rank
        '''
        # if a number of hole cards are mandatory
        if self.mandatory_hole_cards:
            # get all hole and community card combinations
            hole_card_combs = itertools.combinations(
                hole_cards, self.mandatory_hole_cards
            )
            num_comm_cards = self.cards_for_hand - self.mandatory_hole_cards
            if num_comm_cards:
                comm_card_combs = itertools.combinations(
                    community_cards, num_comm_cards
                )
                iterator = itertools.product(
                    hole_card_combs, comm_card_combs
                )
                all_card_combs = list(
                    (sum(card_comb, ()) for card_comb in
                     iterator)
            )
            else:
                all_card_combs = list(hole_card_combs)
        # else create combinations from all cards
        else:
            all_card_combs = list(
                itertools.combinations(
                    hole_cards + community_cards, self.cards_for_hand
                )
            )

        minimum = self.table.max_rank

        for card_comb in all_card_combs:
            score = self.table.lookup(list(card_comb))
            if score < minimum:
                minimum = score
        return minimum

    def get_rank_class(self, hand_rank: int):
        '''Outputs hand rank string from integer hand rank

        Args:
            hand_rank (int): integer hand rank

        Returns:
            str: hand rank string
        '''
        if hand_rank < 0 or hand_rank > self.table.max_rank:
            raise error.InvalidHandRankError(
                (f'invalid hand rank, expected 0 <= hand_rank'
                 f' <= {self.table.max_rank}, got {hand_rank}'))
        for hand in self.table.ranked_hands:
            if hand_rank <= self.table.hand_dict[hand]['cumulative unsuited']:
                return hand


class LookupTable():
    '''
    Lookup table maps unique prime product of hands to unique
    integer hand rank. The lower the rank the better the hand

    Args:
        suits (int): number of suits in deck
        ranks (int): number of ranks in deck
        cards_for_hand (int): number of cards used for a poker hand
        low_end_straight (bool, optional): toggle to include straights
                                           where ace is the lowest
                                           card. defaults to True.
        order (list, optional): custom hand rank order, if None hands
                                are ranked by rarity. defaults to None.
    '''

    ORDER_STRINGS = ['sf', 'fk', 'fh', 'fl', 'st', 'tk', 'tp', 'pa', 'hc']

    def __init__(self, suits: int, ranks: int, cards_for_hand: int,
                 low_end_straight: bool = True, order: list = None):
        if order is not None:
            if any(string not in order for string in self.ORDER_STRINGS):
                raise error.InvalidOrderError(
                    (f'invalid order list {order},'
                     f'order list must be permutation of {self.ORDER_STRINGS}')
                )

        # number of suited and unsuited possibilities of different hands
        straight_flushes, u_straight_flushes = self.__straight_flush(
            suits, ranks, cards_for_hand, low_end_straight
        )
        four_of_a_kinds, u_four_of_a_kinds = self.__four_of_a_kind(
            suits, ranks, cards_for_hand
        )
        full_houses, u_full_houses = self.__full_house(
            suits, ranks, cards_for_hand
        )
        flushes, u_flushes = self.__flush(
            suits, ranks, cards_for_hand, low_end_straight
        )
        straights, u_straights = self.__straight(
            suits, ranks, cards_for_hand, low_end_straight
        )
        three_of_a_kinds, u_three_of_a_kinds = self.__three_of_a_kind(
            suits, ranks, cards_for_hand
        )
        two_pairs, u_two_pairs = self.__two_pair(
            suits, ranks, cards_for_hand
        )
        pairs, u_pairs = self.__pair(
            suits, ranks, cards_for_hand
        )
        high_cards, u_high_cards = self.__high_card(
            suits, ranks, cards_for_hand, low_end_straight
        )

        self.hand_dict = {
            'straight flush': {
                'suited': straight_flushes,
                'unsuited': u_straight_flushes
            },
            'four of a kind': {
                'suited': four_of_a_kinds,
                'unsuited': u_four_of_a_kinds
            },
            'full house': {
                'suited': full_houses,
                'unsuited': u_full_houses
            },
            'flush': {
                'suited': flushes,
                'unsuited': u_flushes
            },
            'straight': {
                'suited': straights,
                'unsuited': u_straights
            },
            'three of a kind': {
                'suited': three_of_a_kinds,
                'unsuited': u_three_of_a_kinds
            },
            'two pair': {
                'suited': two_pairs,
                'unsuited': u_two_pairs
            },
            'pair': {
                'suited': pairs,
                'unsuited': u_pairs
            },
            'high card': {
                'suited': high_cards,
                'unsuited': u_high_cards
            }
        }

        # suited hands
        s_hands = [
            (straight_flushes, 'straight flush'),
            (four_of_a_kinds, 'four of a kind'),
            (full_houses, 'full house'),
            (flushes, 'flush'),
            (straights, 'straight'),
            (three_of_a_kinds, 'three of a kind'),
            (two_pairs, 'two pair'),
            (pairs, 'pair'),
            (high_cards, 'high card')
        ]

        # sort suited hands and rank unsuited hands by suited
        # rank order or by order provided
        if order is None:
            s_hands = sorted(s_hands)
        else:
            idcs = [self.ORDER_STRINGS.index(hand) for hand in order]
            s_hands = [s_hands[idx] for idx in idcs]
        # lookup is done on unsuited hands but hand
        # rank is dependent on suited hands
        u_hands = [
            (self.hand_dict[u_hand[1]]['unsuited'], u_hand[1])
            for u_hand in s_hands
        ]

        # compute cumulative number of unsuited hands for each hand
        # cumulative unsuited is the maximum rank a hand can have
        ranked_hands = []
        rank = 0
        cumulative_hands = 0
        for u_hand in u_hands:
            hand_rank = u_hand[1]
            cumulative_hands += u_hand[0]
            self.hand_dict[hand_rank]['cumulative unsuited'] = cumulative_hands
            if cumulative_hands > 0:
                self.hand_dict[hand_rank]['rank'] = rank
                rank += 1
                ranked_hands.append(hand_rank)
        self.max_rank = cumulative_hands

        # list of hands ordered by rank from best to worst
        self.ranked_hands = ranked_hands

        # create lookup tables
        self.suited_lookup = {}
        self.unsuited_lookup = {}
        self.__flushes(ranks, cards_for_hand, low_end_straight)
        self.__multiples(ranks, cards_for_hand)

        # if suited hands aren't relevant set the suited
        # lookup table equal to the unsuited table
        if not self.hand_dict['flush']['cumulative unsuited']:
            self.suited_lookup = self.unsuited_lookup

    def lookup(self, cards: list):
        '''Returns unique hand rank for list of cards

        Args:
            cards (list): card list to be evaluated

        Returns:
            int: hand rank
        '''
        # if all flush bits equal then use flush lookup
        if functools.reduce(operator.and_, cards + [0xF000]):
            hand_or = functools.reduce(operator.or_, cards) >> 16
            prime = card.prime_product_from_rankbits(hand_or)
            return self.suited_lookup[prime]
        else:
            prime = card.prime_product_from_hand(cards)
            return self.unsuited_lookup[prime]

    def __straight_flush(self, suits, ranks, cards_for_hand, low_end_straight):
        if cards_for_hand < 3 or suits < 2:
            return 0, 0
        # number of smallest cards which start straight
        unsuited = ranks - (cards_for_hand - 1) + low_end_straight
        # multiplied with number of suits
        suited = max(unsuited, unsuited * suits)
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __four_of_a_kind(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 4 or suits < 4:
            return 0, 0
        # choose 1 rank for quads multiplied by
        # rank choice for remaining cards
        unsuited = _ncr(ranks, 1) * _ncr(ranks - 1, cards_for_hand - 4)
        # mutliplied with number of suit choices for remaining cards
        suited = max(unsuited, unsuited * suits**(cards_for_hand - 4))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __full_house(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 5 or suits < 3:
            return 0, 0
        # choose one rank for trips and pair multiplied by
        # rank choice for remaining cards
        unsuited = _ncr(ranks, 1) * _ncr(ranks - 1, 1) * \
            _ncr(ranks - 2, cards_for_hand - 5)
        # multiplied with number of suit choices for
        # trips + pair and remaining cards
        suited = max(unsuited, unsuited * _ncr(suits, 3) * _ncr(suits, 2) *
                     suits**(cards_for_hand - 5))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __flush(self, suits, ranks, cards_for_hand, low_end_straight):
        if cards_for_hand < 3 or suits < 2:
            return 0, 0
        # all straight combinations
        straight_flushes = ranks - (cards_for_hand - 1) + low_end_straight
        # choose all cards from ranks minus straight flushes
        unsuited = _ncr(ranks, cards_for_hand) - straight_flushes
        # multiplied by number of suits
        suited = max(unsuited, unsuited * suits)
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __straight(self, suits, ranks, cards_for_hand, low_end_straight):
        if cards_for_hand < 3:
            return 0, 0
        # number of smallest cards which start straight
        unsuited = ranks - (cards_for_hand - 1) + low_end_straight
        # straight flush combinations
        straight_flushes = 0
        if suits > 1:
            straight_flushes = unsuited * suits
        # multiplied with suit choice for every card
        # minus straight flushes
        suited = max(unsuited, unsuited * suits **
                     cards_for_hand - straight_flushes)
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __three_of_a_kind(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 3 or suits < 3:
            return 0, 0
        # choose one rank for trips multiplied by
        # rank choice for remaining cards
        unsuited = _ncr(ranks, 1) * _ncr(ranks - 1, cards_for_hand - 3)
        # multiplied with suit choices for trips and remaining cards
        suited = max(unsuited, unsuited * _ncr(suits, 3) *
                     _ncr(suits, 3)**(cards_for_hand - 3))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __two_pair(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 4 or suits < 2:
            return 0, 0
        # choose two ranks for pairs multiplied by
        # ranks for remaining cards
        unsuited = _ncr(ranks, 2) * _ncr(ranks - 2, cards_for_hand - 4)
        # multiplied with suit choices for both pairs
        # and suit choices for remaining cards
        suited = max(unsuited, unsuited * _ncr(suits, 2)
                     ** 2 * suits**(cards_for_hand - 4))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __pair(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 2 or suits < 2:
            return 0, 0
        # choose rank for pair multiplied by
        # ranks for remaining cards
        unsuited = _ncr(ranks, 1) * _ncr(ranks - 1, cards_for_hand - 2)
        # multiplied with suit choices for pair and remaining cards
        suited = max(unsuited, unsuited * _ncr(suits, 2)
                     * suits**(cards_for_hand - 2))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __high_card(self, suits, ranks, cards_for_hand, low_end_straight):
        # number of smallest cards which start straight
        straights = 0
        if cards_for_hand > 2:
            straights = ranks - (cards_for_hand - 1) + low_end_straight
        # any combination of rank and subtract straights
        unsuited = _ncr(ranks, cards_for_hand) - straights
        # multiplied with suit choices for all cards
        # all same suits not allowed
        suited = max(unsuited, unsuited * (suits**cards_for_hand - suits))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __flushes(self, ranks, cards_for_hand, low_end_straight):
        # straight flushes in rank order
        straight_flushes = []

        # if any straights/straight flushes exist in card configuration
        # create list of all possibilities
        if (self.hand_dict['straight flush']['cumulative unsuited'] or
                self.hand_dict['straight']['cumulative unsuited']):
            # start with best straight (flush)
            # for 5 card hand with 13 ranks: 0b1111100000000
            bin_num_str = ('0b' + '1' * cards_for_hand
                           + '0' * (13 - cards_for_hand))
            # remove one 0 for every straight (flush)
            for _ in range(ranks - (cards_for_hand - 1)):
                straight_flushes.append(int(bin_num_str, 2))
                bin_num_str = bin_num_str[:-1]
            if low_end_straight:
                # add low end straight
                bin_num_str = ('0b1' + '0' * (ranks - cards_for_hand)
                               + '1' * (cards_for_hand - 1)
                               + '0' * (13 - ranks))
                straight_flushes.append(int(bin_num_str, 2))

        # if any flushes/high cards exist in card configuration
        # create list of all possibilities
        if (self.hand_dict['flush']['cumulative unsuited'] or
                self.hand_dict['high card']['cumulative unsuited']):
            # dynamically generate all the other
            # flushes (including straight flushes)
            flushes = []
            # start with lowest non pair hand
            # for 5 card hand with 13 ranks: 0b11111
            bin_num_str = '0b' + ('1' * cards_for_hand)
            gen = _lexographic_next_bit(int(bin_num_str, 2))
            # iterate over all possibilities of unique hands
            for _ in range(int(_ncr(ranks, cards_for_hand))):
                # pull the next flush pattern from generator
                # offset by number of ranks not in play
                flush = next(gen) << (13 - ranks)
                if flush not in straight_flushes:
                    flushes.append(flush)

        # hand generation started from worst hand
        # so needs to be reversed
        flushes.reverse()

        # add prime products to look up maps
        # use ranks of hands computed beforehand
        if self.hand_dict['straight flush']['cumulative unsuited']:
            num_ranks = len(straight_flushes)
            assert (num_ranks == self.hand_dict['straight flush']['unsuited'])
            rank = self.__get_rank('straight flush')
            for straight_flush in straight_flushes:
                prime_product = card.prime_product_from_rankbits(
                    straight_flush)
                self.suited_lookup[prime_product] = rank
                rank += 1

        if self.hand_dict['flush']['cumulative unsuited']:
            num_ranks = len(flushes)
            assert (num_ranks == self.hand_dict['flush']['unsuited'])
            rank = self.__get_rank('flush')
            for flush in flushes:
                prime_product = card.prime_product_from_rankbits(flush)
                self.suited_lookup[prime_product] = rank
                rank += 1

        # straight flush and flush bit sequences can be reused for
        # straights and high cards since they are inherently related
        # and differ only by context
        if self.hand_dict['straight']['cumulative unsuited']:
            num_ranks = len(straight_flushes)
            assert (num_ranks == self.hand_dict['straight']['unsuited'])
            rank = self.__get_rank('straight')
            for straight in straight_flushes:
                prime_product = card.prime_product_from_rankbits(straight)
                self.unsuited_lookup[prime_product] = rank
                rank += 1

        if self.hand_dict['high card']['cumulative unsuited']:
            num_ranks = len(flushes)
            assert (num_ranks == self.hand_dict['high card']['unsuited'])
            rank = self.__get_rank('high card')
            for high_card in flushes:
                prime_product = card.prime_product_from_rankbits(high_card)
                self.unsuited_lookup[prime_product] = rank
                rank += 1

    def __multiples(self, ranks, cards_for_hand):
        backwards_ranks = list(range(13 - 1, 13 - 1 - ranks, -1))

        if self.hand_dict['four of a kind']['cumulative unsuited']:
            rank = self.__get_rank('four of a kind')
            # for each choice of a set of four rank
            for four_of_a_kind in backwards_ranks:
                # compute prime product for selected rank
                base_product = card.PRIMES[four_of_a_kind]**4
                # and for each possible combination of kicker ranks
                kickers = backwards_ranks[:]
                kickers.remove(four_of_a_kind)
                combinations = list(itertools.combinations(
                    kickers, cards_for_hand - 4))
                # if at least one kicker exists
                if combinations[0]:
                    for combination in combinations:
                        product = base_product
                        # for each kicker multiply kicker prime onto
                        # base prime product
                        for kicker in combination:
                            product *= card.PRIMES[kicker]
                        self.unsuited_lookup[product] = rank
                        rank += 1
                else:
                    self.unsuited_lookup[base_product] = rank
                    rank += 1
            num_ranks = rank - self.__get_rank('four of a kind')
            assert (num_ranks == self.hand_dict['four of a kind']['unsuited'])

        if self.hand_dict['full house']['cumulative unsuited']:
            rank = self.__get_rank('full house')
            # for each three of a kind
            for three_of_a_kind in backwards_ranks:
                # and for each choice of pair rank
                pairs = backwards_ranks[:]
                pairs.remove(three_of_a_kind)
                for pair in pairs:
                    base_product = card.PRIMES[three_of_a_kind]**3 * \
                        card.PRIMES[pair]**2
                    kickers = pairs[:]
                    kickers.remove(pair)
                    combinations = list(itertools.combinations(
                        kickers, cards_for_hand - 5))
                    # if at least one kicker exists
                    if combinations[0]:
                        for combination in combinations:
                            product = base_product
                            # for each kicker multiply kicker prime onto
                            # base prime product
                            for kicker in combination:
                                product *= card.PRIMES[kicker]
                            self.unsuited_lookup[product] = rank
                            rank += 1
                    else:
                        self.unsuited_lookup[base_product] = rank
                        rank += 1
            num_ranks = rank - self.__get_rank('full house')
            assert (num_ranks == self.hand_dict['full house']['unsuited'])

        if self.hand_dict['three of a kind']['cumulative unsuited']:
            rank = self.__get_rank('three of a kind')
            # for each three of a kind
            for three_of_a_kind in backwards_ranks:
                base_product = card.PRIMES[three_of_a_kind]**3
                kickers = backwards_ranks[:]
                kickers.remove(three_of_a_kind)
                combinations = list(itertools.combinations(
                    kickers, cards_for_hand - 3))
                # if at least one kicker exists
                if combinations[0]:
                    for combination in combinations:
                        product = base_product
                        # for each kicker multiply kicker prime onto
                        # base prime product
                        for kicker in combination:
                            product *= card.PRIMES[kicker]
                        self.unsuited_lookup[product] = rank
                        rank += 1
                else:
                    self.unsuited_lookup[base_product] = rank
                    rank += 1
            num_ranks = rank - self.__get_rank('three of a kind')
            assert (num_ranks == self.hand_dict['three of a kind']['unsuited'])

        if self.hand_dict['two pair']['cumulative unsuited']:
            rank = self.__get_rank('two pair')
            # for each two pair
            tp_gen = itertools.combinations(backwards_ranks, 2)
            for two_pair in tp_gen:
                pair1, pair2 = two_pair
                base_product = (card.PRIMES[pair1]**2 *
                                card.PRIMES[pair2]**2)
                kickers = backwards_ranks[:]
                kickers.remove(pair1)
                kickers.remove(pair2)
                combinations = list(itertools.combinations(
                    kickers, cards_for_hand - 4))
                # if at least one kicker exists
                if combinations[0]:
                    for combination in combinations:
                        product = base_product
                        # for each kicker multiply kicker prime onto
                        # base prime product
                        for kicker in combination:
                            product *= card.PRIMES[kicker]
                        self.unsuited_lookup[product] = rank
                        rank += 1
                else:
                    self.unsuited_lookup[base_product] = rank
                    rank += 1
            num_ranks = rank - self.__get_rank('two pair')
            assert (num_ranks == self.hand_dict['two pair']['unsuited'])

        if self.hand_dict['pair']['cumulative unsuited']:
            rank = self.__get_rank('pair')
            # for each pair
            for pair in backwards_ranks:
                base_product = card.PRIMES[pair]**2
                kickers = backwards_ranks[:]
                kickers.remove(pair)
                combinations = list(itertools.combinations(
                    kickers, cards_for_hand - 2))
                # if at least one kicker exists
                if combinations[0]:
                    for combination in combinations:
                        product = base_product
                        # for each kicker multiply kicker prime onto
                        # base prime product
                        for kicker in combination:
                            product *= card.PRIMES[kicker]
                        self.unsuited_lookup[product] = rank
                        rank += 1
                else:
                    self.unsuited_lookup[base_product] = rank
                    rank += 1
            num_ranks = rank - self.__get_rank('pair')
            assert (num_ranks == self.hand_dict['pair']['unsuited'])

    def __get_rank(self, hand):
        rank = self.hand_dict[hand]['rank']
        if not rank:
            return 0
        better_hand = self.ranked_hands[rank - 1]
        return self.hand_dict[better_hand]['cumulative unsuited'] + 1


def _lexographic_next_bit(bits):
    # generator next legographic bit sequence given a bit sequence with
    # N bits set e.g.
    # 00010011 -> 00010101 -> 00010110 -> 00011001 ->
    # 00011010 -> 00011100 -> 00100011 -> 00100101
    lex = bits
    yield lex
    while True:
        temp = (lex | (lex - 1)) + 1
        lex = temp | ((((temp & -temp) // (lex & -lex)) >> 1) - 1)
        yield lex


def _ncr(n, r):
    r = min(r, n-r)
    numer = functools.reduce(operator.mul, range(n, n-r, -1), 1)
    denom = functools.reduce(operator.mul, range(1, r+1), 1)
    return numer / denom
