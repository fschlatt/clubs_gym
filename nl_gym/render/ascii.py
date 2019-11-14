from .viewer import PokerViewer
from nl_gym.poker.deck import Card
import os


class ASCIIViewer(PokerViewer):

    POS_DICT = {2: [0, 5],
                3: [0, 3, 6],
                4: [0, 2, 4, 6],
                5: [0, 2, 4, 6, 8],
                6: [0, 1, 3, 5, 6, 8],
                7: [0, 1, 3, 5, 6, 7, 9],
                8: [0, 1, 2, 4, 5, 6, 7, 9],
                9: [0, 1, 2, 4, 5, 6, 7, 8, 9],
                10: list(range(10))}

    KEYS = (['p{}'.format(idx) for idx in range(10)]
            + ['p{}c'.format(idx) for idx in range(10)]
            + ['a{}'.format(idx) for idx in range(10)]
            + ['b{}'.format(idx) for idx in range(10)]
            + ['sb', 'bb', 'ccs', 'pot', 'action'])

    def __init__(self, num_players, num_hole_cards, num_community_cards):
        super(ASCIIViewer, self).__init__(
            num_players, num_hole_cards, num_community_cards)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open('{}/ascii_table.txt'.format(dir_path), 'r') as file:
            self.table = file.read()

        self.length = max([len(row) for row in self.table.split('\n')])

        self.player_pos = self.POS_DICT[num_players]

    def render(self, config):

        # TODO split pot for all ins
        action = config['action']
        dealer = config['dealer']
        done = config['done']

        str_config = {key: '' for key in self.KEYS}

        ccs = Card.int_to_str(config['community_cards'])
        ccs += ['--'] * (self.num_community_cards - len(ccs))
        ccs = '[' + ','.join(ccs) + ']'

        str_config['ccs'] = ccs
        if not done:
            str_config['pot'] = '{:,}'.format(config['pot'])
            str_config['a{}'.format(self.player_pos[action])] = 'X'
        else:
            str_config['pot'] = '0'
        str_config['b{}'.format(self.player_pos[dealer])] = 'D '
        if config['small_blind']:
            str_config['b{}'.format(
                self.player_pos[(dealer + 1) % self.num_players])] = 'SB'
        if config['big_blind'] and self.num_players > 2:
            str_config['b{}'.format(
                self.player_pos[(dealer + 2) % self.num_players])] = 'BB'

        players = []
        iterator = zip(
            config['hole_cards'], config['stacks'], config['active'])
        for idx, (hand, stack, active) in enumerate(iterator):
            if not active:
                players.append('{:2}. '.format(idx + 1) +
                               ','.join(['--']*self.num_hole_cards) +
                               ' {:,}'.format(stack))
                continue
            if done or idx == action:
                players.append('{:2}. '.format(idx + 1) +
                               ','.join(Card.int_to_str(hand)) +
                               ' {:,}'.format(stack))
                continue
            players.append('{:2}. '.format(idx + 1) +
                           ','.join(['??']*self.num_hole_cards) +
                           ' {:,}'.format(stack))

        positions = ['p{}'.format(idx) for idx in self.player_pos]
        iterator = zip(
            players, config['street_commits'], positions, config['all_in'])
        for player, street_commit, pos, all_in in iterator:
            str_config[pos] = player
            str_config[pos + 'c'] = '{:,}'.format(street_commit)
            if all_in and not done:
                str_config['a' + pos[:1]] = 'A'

        iterator = zip(
            config['payouts'], positions)
        if done:
            for payout, pos in iterator:
                str_config[pos + 'c'] = '{:,}'.format(payout)

        string = self.table.format(**str_config)
        print(string)
