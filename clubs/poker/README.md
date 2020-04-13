# Poker

## Card

Every card is represented as a single 32 bit integer with particular bits activated. The first 8 are used for the unique prime number of every rank, the following 4 for the rank in binary form, the next 4 represent the bit wise suit and the final 16 the bit wise rank. See the diagram below for details.

          bitrank     suit rank   prime
    +--------+--------+--------+--------+
    |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
    +--------+--------+--------+--------+

    1) p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
    2) r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
    3) cdhs = suit of card (bit turned on based on suit of card)
    4) b = bit turned on depending on rank of card
    5) x = unused

The 32 bit integer representation enables fast hand evaluation by avoiding object instantiation and allowing for efficient lookup for both suited and unsuited hands.

## Lookup Table

A lookup table for all possible hands is pre generated based on the number of ranks and suits in the deck as well as the number of cards used in a hand. To rank the hands, the number of possibilities for each hand need to be computed. If a hand is not possible for a certain deck configuration (e.g. full house if only 2 cards are used for a hand) it is not regarded. Hands are ranked by rarity (or by the order provided by the user) - the more unlikely a hand the lower the rank, i.e. lower rank is a better hand. The number of possibilities for each hand is then used to generate two separate look up tables, one for suited hands (flushes and straight flushes) and the other for all other hands. This lowers the size of the look up tables drastically. Hand ranking is done on the full range of hands, including suits, but the lookup disregards suits and only considers the ranks of cards (2598960 suited hand possibilities vs 7462 unsuited hand possibilities for full deck 5 card hands).

Both lookup tables work the same way. For every possible bit rank configuration of a hand, the unique prime product is computed. The total rank of that hand is then computed by subtracting the rank of the hand within in it's rank class from the highest rank of the hand class. Sounds more confusing than it is, so here an example: the full list of prime numbers for the 13 rank deck is `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]`. A full house with kings full of queens then has the unique prime product `37 * 37 * 37 * 31 * 31 = 48677533`. The best full house, aces full of kings, has a rank of 167. A full house with kings full of queens is the 13th best full house, therefore the rank of kings full of queens is `167 + 13 = 180`. The lookup table then saves the prime product as the key and the rank as the value `unsuited_lookup[4877533] = 180`.

To evaluate a hand, first the hand is checked for "suitedness" to determine if the suited or unsuited lookup table should be used. Then the prime product of the hand is computed and the rank taken from the lookup table.
