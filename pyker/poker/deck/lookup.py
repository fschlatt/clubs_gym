'''
Lookup table which maps a hand's unique prime product to
unique hand rank
'''

import itertools
import operator as op
from functools import reduce

from .card import Card


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom


class LookupTable():
    '''
    Lookup table which maps a hand's unique prime product to
    unique hand rank
    Examples for 5 card hands:
    * Royal flush (best hand possible)          => 1
    * 7-5-4-3-2 unsuited (worst hand possible)  => 7462
    '''

    def __init__(self, suits, ranks, cards_for_hand):
        '''
        Calculates lookup tables
        '''
        # number of suited and unsuited possibilities of different hands
        straight_flushes, u_straight_flushes = self.__straight_flush(
            suits, ranks, cards_for_hand)
        four_of_a_kinds, u_four_of_a_kinds = self.__four_of_a_kind(
            suits, ranks, cards_for_hand)
        full_houses, u_full_houses = self.__full_house(
            suits, ranks, cards_for_hand)
        flushes, u_flushes = self.__flush(
            suits, ranks, cards_for_hand)
        straights, u_straights = self.__straight(
            suits, ranks, cards_for_hand)
        three_of_a_kinds, u_three_of_a_kinds = self.__three_of_a_kind(
            suits, ranks, cards_for_hand)
        two_pairs, u_two_pairs = self.__two_pair(
            suits, ranks, cards_for_hand)
        pairs, u_pairs = self.__pair(
            suits, ranks, cards_for_hand)
        high_cards, u_high_cards = self.__high_card(
            suits, ranks, cards_for_hand)

        self.hands = {
            'straight flush': {
                'suited': straight_flushes,
                'unsuited': u_straight_flushes},
            'four of a kind': {
                'suited': four_of_a_kinds,
                'unsuited': u_four_of_a_kinds},
            'full house': {
                'suited': full_houses,
                'unsuited': u_full_houses},
            'flush': {
                'suited': flushes,
                'unsuited': u_flushes},
            'straight': {
                'suited': straights,
                'unsuited': u_straights},
            'three of a kind': {
                'suited': three_of_a_kinds,
                'unsuited': u_three_of_a_kinds},
            'two pair': {
                'suited': two_pairs,
                'unsuited': u_two_pairs},
            'pair': {
                'suited': pairs,
                'unsuited': u_pairs},
            'high card': {
                'suited': high_cards,
                'unsuited': u_high_cards}
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
            (high_cards, 'high card')]

        # sort suited hands and rank unsuited hands by suited
        # rank order => lookup is done on unsuited hands but hand
        # rank is dependent on suited hands
        s_hands = sorted(s_hands)
        u_hands = [(self.hands[u_hand[1]]['unsuited'], u_hand[1])
                   for u_hand in s_hands]

        # compute cumulative number of unsuited hands for each hand
        # cumulative unsuited is the maximum rank a hand can have
        ranked_hands = []
        rank = 0
        cumulative_hands = 0
        for u_hand in u_hands:
            hand_rank = u_hand[1]
            cumulative_hands += u_hand[0]
            self.hands[hand_rank]['cumulative unsuited'] = cumulative_hands
            if cumulative_hands > 0:
                self.hands[hand_rank]['rank'] = rank
                rank += 1
                ranked_hands.append(hand_rank)

        # list of hands ordered by rank from best to worst
        self.hands['ranked hands'] = ranked_hands

        # create dictionaries
        self.flush_lookup = {}
        self.unsuited_lookup = {}

        # create the lookup table in piecewise fashion
        # this will call straights and high cards method,
        # we reuse some of the bit sequences
        self.__flushes(ranks, cards_for_hand)
        self.__multiples(ranks, cards_for_hand)

        # if suited hands aren't relevant set the suited
        # lookup table equal to the unsuited table
        if not self.hands['flush']['cumulative unsuited']:
            self.flush_lookup = self.unsuited_lookup

    def __straight_flush(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 3 or suits < 2:
            return 0, 0
        # number of smallest cards which start straight
        # add 1 for top and and bottom if ace included
        unsuited = ranks - (cards_for_hand - 1) + int(ranks == 13)
        # multiplied with number of suits
        suited = max(unsuited, unsuited * suits)
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __four_of_a_kind(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 4 or suits < 4:
            return 0, 0
        # choose 1 rank for quads multiplied by choice for 1 card from remaining rank
        unsuited = ncr(ranks, 1) * ncr(ranks - 1, cards_for_hand - 4)
        # mutliplied with number of suit choices for remaining cards
        suited = max(unsuited, unsuited * suits**(cards_for_hand - 4))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __full_house(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 5 or suits < 3:
            return 0, 0
        # choose one rank for trips and one rank for pair
        unsuited = ncr(ranks, 1) * ncr(ranks - 1, 1) * \
            ncr(ranks - 2, cards_for_hand - 5)
        # multiplied with number of suit choices for trips, pair and remaining cards
        suited = max(unsuited, unsuited * ncr(suits, 3) * ncr(suits, 2) *
                     suits**(cards_for_hand - 5))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __flush(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 3 or suits < 2:
            return 0, 0
        # all straight combinations
        straight_flushes = ranks - (cards_for_hand - 1) + int(ranks == 13)
        # choose all cards from ranks minus straight flushes
        unsuited = ncr(ranks, cards_for_hand) - straight_flushes
        # multiplied by number of suits
        suited = max(unsuited, unsuited * suits)
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __straight(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 3:
            return 0, 0
        # number of smallest cards which start straight
        # add 1 for low and high end ace straights
        unsuited = ranks - (cards_for_hand - 1) + 1
        # straight flush combinations
        straight_flushes = 0
        if suits > 1:
            straight_flushes = unsuited * suits
        # multiplied with suit choice for every card minus straight flushes
        suited = max(unsuited, unsuited * suits **
                     (cards_for_hand) - straight_flushes)
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __three_of_a_kind(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 3 or suits < 3:
            return 0, 0
        # choose one rank for trips and remaining cards from remaining ranks
        unsuited = ncr(ranks, 1) * ncr(ranks - 1, cards_for_hand - 3)
        # multiplied with suit choices for trips and suit choices for remaining cards
        suited = max(unsuited, unsuited * ncr(suits, 3) *
                     ncr(suits, 3)**(cards_for_hand - 3))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __two_pair(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 4 or suits < 2:
            return 0, 0
        # choose two ranks for pairs and ranks for remaining cards
        unsuited = ncr(ranks, 2) * ncr(ranks - 2, cards_for_hand - 4)
        # multiplied with suit choices for both pairs and suit choices for remaining cards
        suited = max(unsuited, unsuited * ncr(suits, 2)
                     ** 2 * suits**(cards_for_hand - 4))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __pair(self, suits, ranks, cards_for_hand):
        if cards_for_hand < 2 or suits < 2:
            return 0, 0
        # choose rank for pair and ranks for remaining cards
        unsuited = ncr(ranks, 1) * ncr(ranks - 1, cards_for_hand - 2)
        # multiplied with suit choices for pair and suit choices for remaining cards
        suited = max(unsuited, unsuited * ncr(suits, 2)
                     * suits**(cards_for_hand - 2))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __high_card(self, suits, ranks, cards_for_hand):
        # number of smallest cards which start straight
        # add 1 for top and bottom if ace included
        straights = 0
        if cards_for_hand > 2:
            straights = ranks - (cards_for_hand - 1) + int(ranks == 13)
        # any ncrination of rank and subtract straights
        unsuited = ncr(ranks, cards_for_hand) - straights
        # multiplied with suit choices for all cards, all same suits not allowed
        suited = max(unsuited, unsuited * (suits**cards_for_hand - suits))
        if suits < 2:
            suited = unsuited
        return int(suited), int(unsuited)

    def __flushes(self, ranks, cards_for_hand):
        '''
        Straight flushes and flushes.
        Lookup is done on 13 bit integer (2^13 > 7462):
        xxxbbbbb bbbbbbbb => integer hand index
        '''

        # straight flushes in rank order
        straight_flushes = []

        # if any straights/straight flushes exist in card configuration
        # create list of all possibilities
        if (self.hands['straight flush']['cumulative unsuited'] or
                self.hands['straight']['cumulative unsuited']):
            # start with best straight (flush)
            # for 5 card hand with 13 ranks: 0b1111100000000
            bin_num_str = '0b' + '1' * cards_for_hand + \
                '0' * (13 - cards_for_hand)
            # remove one 0 for every straight (flush)
            for _ in range(ranks - (cards_for_hand - 1)):
                straight_flushes.append(int(bin_num_str, 2))
                bin_num_str = bin_num_str[:-1]
            # add low end straight
            bin_num_str = '0b1' + '0' * \
                (13 - cards_for_hand) + '1' * (cards_for_hand - 1)
            straight_flushes.append(int(bin_num_str, 2))

        # if any flushes/high cards exist in card configuration
        # create list of all possibilities
        if (self.hands['flush']['cumulative unsuited'] or
                self.hands['high card']['cumulative unsuited']):
            # dynamically generate all the other
            # flushes (including straight flushes)
            flushes = []
            # start with lowest non pair hand
            # for 5 card hand with 13 ranks: 0b11111
            bin_num_str = '0b' + ('1' * cards_for_hand)
            gen = self.__lexographic_next_bit(
                int(bin_num_str, 2))
            # iterate over all possibilities of unique hands
            for _ in range(int(ncr(ranks, cards_for_hand))):
                # pull the next flush pattern from our generator
                flush = next(gen) << (13 - ranks)

                # if this flush matches perfectly any
                # straight flush, do not add it
                not_straight_flush = True
                for straight_flush in straight_flushes:
                    # if flush XOR straight_flush == 0, then bit pattern
                    # is same, and we should not add
                    if not flush ^ straight_flush:
                        not_straight_flush = False

                if not_straight_flush:
                    flushes.append(flush)

        # we started from the lowest straight pattern, now we want to start ranking from
        # the most powerful hands, so we reverse
        flushes.reverse()

        # now add to the lookup map:
        # start with straight flushes and the rank of 1
        # since it is the best hand in poker
        # rank 1 = Royal Flush!
        if self.hands['straight flush']['cumulative unsuited']:
            rank = self.__get_rank('straight flush')
            for straight_flush in straight_flushes:
                prime_product = Card.prime_product_from_rankbits(
                    straight_flush)
                self.flush_lookup[prime_product] = rank
                rank += 1

        # we start the counting for flushes on max full house, which
        # is the worst rank that a full house can have (2,2,2,3,3)
        if self.hands['flush']['cumulative unsuited']:
            rank = self.__get_rank('flush')
            for flush in flushes:
                prime_product = Card.prime_product_from_rankbits(flush)
                self.flush_lookup[prime_product] = rank
                rank += 1

        # we can reuse these bit sequences for straights
        # and high cards since they are inherently related
        # and differ only by context
        self.__straight_and_highcards(straight_flushes, flushes)

    def __straight_and_highcards(self, straights, highcards):
        '''
        Unique five card sets. Straights and highcards.
        Reuses bit sequences from flush calculations.
        '''

        if self.hands['straight']['cumulative unsuited']:
            rank = self.__get_rank('straight')
            for straight in straights:
                prime_product = Card.prime_product_from_rankbits(straight)
                self.unsuited_lookup[prime_product] = rank
                rank += 1

        if self.hands['high card']['cumulative unsuited']:
            rank = self.__get_rank('high card')
            for high_card in highcards:
                prime_product = Card.prime_product_from_rankbits(high_card)
                self.unsuited_lookup[prime_product] = rank
                rank += 1

    def __multiples(self, ranks, cards_for_hand):
        '''
        Pair, Two Pair, Three of a Kind, Full House, and 4 of a Kind.
        '''
        backwards_ranks = list(range(13 - 1, 13 - 1 - ranks, -1))

        # 1) Four of a Kind

        if self.hands['four of a kind']['cumulative unsuited']:
            rank = self.__get_rank('four of a kind')
            # for each choice of a set of four rank
            for idx in backwards_ranks:
                # compute prime product for selected rank
                base_product = Card.PRIMES[idx]**4

                # and for each possible ncrination of kicker ranks
                kickers = backwards_ranks[:]
                kickers.remove(idx)
                combinations = list(itertools.combinations(
                    kickers, cards_for_hand - 4))
                # if at least one kicker exists
                if combinations[0]:
                    for ncrination in combinations:
                        product = base_product
                        # for each kicker multiply kicker prime onto
                        # base prime product
                        for kicker in ncrination:
                            product *= Card.PRIMES[kicker]
                        self.unsuited_lookup[product] = rank
                        rank += 1
                else:
                    self.unsuited_lookup[base_product] = rank
                    rank += 1

        # 2) Full House
        if self.hands['full house']['cumulative unsuited']:
            rank = self.__get_rank('full house')
            # for each three of a kind
            for idx in backwards_ranks:

                # and for each choice of pair rank
                pairranks = backwards_ranks[:]
                pairranks.remove(idx)
                for pair_rank in pairranks:
                    base_product = Card.PRIMES[idx]**3 * \
                        Card.PRIMES[pair_rank]**2

                    pairranks.remove(pair_rank)
                    combinations = list(itertools.combinations(
                        pairranks, cards_for_hand - 5))
                    # if at least one kicker exists
                    if combinations[0]:
                        for ncrination in combinations:
                            product = base_product
                            # for each kicker multiply kicker prime onto
                            # base prime product
                            for kicker in ncrination:
                                product *= Card.PRIMES[kicker]
                            self.unsuited_lookup[product] = rank
                            rank += 1
                    else:
                        self.unsuited_lookup[base_product] = rank
                        rank += 1

        # 3) Three of a Kind
        # pick three of one rank
        if self.hands['three of a kind']['cumulative unsuited']:
            rank = self.__get_rank('three of a kind')
            for three_of_a_kind in backwards_ranks:

                base_product = Card.PRIMES[three_of_a_kind]**3

                kickers = backwards_ranks[:]
                kickers.remove(three_of_a_kind)
                combinations = list(itertools.combinations(
                    kickers, cards_for_hand - 3))

                if combinations[0]:
                    for ncrination in combinations:
                        product = base_product
                        # for each kicker multiply kicker prime onto
                        # base prime product
                        for kicker in ncrination:
                            product *= Card.PRIMES[kicker]
                        self.unsuited_lookup[product] = rank
                        rank += 1
                else:
                    self.unsuited_lookup[base_product] = rank
                    rank += 1

        # 4) Two Pair
        if self.hands['two pair']['cumulative unsuited']:
            rank = self.__get_rank('two pair')
            # choose two pairs
            tpgen = itertools.combinations(backwards_ranks, 2)
            for two_pair in tpgen:
                pair1, pair2 = two_pair
                base_product = Card.PRIMES[pair1]**2 * Card.PRIMES[pair2]**2

                kickers = backwards_ranks[:]
                kickers.remove(pair1)
                kickers.remove(pair2)
                combinations = list(itertools.combinations(
                    kickers, cards_for_hand - 4))
                if combinations[0]:
                    for ncrination in combinations:
                        product = base_product
                        # for each kicker multiply kicker prime onto
                        # base prime product
                        for kicker in ncrination:
                            product *= Card.PRIMES[kicker]
                        self.unsuited_lookup[product] = rank
                        rank += 1
                else:
                    self.unsuited_lookup[base_product] = rank
                    rank += 1

        # 5) Pair
        # choose a pair
        if self.hands['pair']['cumulative unsuited']:
            rank = self.__get_rank('pair')
            for pairrank in backwards_ranks:

                base_product = Card.PRIMES[pairrank]**2

                kickers = backwards_ranks[:]
                kickers.remove(pairrank)
                combinations = list(itertools.combinations(
                    kickers, cards_for_hand - 2))

                if combinations[0]:
                    for ncrination in combinations:
                        product = base_product
                        # for each kicker multiply kicker prime onto
                        # base prime product
                        for kicker in ncrination:
                            product *= Card.PRIMES[kicker]
                        self.unsuited_lookup[product] = rank
                        rank += 1
                else:
                    self.unsuited_lookup[base_product] = rank
                    rank += 1

    def write_table_to_disk(self, table, filepath):
        '''
        Writes lookup table to disk
        '''
        with open(filepath, 'w') as ofile:
            for prime_prod, rank in table.iteritems():
                ofile.write(str(prime_prod) + ',' + str(rank) + '\n')

    def __get_rank(self, hand):
        rank = self.hands[hand]['rank']
        if rank == 0:
            return 0
        better_hand = self.hands['ranked hands'][rank - 1]
        return self.hands[better_hand]['cumulative unsuited'] + 1

    def __lexographic_next_bit(self, bits):
        '''
        Bit hack from here:
        http://www.graphics.stanford.edu/~seander/bithacks.html#NextBitPermutation
        Generator even does this in poker order rank
        so no need to sort when done! Perfect.
        '''
        lex = bits
        yield lex
        while True:
            temp = (lex | (lex - 1)) + 1
            lex = temp | ((((temp & -temp) // (lex & -lex)) >> 1) - 1)
            yield lex
