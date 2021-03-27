try:
    from asciimatics import screen

    ASCIIMATICS = True
except ImportError:
    ASCIIMATICS = False
import threading
import time

from . import ascii_viewer


class AsciimaticsViewer(ascii_viewer.ASCIIViewer):
    """Poker game renderer which prints an animated ascii representation
    of the table state to the terminal using the asciimatics library

    Parameters
    ----------
    num_players : int
        number of players
    num_hole_cards : int
        number of hole cards
    num_community_cards : int
        number of community cards
    """

    def __init__(
        self, num_players: int, num_hole_cards: int, num_community_cards: int
    ) -> None:
        super(AsciimaticsViewer, self).__init__(
            num_players, num_hole_cards, num_community_cards
        )

        if not ASCIIMATICS:
            raise ImportError("install asciimatics to use the asciimatics viewer")

        self.string = ""
        self.refresh = threading.Condition()
        thread = threading.Thread(target=self._render_loop, daemon=True)
        thread.start()

    def render(self, config: dict, fps: int = 5, **kwargs) -> None:
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
        fps : int, optional
            frames per second for ascii animation, by default 5
        """

        self.string = self.parse_string(config)

        self.refresh.acquire()
        self.refresh.notify()
        self.refresh.release()
        if fps:
            time.sleep(1 / fps)

    def _render_loop(self):
        with screen.ManagedScreen() as scr:
            while True:
                for idx, line in enumerate(self.string.split("\n")):
                    scr.print_at(line, 0, idx)
                scr.refresh()
                self.refresh.acquire()
                self.refresh.wait()
