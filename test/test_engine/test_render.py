import io
import random
from contextlib import redirect_stdout

import pytest

import clubs
from clubs import error


def test_render():

    random.seed(42)

    config = clubs.configs.NO_LIMIT_HOLDEM_SIX_PLAYER

    dealer = clubs.poker.Dealer(**config)

    dealer.reset()
    with pytest.raises(error.InvalidRenderModeError):
        dealer.render("lala")

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        dealer.render()
    string = stdout.getvalue()

    action_string = "Action on Player 5"
    sub_strings = [
        f"6{chr(9824)},2{chr(9827)} 200",
        "199",
        "??",
        "3",
        "Ac",
        action_string,
    ]
    assert all(sub_string in string for sub_string in sub_strings)
