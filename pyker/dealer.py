import numpy as np

from pyker import deuces, render


class Dealer():

    def __init__(self, num_players, num_streets, small_blind, big_blind,
                 ante, raise_size, num_raises, num_suits, num_ranks,
                 num_hole_cards, num_community_cards, num_cards_for_hand,
                 mandatory_num_hole_cards, start_stack):

        self.num_players = num_players
        self.num_streets = num_streets
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.ante = ante
        self.raise_size = raise_size
        self.num_raises = num_raises
        self.num_suits = num_suits
        self.num_ranks = num_ranks
        self.num_hole_cards = num_hole_cards
        self.num_community_cards = num_community_cards
        self.num_cards_for_hand = num_cards_for_hand
        self.mandatory_num_hole_cards = mandatory_num_hole_cards
        self.start_stack = start_stack

        if not isinstance(self.raise_size, list):
            self.raise_size = [self.raise_size] * self.num_streets
        if not isinstance(self.num_raises, list):
            self.num_raises = [self.num_raises] * self.num_streets

        def _parse_raise_size(raise_size):
            if isinstance(raise_size, int):
                return raise_size
            if raise_size.endswith('bb'):
                factor = int(raise_size.split('bb')[0])
                return self.big_blind * factor
            if raise_size == 'inf':
                return float(raise_size)
            if raise_size == 'pot':
                return raise_size
            raise ValueError(f'unkown raise size {raise_size}')

        self.raise_size = [
            _parse_raise_size(raise_size)
            for raise_size in self.raise_size]

        self.num_raises = [
            float(num_raises)
            for num_raises in self.num_raises]

        self.action = 0
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

        self.done = np.zeros(self.num_players, dtype=np.uint8)
        self.observation = {}
        self.rewards = np.zeros(self.num_players, dtype=np.uint8)
        self.info = None

        self.viewer = None

    def reset(self, reset_stacks, reset_button):
        self.deck.shuffle()

        if reset_stacks:
            self.active.fill(1)
            self.stacks = np.full(self.num_players, self.start_stack)
        else:
            self.active = self.stacks > 0
        if reset_button:
            self.button = 0
        else:
            self.button = self.button % self.num_players

        # in heads up button posts small blind
        if self.num_players > 2:
            self.action = self.button + 1 % self.num_players
        else:
            self.action = self.button

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

        self.__collect_ante()
        self.__collect_blinds()

        self.observation = self.__create_observation()
        return self.observation

    def step(self, action):

        fold = round(action['fold'])
        bet = round(action['bet'])

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
            self.street += 1
            if self.street < self.num_streets:
                self.community_cards += self.deck.draw(
                    self.num_community_cards[self.street])
            self.street_commits.fill(0)
            self.street_option = np.logical_not(self.active).astype(np.uint8)
            self.street_raises = 0

        self.done = self.__create_done()
        self.observation = self.__create_observation()
        self.rewards = self.__create_reward()
        self.info = None

        return self.observation, self.rewards, self.done, self.info

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
        all_in = self.active & (self.stacks > 0)
        big_blind = bool(self.big_blind)
        community_cards = self.community_cards
        dealer = self.button
        done = self.done.all()
        hole_cards = self.hole_cards
        pot = self.pot
        payouts = self.rewards
        street_commits = self.street_commits
        small_blind = bool(self.small_blind)
        stacks = self.stacks

        config = {
            'action': action,
            'active': active,
            'all_in': all_in,
            'big_blind': big_blind,
            'community_cards': community_cards,
            'dealer': dealer,
            'done': done,
            'hole_cards': hole_cards,
            'pot': pot,
            'payouts': payouts,
            'prev_action': None if not self.history else self.history[-1],
            'street_commits': street_commits,
            'small_blind': small_blind,
            'stacks': stacks,
        }

        self.viewer.render(config)

    def __all_agreed(self):
        # not all agreed if not all players had chance to act
        if not self.street_option.all():
            return False
        # all agreed if street commits equal to maximum street commit
        # or player is all in
        # or player is not active
        return ((self.street_commits == self.street_commits.max()) |
                (self.stacks == 0) |
                np.logical_not(self.active)).all()

    def __collect_ante(self):
        bets = (self.stacks > 0) * self.active * self.ante
        self.pot_commit += bets
        self.pot += bets.sum()
        self.stacks -= bets

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
        # pessimistic approach: in ties order is fold -> call -> raise
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

    def __collect_blinds(self):
        self.__collect_bet(self.small_blind)
        self.__move_action()
        self.__collect_bet(self.big_blind)
        self.__move_action()

    def __collect_bet(self, bet):
        # bet only as large as stack size
        bet = min(self.stacks[self.action], bet)

        self.pot += bet
        self.pot_commit[self.action] += bet
        self.street_commits[self.action] += bet
        self.stacks[self.action] -= bet

    def __create_done(self):
        if self.street == self.num_streets or self.active.sum() <= 1:
            # end game
            return np.full(self.num_players, 1)
        return np.logical_not(self.active)

    def __create_observation(self):
        if self.done.all():
            call = min_raise = max_raise = 0
        else:
            call, min_raise, max_raise = self.__bet_sizes()
        observation = {'action': self.action,
                       'active': self.active,
                       'button': self.button,
                       'call': call,
                       'community_cards': [
                           deuces.Card.int_to_pretty_str(card)
                           for card in self.community_cards],
                       'hole_cards': [
                           deuces.Card.int_to_pretty_str(card)
                           for card in self.hole_cards[self.action]],
                       'max_raise': max_raise,
                       'min_raise': min_raise,
                       'pot': self.pot,
                       'stacks': self.stacks,
                       'street_commits': self.street_commits}
        return observation

    def __create_reward(self):
        # players that have folded lose their bets
        rewards = -1 * self.pot_commit * np.logical_not(self.active)
        if self.active.sum() <= 1:
            return rewards + self.active * self.pot
        # if last street played and 
        # still players multiple players active
        if self.street == self.num_streets:
            rewards = self.__eval_round()
        rewards -= self.pot_commit
        return rewards

    def __eval_round(self):
        # grab array of hand strength and pot commits
        worst_hand = self.evaluator.table.max_rank + 1
        hands = []
        rewards = np.zeros(self.num_players, dtype=int)
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
            split_pot = cut.sum()
            split = split_pot // len(eligible)
            remain = split_pot % len(eligible)
            rewards[eligible] += split
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
            involved_players = np.nonzero(rewards)[0]
            button_shift = (involved_players <= self.button) * self.num_players
            button_shifted_players = involved_players + button_shift
            worst_idx = np.argmin(button_shifted_players)
            worst_pos = involved_players[worst_idx]
            rewards[worst_pos] += remainder
        return rewards

    def __move_action(self):
        for idx in range(1, self.num_players+1):
            action = (self.action + idx) % self.num_players
            if self.active[action]:
                break
            else:
                self.street_option[action] = True
        self.action = action
