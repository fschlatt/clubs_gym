"""Classes and functions for running poker games"""
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import numpy as np

from clubs import error, poker, render


class Dealer:
    """Runs a range of different of poker games dependent on the
    given configuration. Supports limit, no limit and pot limit
    bet sizing, arbitrary deck sizes, arbitrary hole and community
    cards and many other options.

    Parameters
    ----------
    num_players : int
        maximum number of players
    num_streets : int
        number of streets including preflop, e.g. for texas hold'em
        num_streets=4
    blinds : Union[int, List[int]]
        blind distribution as a list of ints, one for each player
        starting from the button e.g. [0, 1, 2] for a three player game
        with a sb of 1 and bb of 2, passed ints will be expanded to
        all players i.e. pass blinds=0 for no blinds
    antes : Union[int, List[int]]
        ante distribution as a list of ints, one for each player
        starting from the button e.g. [0, 0, 5] for a three player game
        with a bb ante of 5, passed ints will be expanded to all
        players i.e. pass antes=0 for no antes
    raise_sizes : Union[float, str, List[Union[float, str]]]
        max raise sizes for each street, valid raise sizes are ints,
        floats, and 'pot', e.g. for a 1-2 limit hold'em the raise sizes
        should be [2, 2, 4, 4] as the small and big bet are 2 and 4.
        float('inf') can be used for no limit games. pot limit raise
        sizes can be set using 'pot'. if only a single int, float or
        string is passed the value is expanded to a list the length
        of number of streets, e.g. for a standard no limit game pass
        raise_sizes=float('inf')
    num_raises : Union[float, List[float]]
        max number of bets for each street including preflop, valid
        raise numbers are ints and floats. if only a single int or float
        is passed the value is expanded to a list the length of number
        of streets, e.g. for a standard limit game pass num_raises=4
    num_suits : int
        number of suits to use in deck, must be between 1 and 4
    num_ranks : int
        number of ranks to use in deck, must be between 1 and 13
    num_hole_cards : int
        number of hole cards per player, must be greater than 0
    num_community_cards : Union[int, List[int]]
        number of community cards per street including preflop, e.g.
        for texas hold'em pass num_community_cards=[0, 3, 1, 1]. if only
        a single int is passed, it is expanded to a list the length of
        number of streets
    num_cards_for_hand : int
        number of cards for a valid poker hand, e.g. for texas hold'em
        num_cards_for_hand=5
    mandatory_num_hole_cards : int
        number of hole cards which have to be used for the hand, e.g.
        for pot limit omaha mandatory_num_hole_cards=2
    start_stack : int
        number of chips each player starts with
    low_end_straight : bool, optional
        toggle to include the low ace straight within valid hands, by
        default True
    order : Optional[List[str]], optional
        optional custom order of hand ranks, must be permutation of
        ['sf', 'fk', 'fh', 'fl', 'st', 'tk', 'tp', 'pa', 'hc']. if
        order=None, hands are ranked by rarity. by default None

    Examples
    ----------
    1-2 Heads Up No Limit Texas Hold'em:

        Dealer(num_players=2, num_streets=4, blinds=[1, 2], antes=0,
               raise_sizes=float('inf'), num_raises=float('inf'),
               num_suits=4, num_ranks=13, num_hole_cards=2,
               mandatory_num_hole_cards=0, start_stack=200)

    1-2 6 Player PLO

        Dealer(num_players=6, num_streets=4, blinds=[0, 1, 2, 0, 0, 0],
               antes=0, raise_sizes='pot', num_raises=float('inf'),
               num_suits=4, num_ranks=13, num_hole_cards=4,
               mandatory_num_hole_cards=2, start_stack=200)

    1-2 Heads Up No Limit Short Deck

        Dealer(num_players=2, num_streets=4, blinds=[1, 2], antes=0,
               raise_sizes=float('inf'), num_raises=float('inf'),
               num_suits=4, num_ranks=9, num_hole_cards=2,
               mandatory_num_hole_cards=0, start_stack=200,
               order=['sf', 'fk', 'fl', 'fh', 'st',
                      'tk', 'tp', 'pa', 'hc'])
    """

    def __init__(
        self,
        num_players: int,
        num_streets: int,
        blinds: Union[int, List[int]],
        antes: Union[int, List[int]],
        raise_sizes: Union[float, str, List[Union[float, str]]],
        num_raises: Union[float, List[float]],
        num_suits: int,
        num_ranks: int,
        num_hole_cards: int,
        num_community_cards: Union[int, List[int]],
        num_cards_for_hand: int,
        mandatory_num_hole_cards: int,
        start_stack: int,
        low_end_straight: bool = True,
        order: Optional[List[str]] = None,
    ) -> None:
        def check_inp(
            var: Union[List[Any], Any], expect_num: int, error_msg: str
        ) -> List[Any]:
            if isinstance(var, list):
                if len(var) != expect_num:
                    raise error.InvalidConfigError(error_msg)
                return var
            return [var] * expect_num

        error_msg = "incorrect {} distribution, expected list of length {}, got {}"
        blinds = check_inp(
            blinds, num_players, error_msg.format("blind", num_players, str(blinds)),
        )
        antes = check_inp(
            antes, num_players, error_msg.format("ante", num_players, str(antes))
        )
        raise_sizes = check_inp(
            raise_sizes,
            num_streets,
            error_msg.format("raise size", num_streets, str(raise_sizes)),
        )
        num_raises = check_inp(
            num_raises,
            num_streets,
            error_msg.format("number of raises", num_streets, str(num_raises)),
        )
        num_community_cards = check_inp(
            num_community_cards,
            num_streets,
            error_msg.format("community card", num_streets, str(num_community_cards)),
        )

        def clean_rs(raise_size):
            if isinstance(raise_size, (int, float)):
                return raise_size
            if raise_size == "pot":
                return raise_size
            raise error.InvalidRaiseSizeError(
                f"unknown raise size, expected one of (int, float, 'pot'),"
                f" got {raise_size}"
            )

        # config
        self.num_players = num_players
        self.num_streets = num_streets
        self.blinds = np.array(blinds)
        self.antes = np.array(antes)
        self.big_blind = blinds[1]
        self.raise_sizes = [clean_rs(raise_size) for raise_size in raise_sizes]
        self.num_raises = [float(raise_num) for raise_num in num_raises]
        self.num_suits = num_suits
        self.num_ranks = num_ranks
        self.num_hole_cards = num_hole_cards
        self.num_community_cards = num_community_cards
        self.num_cards_for_hand = num_cards_for_hand
        self.mandatory_num_hole_cards = mandatory_num_hole_cards
        self.start_stack = start_stack

        # dealer
        self.action = -1
        self.active = np.zeros(self.num_players, dtype=np.uint8)
        self.button = 0
        self.community_cards: List[poker.Card] = []
        self.deck = poker.Deck(self.num_suits, self.num_ranks)
        self.evaluator = poker.Evaluator(
            self.num_suits,
            self.num_ranks,
            self.num_cards_for_hand,
            self.mandatory_num_hole_cards,
            low_end_straight=low_end_straight,
            order=order,
        )
        self.history: List[Tuple[int, int, bool]] = []
        self.hole_cards: List[List[poker.Card]] = []
        self.largest_raise = 0
        self.pot = 0
        self.pot_commit = np.zeros(self.num_players, dtype=np.int32)
        self.stacks = np.full(self.num_players, self.start_stack, dtype=np.int32)
        self.street = 0
        self.street_commits = np.zeros(self.num_players, dtype=np.int32)
        self.street_option = np.zeros(self.num_players, dtype=np.uint8)
        self.street_raises = 0

        # render
        self.viewer: Optional[render.PokerViewer]
        self.viewer = None
        self.ascii_viewer = render.ASCIIViewer(
            num_players, num_hole_cards, sum(num_community_cards)
        )

    def __str__(self) -> str:
        config = self._render_config()
        return self.ascii_viewer.parse_string(config)

    def __repr__(self) -> str:
        string = (
            f"Dealer ({id(self)}) - num players: {self.num_players}, "
            f"num streets: {self.num_streets}"
        )
        return string

    def reset(self, reset_button: bool = False, reset_stacks: bool = False) -> Dict:
        """Resets the table. Shuffles the deck, deals new hole cards
        to all players, moves the button and collects blinds and antes.

        Parameters
        ----------
        reset_button : bool, optional
            reset button to first position at table, by default False
        reset_stacks : bool, optional
            reset stack sizes to starting stack size, by default False

        Returns
        -------
        Dict
            observation dictionary containing following info

                {
                    active: position of active player
                    button: position of button
                    call: number of chips needed to call
                    community_cards: shared community cards
                    hole_cards: hole cards for every player
                    max_raise: maximum raise size
                    min_raise: minimum raise size
                    pot: number of chips in the pot
                    stacks: stack size for every player
                    street_commits: number of chips commited by every
                                    player on this street
                }
        """
        if reset_stacks:
            self.active.fill(1)
            self.stacks = np.full(self.num_players, self.start_stack)
        else:
            self.active = self.stacks > 0
            if sum(self.active) <= 1:
                raise error.TooFewActivePlayersError(
                    "not enough players have chips, set reset_stacks=True"
                )
        if reset_button:
            self.button = 0
        else:
            self.button = self.button + 1 % self.num_players

        self.deck.shuffle()
        self.community_cards = self.deck.draw(self.num_community_cards[0])
        self.history = []
        self.hole_cards = [
            self.deck.draw(self.num_hole_cards) for _ in range(self.num_players)
        ]
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

    def step(self, bet: int) -> Tuple[Dict, np.ndarray, np.ndarray]:
        """Advances poker game to next player. If the bet is 0, it is
        either considered a check or fold, depending on the previous
        action. The given bet is always rounded to the closest valid bet
        size. When it is the same distance from two valid bet sizes
        the smaller bet size is used, e.g. if the min raise is 10 and
        the bet is 5, it is rounded down to 0.

        Parameters
        ----------
        bet : int
            number of chips bet by player currently active

        Returns
        -------
        Tuple[Dict, np.ndarray, np.ndarray]
            observation dictionary containing following info

                {
                    active: position of active player
                    button: position of button
                    call: number of chips needed to call
                    community_cards: shared community cards
                    hole_cards: hole cards for every player
                    max_raise: maximum raise size
                    min_raise: minimum raise size
                    pot: number of chips in the pot
                    stacks: stack size for every player
                    street_commits: number of chips commited by every
                                    player on this street
                }

            payouts for every player

            bool array containing value for every player if that player
            is still involved in round
        """
        if self.action == -1:
            if any(self.active):
                return self.__output()
            raise error.TableResetError("call reset() before calling first step()")

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
        if bet and (bet - call) >= self.largest_raise:
            self.largest_raise = bet - call
            self.street_raises += 1

        self.__collect_bet(bet)

        self.history.append((self.action, int(bet), fold))

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
                    self.num_community_cards[self.street]
                )
                if not all_all_in:
                    break
            self.street_commits.fill(0)
            self.street_option = np.logical_not(self.active).astype(np.uint8)
            self.street_raises = 0

        observation, payouts, done = self.__output()
        if all(done):
            self.action = -1
            observation["action"] = -1
        return observation, payouts, done

    def _render_config(self):
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
            "action": action,
            "active": active,
            "all_in": all_in,
            "community_cards": community_cards,
            "dealer": dealer,
            "done": done,
            "hole_cards": hole_cards,
            "pot": pot,
            "payouts": payouts,
            "prev_action": None if not self.history else self.history[-1],
            "street_commits": street_commits,
            "stacks": stacks,
        }

        return config

    def render(self, mode: str = "ascii", **kwargs):
        """Renders poker table. Render mode options are: ascii,
        asciimatics

        Parameters
        ----------
        mode : str, optional
            toggle for using different renderer, by default 'ascii'
        """
        viewer: Optional[Type[render.PokerViewer]] = None
        if self.viewer is None:
            if mode == "ascii":
                viewer = render.ASCIIViewer
            elif mode == "asciimatics":
                viewer = render.AsciimaticsViewer

        if viewer is None:
            render_modes = ", ".join(["ascii", "asciimatics"])
            raise error.InvalidRenderModeError(
                (f"incorrect render mode {mode}," f"use one of[{render_modes}]")
            )

        self.viewer = viewer(
            self.num_players,
            self.num_hole_cards,
            sum(self.num_community_cards),
            **kwargs,
        )

        config = self._render_config()

        self.viewer.render(config, **kwargs)

    def __all_agreed(self) -> bool:
        # not all agreed if not all players had chance to act
        if not all(self.street_option):
            return False
        # all agreed if street commits equal to maximum street commit
        # or player is all in
        # or player is not active
        return all(
            (self.street_commits == self.street_commits.max())
            | (self.stacks == 0)
            | np.logical_not(self.active)
        )

    def __bet_sizes(self) -> Tuple[int, int, int]:
        # call difference between commit and maximum commit
        call = self.street_commits.max() - self.street_commits[self.action]
        # min raise at least largest previous raise
        # if limit game min and max raise equal to raise size
        if isinstance(self.raise_sizes[self.street], int):
            max_raise = min_raise = self.raise_sizes[self.street] + call
        else:
            min_raise = max(self.big_blind, self.largest_raise + call)
            if self.raise_sizes[self.street] == "pot":
                max_raise = self.pot + call * 2
            elif self.raise_sizes[self.street] == float("inf"):
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
    def __clean_bet(bet: int, call: int, min_raise: int, max_raise: int) -> int:
        # find closest bet size to actual bet
        # pessimistic approach: in ties order is fold/check -> call -> raise
        idx = np.argmin(np.absolute(np.array([0, call, min_raise, max_raise]) - bet))
        # if call closest
        if idx == 1:
            return call
        # if min raise or max raise closest
        if idx in (2, 3):
            return round(min(max_raise, max(min_raise, bet)))
        # if fold closest
        return 0

    def __collect_multiple_bets(self, bets: List[int], street_commits: bool = True):
        bets = np.roll(bets, self.action)
        bets = (self.stacks > 0) * self.active * bets
        if street_commits:
            self.street_commits += bets
        self.pot_commit += bets
        self.pot += sum(bets)
        self.stacks -= bets

    def __collect_bet(self, bet: int):
        # bet only as large as stack size
        bet = min(self.stacks[self.action], bet)

        self.pot += bet
        self.pot_commit[self.action] += bet
        self.street_commits[self.action] += bet
        self.stacks[self.action] -= bet

    def __done(self) -> List[bool]:
        if self.street >= self.num_streets or sum(self.active) <= 1:
            # end game
            out = np.full(self.num_players, 1)
            return out
        return np.logical_not(self.active)

    def __observation(self) -> Dict:
        if all(self.__done()):
            call = min_raise = max_raise = 0
        else:
            call, min_raise, max_raise = self.__bet_sizes()
        observation: dict = {
            "action": self.action,
            "active": self.active,
            "button": self.button,
            "call": call,
            "community_cards": [str(card) for card in self.community_cards],
            "hole_cards": [[str(card) for card in cards] for cards in self.hole_cards],
            "max_raise": max_raise,
            "min_raise": min_raise,
            "pot": self.pot,
            "stacks": self.stacks,
            "street_commits": self.street_commits,
        }
        return observation

    def __payouts(self) -> np.ndarray:
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

    def __output(self) -> Tuple[Dict, np.ndarray, np.ndarray]:
        observation = self.__observation()
        payouts = self.__payouts()
        done = self.__done()
        return observation, payouts, done

    def __eval_round(self) -> np.ndarray:
        # grab array of hand strength and pot commits
        worst_hand = self.evaluator.table.max_rank + 1
        hand_list = []
        payouts = np.zeros(self.num_players, dtype=int)
        for player in range(self.num_players):
            # if not active hand strength set
            # to 1 worse than worst possible rank
            hand_strength = worst_hand
            if self.active[player]:
                hand_strength = self.evaluator.evaluate(
                    self.hole_cards[player], self.community_cards
                )
            hand_list.append([player, hand_strength, self.pot_commit[player]])
        hands = np.array(hand_list)
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
