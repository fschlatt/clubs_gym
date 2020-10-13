class PokerViewer:
    """Base class for renderer. Any renderer must subclass this renderer
    and implement the function render

    Parameters
    ----------
    num_players : int
        number of player
    num_hole_cards : int
        number of hole cards
    num_community_cards : int
        number of community cards
    """

    def __init__(
        self, num_players: int, num_hole_cards: int, num_community_cards: int, **kwargs,
    ) -> None:
        self.num_players = num_players
        self.num_hole_cards = num_hole_cards
        self.num_community_cards = num_community_cards

    def render(self, config: dict, **kwargs) -> None:
        """Render the table based on the table configuration

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
        raise NotImplementedError
