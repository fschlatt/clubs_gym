import os

from . import viewer


class ASCIIViewer(viewer.PokerViewer):
    """Poker game renderer which prints an ascii representation of the
    table state to the terminal

    Parameters
    ----------
    num_players : int
        number of players
    num_hole_cards : int
        number of hole cards
    num_community_cards : int
        number of community cards
    """

    POS_DICT = {
        2: [0, 5],
        3: [0, 3, 6],
        4: [0, 2, 4, 6],
        5: [0, 2, 4, 6, 8],
        6: [0, 1, 3, 5, 6, 8],
        7: [0, 1, 3, 5, 6, 7, 9],
        8: [0, 1, 2, 4, 5, 6, 7, 9],
        9: [0, 1, 2, 4, 5, 6, 7, 8, 9],
        10: list(range(10)),
    }

    KEYS = (
        ["p{}".format(idx) for idx in range(10)]
        + ["p{}c".format(idx) for idx in range(10)]
        + ["a{}".format(idx) for idx in range(10)]
        + ["b{}".format(idx) for idx in range(10)]
        + ["sb", "bb", "ccs", "pot", "action"]
    )

    def __init__(
        self, num_players: int, num_hole_cards: int, num_community_cards: int
    ) -> None:
        super(ASCIIViewer, self).__init__(
            num_players, num_hole_cards, num_community_cards
        )

        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open("{}/ascii_table.txt".format(dir_path), "r") as file:
            self.table = file.read()

        self.player_pos = self.POS_DICT[num_players]

    def parse_string(self, config: dict) -> str:
        """Parses game config and inserts values into ascii table

        Parameters
        ----------
        config : dict
            game configuration dictionary,
                config = {
                    'action': int - position of active player,
                    'active': List[bool] - list of active players,
                    'all_in': List[bool] - list of all in players,
                    'community_cards': List[Card] - list of community
                                       cards,
                    'dealer': int - position of dealer,
                    'done': bool - list of done players,
                    'hole_cards': List[List[Card]] - list of hole cards,
                    'pot': int - chips in pot,
                    'payouts': List[int] - list of chips won for each
                               player,
                    'prev_action': Tuple[int, int, int] - last
                                   position bet and fold,
                    'street_commits': List[int] - list of number of
                                      chips added to pot from each
                                      player on current street,
                    'stacks': List[int] - list of stack sizes,
                }

        Returns
        -------
        str
            ascii table representation
        """

        action = config["action"]
        dealer = config["dealer"]
        done = config["done"]
        positions = ["p{}".format(idx) for idx in self.player_pos]

        players = self._parse_players(config, done, action)
        action_string, win_string = self._parse_string(config, done, positions)

        str_config = {key: "" for key in self.KEYS}

        # community cards
        ccs = [str(card) for card in config["community_cards"]]
        ccs += ["--"] * (self.num_community_cards - len(ccs))
        ccs_string = "[" + ",".join(ccs) + "]"
        str_config["ccs"] = ccs_string

        # pot
        if not done:
            str_config["pot"] = "{:,}".format(config["pot"])
            str_config["a{}".format(self.player_pos[action])] = "X"
        else:
            str_config["pot"] = "0"

        # dealer + player positions
        str_config["b{}".format(self.player_pos[dealer])] = "D "
        iterables = [players, config["street_commits"], positions, config["all_in"]]
        for player, street_commit, pos, all_in in zip(*iterables):
            str_config[pos] = player
            str_config[pos + "c"] = "{:,}".format(street_commit)
            if all_in and not done:
                str_config["a" + pos[1:]] = "A"

        # payouts
        if done:
            iterables = [config["payouts"], positions]
            for payout, pos in zip(*iterables):
                str_config[pos + "c"] = "{:,}".format(payout)

        # action + win string
        str_config["action"] = action_string
        str_config["win"] = win_string

        string = self.table.format(**str_config)

        return string

    def _parse_players(self, config, done, action):
        players = []
        iterator = zip(config["hole_cards"], config["stacks"], config["active"])
        for idx, (hand, stack, active) in enumerate(iterator):
            if not active:
                players.append(
                    "{:2}. ".format(idx + 1)
                    + ",".join(["--"] * self.num_hole_cards)
                    + " {:,}".format(stack)
                )
                continue
            if done or idx == action:
                players.append(
                    "{:2}. ".format(idx + 1)
                    + ",".join([str(card) for card in hand])
                    + " {:,}".format(stack)
                )
                continue
            players.append(
                "{:2}. ".format(idx + 1)
                + ",".join(["??"] * self.num_hole_cards)
                + " {:,}".format(stack)
            )
        return players

    def _parse_string(self, config, done, positions):
        action_string = ""
        win_string = ""

        prev_action = config["prev_action"]
        if prev_action is not None:
            action_string = "Player {} {}"
            player, bet, fold = prev_action
            if fold:
                action = "folded "
            else:
                if bet:
                    action = "bet {} ".format(bet)
                else:
                    action = "checked "
            action_string = action_string.format(player + 1, action)

        if done:
            win_string = "Player"
            if sum(payout > 0 for payout in config["payouts"]) > 1:
                win_string += "s {} won {} respectively"
            else:
                win_string += " {} won {}"
            players = []
            payouts = []
            for player, payout in enumerate(config["payouts"]):
                if payout > 0:
                    players.append(str(player + 1))
                    payouts.append(str(payout))
            win_string = win_string.format(", ".join(players), ", ".join(payouts))
        else:
            action_string += "Action on Player {}".format(config["action"] + 1)

        return action_string, win_string

    def render(self, config: dict, **kwargs) -> None:
        """Render ascii table representation based on the table
        configuration

        Parameters
        ----------
        config : dict
            game configuration dictionary,
                config = {
                    'action': int - position of active player,
                    'active': List[bool] - list of active players,
                    'all_in': List[bool] - list of all in players,
                    'community_cards': List[Card] - list of community
                                       cards,
                    'dealer': int - position of dealer,
                    'done': bool - list of done players,
                    'hole_cards': List[List[Card]] - list of hole cards,
                    'pot': int - chips in pot,
                    'payouts': List[int] - list of chips won for each
                               player,
                    'prev_action': Tuple[int, int, int] - last
                                   position bet and fold,
                    'street_commits': List[int] - list of number of
                                      chips added to pot from each
                                      player on current street,
                    'stacks': List[int] - list of stack sizes,
                }
        """

        string = self.parse_string(config)

        print(string)
