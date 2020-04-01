try:
    from asciimatics import screen
    ASCIIMATICS = True
except ImportError:
    ASCIIMATICS = False
import threading
import time

from . import ascii


class AsciimaticsViewer(ascii.ASCIIViewer):

    def __init__(self, num_players, num_hole_cards, num_community_cards):
        super(AsciimaticsViewer, self).__init__(
            num_players, num_hole_cards, num_community_cards)

        if not ASCIIMATICS:
            raise ImportError(
                'install asciimatics to use the asciimatics viewer')

        self.string = ''
        self.refresh = threading.Condition()
        thread = threading.Thread(target=self._render, daemon=True)
        thread.start()

    def render(self, config, fps=5):

        self.string = self._parse_string(config)

        self.refresh.acquire()
        self.refresh.notify()
        self.refresh.release()
        if fps:
            time.sleep(1/fps)

    def _render(self):
        with screen.ManagedScreen() as scr:
            while True:
                for idx, line in enumerate(self.string.split('\n')):
                    scr.print_at(line, 0, idx)
                scr.refresh()
                self.refresh.acquire()
                self.refresh.wait()
