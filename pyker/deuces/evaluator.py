import functools
import itertools
import operator

from . import card, lookup


class Evaluator(object):
    '''
    Evaluates hand strengths using a variant of Cactus Kev's algorithm:
    http://suffe.cool/poker/evaluator.html

    I make considerable optimizations in terms of speed and memory usage,
    in fact the lookup table generation can be done in under a second and
    consequent evaluations are very fast. Won't beat C, but very fast as
    all calculations are done with bit arithmetic and table lookups.
    '''

    def __init__(self, suits, ranks, h_cards, cards_for_hand, mandatory_h_cards):

        if cards_for_hand < 0 or cards_for_hand > 5:
            raise NotImplementedError(
                'Evaluation not implemented for %s card hands' % (cards_for_hand))

        self.suits = suits
        self.ranks = ranks
        self.h_cards = h_cards
        self.cards_for_hand = cards_for_hand
        self.mandatory_h_cards = mandatory_h_cards

        self.table = lookup.LookupTable(suits, ranks, cards_for_hand)

        hands = ['{} ({})'.format(hand, self.table.hands[hand]['suited'])
                 for hand in self.table.hands['ranked hands']]
        self.ranks = ' > '.join(hands)

    def evaluate(self, cards, board):
        '''
        This is the function that the user calls to get a hand rank.

        Supports empty board, etc very flexible. No input validation
        because that's cycles!
        '''

        # compute all possible hand combinations
        all_card_combs = []
        # if a number of hole cards are mandatory
        if self.mandatory_h_cards:
            num_board_cards = self.cards_for_hand - self.mandatory_h_cards
            # get all hole card combinations
            h_cards_combs = list(itertools.combinations(
                cards, self.mandatory_h_cards))
            # and board card combinations
            b_cards_combs = list(
                itertools.combinations(board, num_board_cards))
            # and combine them together
            for h_cards_comb in h_cards_combs:
                for b_cards_comb in b_cards_combs:
                    all_card_combs.append(h_cards_comb + b_cards_comb)
        # else create combinations from all cards
        else:
            all_cards = cards + board
            all_card_combs = itertools.combinations(
                all_cards, self.cards_for_hand)

        worst_hand = self.table.hands['ranked hands'][-1]
        minimum = self.table.hands[worst_hand]['cumulative unsuited']

        for card_comb in all_card_combs:
            score = self.__lookup(list(card_comb))
            if score < minimum:
                minimum = score
        return minimum

    def __lookup(self, cards):
        '''
        Performs an evalution given cards in integer form, mapping them to
        a rank dependent on number of cards and suits in the deck. Lower ranks
        are better
        '''
        # if flush
        if functools.reduce(operator.and_, cards + [0xF000]):
            hand_or = functools.reduce(operator.or_, cards) >> 16
            prime = card.Card.prime_product_from_rankbits(hand_or)
            return self.table.flush_lookup[prime]

        # otherwise
        else:
            prime = card.Card.prime_product_from_hand(cards)
            return self.table.unsuited_lookup[prime]

    def get_rank_class(self, hr):
        '''
        Returns the class of hand given the hand hand_rank
        returned from evaluate
        '''

        hands = self.table.hands

        rank = None
        for hand in hands['ranked hands']:
            if hr >= 0 and hr <= hands[hand]['cumulative unsuited']:
                rank = hands[hand]['rank']
                break
        if rank is not None:
            return rank
        else:
            raise Exception('Inavlid hand rank, cannot return rank class')

    def get_rank_string(self, hr):
        '''
        Returns the string of the hand for a given hand rank
        '''
        hands = self.table.hands

        rank = None
        for hand in hands['ranked hands']:
            if not hands[hand]['cumulative unsuited']:
                continue
            if hr >= 0 and hr <= hands[hand]['cumulative unsuited']:
                rank = hand
                break
        if rank is not None:
            return rank
        else:
            raise Exception('Inavlid hand rank, cannot return rank class')

    def get_five_card_rank_percentage(self, hand_rank):
        '''
        Scales the hand rank score to the [0.0, 1.0] range.
        '''
        worst_hand = self.table.hands['ranked hands'][-1]
        worst_hand_rank = self.table.hands[worst_hand]['cumulative unsuited']
        return float(hand_rank) / float(worst_hand_rank)
