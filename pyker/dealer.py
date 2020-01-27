import numpy as np

from pyker import deuces, render


class Dealer():

    def __init__(self, num_players, num_streets, blinds,
                 antes, raise_size, num_raises, num_suits, num_ranks,
                 num_hole_cards, num_community_cards, num_cards_for_hand,
                 mandatory_num_hole_cards, start_stack):

        if isinstance(raise_size, list):
            assert len(raise_size) == num_streets
        else:
            raise_size = [raise_size] * num_streets
        if isinstance(num_raises, list):
            assert len(num_raises) == num_streets
        else:
            num_raises = [num_raises] * num_streets
        if isinstance(blinds, list):
            assert len(blinds) == num_players
        else:
            blinds = [blinds] * num_players
        if isinstance(antes, list):
            assert len(antes) == num_players
        else:
            antes = [antes] * num_players

        def clean_rs(_raise_size):
            if isinstance(_raise_size, int):
                return _raise_size
            if _raise_size.endswith('bb'):
                factor = int(_raise_size.split('bb')[0])
                return self.big_blind * factor
            if _raise_size == 'inf':
                return float(_raise_size)
            if _raise_size == 'pot':
                return _raise_size
            raise ValueError(f'unkown raise size {_raise_size}')

        # config
        self.num_players = num_players
        self.num_streets = num_streets
        self.blinds = np.array(blinds)
        self.antes = np.array(antes)
        self.big_blind = blinds[1]
        self.antes = antes
        self.raise_size = [clean_rs(_raise_size) for _raise_size in raise_size]
        self.num_raises = [float(_num_raises) for _num_raises in num_raises]
        self.num_suits = num_suits
        self.num_ranks = num_ranks
        self.num_hole_cards = num_hole_cards
        self.num_community_cards = num_community_cards
        self.num_cards_for_hand = num_cards_for_hand
        self.mandatory_num_hole_cards = mandatory_num_hole_cards
        self.start_stack = start_stack

        # dealer
        self.action = -1
        self.active = np.ones(self.num_players, dtype=np.uint8)
        self.button = 0
        self.community_cards = []
        self.deck = deuces.Deck(self.num_suits, self.num_ranks)
        self.evaluator = deuces.Evaluator(
            self.num_suits, self.num_ranks, self.num_hole_cards,
            self.num_cards_for_hand, self.mandatory_num_hole_cards)
        self.history = []
        self.hole_cards = []
        self.largest_raise = 0
        self.pot = 0
        self.pot_commit = np.zeros(self.num_players, dtype=np.int32)
        self.stacks = np.full(
            self.num_players, self.start_stack, dtype=np.int32)
        self.street = 0
        self.street_commits = np.zeros(self.num_players, dtype=np.int32)
        self.street_option = np.zeros(self.num_players, dtype=np.uint8)
        self.street_raises = 0

        # render
        self.viewer = None

    def reset(self, reset_button, reset_stacks):
        if reset_stacks:
            self.active.fill(1)
            self.stacks = np.full(self.num_players, self.start_stack)
        else:
            self.active = self.stacks > 0
            if sum(self.active) <= 1:
                raise RuntimeError(
                    'not enough players have chips, set reset_stacks=True')
        if reset_button:
            self.button = 0
        else:
            self.button = self.button + 1 % self.num_players

        self.deck.shuffle()
        self.community_cards = self.deck.draw(self.num_community_cards[0])
        self.history = []
        self.hole_cards = [self.deck.draw(
            self.num_hole_cards) for _ in range(self.num_players)]
        self.largest_raise = self.big_blind
        self.pot = 0
        self.pot_commit.fill(0)
        self.street = 0
        self.street_commits.fill(0)
        self.street_option.fill(0)
        self.street_raises = 0

        self.action = self.button
        # in heads up button posts small blind
        if self.num_players > 2:
            self.__move_action()
        self.__collect_multiple_bets(bets=self.antes, street_commits=False)
        self.__collect_multiple_bets(bets=self.blinds, street_commits=True)
        self.__move_action()
        self.__move_action()

        return self.__observation()

    def step(self, bet):

        if self.action == -1:
            if any(self.active):
                return self.__output()
            else:
                raise RuntimeError('call reset before calling first step')

        fold = bet < 0
        bet = round(bet)

        call, min_raise, max_raise = self.__bet_sizes()
        # round bet to nearest sizing
        bet = self.__clean_bet(bet, call, min_raise, max_raise)

        # only fold if player cannot check
        if call and ((bet < call) or fold):
            self.active[self.action] = 0
            bet = 0

        # if bet is full raise record as largest raise
        if bet and (bet - call) > self.largest_raise:
            self.largest_raise = bet - call
            self.street_raises += 1

        self.__collect_bet(bet)

        self.history.append([self.action, bet, fold])

        self.street_option[self.action] = True
        self.__move_action()

        # if all agreed go to next street
        if self.__all_agreed():
            self.action = self.button
            self.__move_action()
            # if at most 1 player active and not all in turn up all
            # community cards and evaluate hand
            while True:
                self.street += 1
                full_streets = self.street >= self.num_streets
                all_in = self.active * (self.stacks == 0)
                all_all_in = sum(self.active) - sum(all_in) <= 1
                if full_streets:
                    break
                self.community_cards += self.deck.draw(
                    self.num_community_cards[self.street])
                if not all_all_in:
                    break
            self.street_commits.fill(0)
            self.street_option = np.logical_not(self.active).astype(np.uint8)
            self.street_raises = 0

        observation, payouts, done, info = self.__output()
        if all(done):
            self.action = -1
            observation['action'] = -1
        return observation, payouts, done, info

    def render(self, mode='ascii'):
        if self.viewer is None:
            if mode == 'ascii':
                self.viewer = render.ASCIIViewer(
                    self.num_players,
                    self.num_hole_cards,
                    sum(self.num_community_cards))
            elif mode == 'asciimatics':
                self.viewer = render.AsciimaticsViewer(
                    self.num_players,
                    self.num_hole_cards,
                    sum(self.num_community_cards))
            else:
                render_modes = ', '.join(['ascii', 'asciimatics'])
                raise Exception(
                    (f'incorrect render mode {mode},'
                     f'use one of[{render_modes}]'))

        action = self.action
        active = self.active
        all_in = self.active * (self.stacks == 0)
        community_cards = self.community_cards
        dealer = self.button
        done = all(self.__done())
        hole_cards = self.hole_cards
        pot = self.pot
        payouts = self.__payouts()
        street_commits = self.street_commits
        stacks = self.stacks

        config = {
            'action': action,
            'active': active,
            'all_in': all_in,
            'community_cards': community_cards,
            'dealer': dealer,
            'done': done,
            'hole_cards': hole_cards,
            'pot': pot,
            'payouts': payouts,
            'prev_action': None if not self.history else self.history[-1],
            'street_commits': street_commits,
            'stacks': stacks,
        }

        self.viewer.render(config)

    def __all_agreed(self):
        # not all agreed if not all players had chance to act
        if not all(self.street_option):
            return False
        # all agreed if street commits equal to maximum street commit
        # or player is all in
        # or player is not active
        return all((self.street_commits == self.street_commits.max()) |
                   (self.stacks == 0) |
                   np.logical_not(self.active))

    def __bet_sizes(self):
        # call difference between commit and maximum commit
        call = self.street_commits.max() - self.street_commits[self.action]
        # min raise at least largest previous raise
        # if limit game min and max raise equal to raise size
        if isinstance(self.raise_size[self.street], int):
            max_raise = min_raise = self.raise_size[self.street] + call
        else:
            min_raise = max(self.big_blind, self.largest_raise + call)
            if self.raise_size[self.street] == 'pot':
                max_raise = self.pot + call * 2
            elif self.raise_size[self.street] == float('inf'):
                max_raise = self.stacks[self.action]
        # if maximum number of raises in street
        # was reached cap raise at 0
        if self.street_raises >= self.num_raises[self.street]:
            min_raise = max_raise = 0
        # if last full raise was done by active player
        # (another player has raised less than minimum raise amount)
        # cap active players raise size to 0
        if self.street_raises and call < self.largest_raise:
            min_raise = max_raise = 0
        # clip bets to stack size
        call = min(call, self.stacks[self.action])
        min_raise = min(min_raise, self.stacks[self.action])
        max_raise = min(max_raise, self.stacks[self.action])
        return call, min_raise, max_raise

    @staticmethod
    def __clean_bet(bet, call, min_raise, max_raise):
        # find closest bet size to actual bet
        # pessimistic approach: in ties order is fold/check -> call -> raise
        idx = np.argmin(np.absolute(
            np.array([0, call, min_raise, max_raise]) - bet))
        # if call closest
        if idx == 1:
            return call
        # if min raise or max raise closest
        if idx in (2, 3):
            return round(min(max_raise, max(min_raise, bet)))
        # if fold closest
        return 0

    def __collect_multiple_bets(self, bets, street_commits=True):
        bets = np.roll(bets, self.action)
        bets = (self.stacks > 0) * self.active * bets
        if street_commits:
            self.street_commits += bets
        self.pot_commit += bets
        self.pot += sum(bets)
        self.stacks -= bets

    def __collect_bet(self, bet):
        # bet only as large as stack size
        bet = min(self.stacks[self.action], bet)

        self.pot += bet
        self.pot_commit[self.action] += bet
        self.street_commits[self.action] += bet
        self.stacks[self.action] -= bet

    def __done(self):
        if self.street >= self.num_streets or sum(self.active) <= 1:
            # end game
            return np.full(self.num_players, 1)
        return np.logical_not(self.active)

    def __observation(self):
        if all(self.__done()):
            call = min_raise = max_raise = 0
        else:
            call, min_raise, max_raise = self.__bet_sizes()
        observation = {'action': self.action,
                       'active': self.active,
                       'button': self.button,
                       'call': call,
                       'community_cards': [
                           str(card)
                           for card in self.community_cards],
                       'hole_cards': [
                           str(card)
                           for card in self.hole_cards[self.action]],
                       'max_raise': max_raise,
                       'min_raise': min_raise,
                       'pot': self.pot,
                       'stacks': self.stacks,
                       'street_commits': self.street_commits}
        return observation

    def __payouts(self):
        # players that have folded lose their bets
        payouts = -1 * self.pot_commit * np.logical_not(self.active)
        if sum(self.active) == 1:
            payouts += self.active * (self.pot - self.pot_commit)
        # if last street played and still multiple players active
        elif self.street >= self.num_streets:
            payouts = self.__eval_round()
            payouts -= self.pot_commit
        if any(payouts > 0):
            self.stacks += payouts + self.pot_commit
        return payouts

    def __output(self):
        observation = self.__observation()
        payouts = self.__payouts()
        done = self.__done()
        info = None
        return observation, payouts, done, info

    def __eval_round(self):
        # grab array of hand strength and pot commits
        worst_hand = self.evaluator.table.max_rank + 1
        hands = []
        payouts = np.zeros(self.num_players, dtype=int)
        for player in range(self.num_players):
            # if not active hand strength set
            # to 1 worse than worst possible rank
            hand_strength = worst_hand
            if self.active[player]:
                hand_strength = self.evaluator.evaluate(
                    self.hole_cards[player], self.community_cards)
            hands.append([player, hand_strength, self.pot_commit[player]])
        hands = np.array(hands)
        # sort hands by hand strength and pot commits
        hands = hands[np.lexsort([hands[:, 2], hands[:, 1]])]
        pot = self.pot
        remainder = 0
        # iterate over hand strength and
        # pot commits from smallest to largest
        for idx, (_, strength, pot_commit) in enumerate(hands):
            eligible = hands[:, 0][hands[:, 1] == strength].astype(int)
            # cut can only be as large as lowest player commit amount
            cut = np.clip(hands[:, 2], None, pot_commit)
            split_pot = sum(cut)
            split = split_pot // len(eligible)
            remain = split_pot % len(eligible)
            payouts[eligible] += split
            remainder += remain
            # remove chips from players and pot
            hands[:, 2] -= cut
            pot -= split_pot
            # remove player from next split pot
            hands[idx, 1] = worst_hand
            if pot == 0:
                break

        # give worst position player remainder chips
        if remainder:
            # worst player is first player after button involved in pot
            involved_players = np.nonzero(payouts)[0]
            button_shift = (involved_players <= self.button) * self.num_players
            button_shifted_players = involved_players + button_shift
            worst_idx = np.argmin(button_shifted_players)
            worst_pos = involved_players[worst_idx]
            payouts[worst_pos] += remainder
        return payouts

    def __move_action(self):
        for idx in range(1, self.num_players + 1):
            action = (self.action + idx) % self.num_players
            if self.active[action]:
                break
            else:
                self.street_option[action] = True
        self.action = action
