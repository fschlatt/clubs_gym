import io
from contextlib import redirect_stdout

from clubs import render


def test_init():
    viewer = render.ASCIIViewer(2, 2, 5)
    assert len(viewer.table) == 1061


def test_render():

    viewer = render.ASCIIViewer(2, 2, 5)

    config = {
        "action": 0,
        "active": [1, 1],
        "all_in": [0, 0],
        "community_cards": [],
        "dealer": 0,
        "done": 0,
        "hole_cards": [["Ah", "Ad"], ["Ks", "Kd"]],
        "pot": 20,
        "payouts": [0, 0],
        "prev_action": None,
        "street_commits": [0, 0],
        "stacks": [100, 100],
    }

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        viewer.render(config)
    string = stdout.getvalue()

    sub_strings = ["Ah", "Ad", "??", "20"]
    not_sub_strings = ["Ks", "Kd"]
    assert all(sub_string in string for sub_string in sub_strings)
    assert all(sub_string not in string for sub_string in not_sub_strings)

    config["active"] = [1, 0]

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        viewer.render(config)
    string = stdout.getvalue()

    sub_strings = ["Ah", "Ad", "20"]
    not_sub_strings = ["??"]
    assert all(sub_string in string for sub_string in sub_strings)
    assert all(sub_string not in string for sub_string in not_sub_strings)

    config["active"] = [1, 1]
    config["all_in"] = [0, 1]

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        viewer.render(config)
    string = stdout.getvalue()

    sub_strings = ["Ah", "Ad", "20", "A"]
    not_sub_strings = ["Ks", "Kd"]
    assert all(sub_string in string for sub_string in sub_strings)
    assert all(sub_string not in string for sub_string in not_sub_strings)

    config["all_in"] = [0, 0]
    config["prev_action"] = [1, 200, 0]

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        viewer.render(config)
    string = stdout.getvalue()

    action_string = "Player 2 bet 200 Action on Player 1"
    sub_strings = ["Ah", "Ad", "20", action_string]
    not_sub_strings = ["Ks", "Kd"]
    assert all(sub_string in string for sub_string in sub_strings)
    assert all(sub_string not in string for sub_string in not_sub_strings)

    config["prev_action"] = [1, 0, 1]

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        viewer.render(config)
    string = stdout.getvalue()

    action_string = "Player 2 folded Action on Player 1"
    sub_strings = ["Ah", "Ad", "20", action_string]
    not_sub_strings = ["Ks", "Kd"]
    assert all(sub_string in string for sub_string in sub_strings)
    assert all(sub_string not in string for sub_string in not_sub_strings)

    config["prev_action"] = [1, 0, 0]

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        viewer.render(config)
    string = stdout.getvalue()

    action_string = "Player 2 checked Action on Player 1"
    sub_strings = ["Ah", "Ad", "20", action_string]
    not_sub_strings = ["Ks", "Kd"]
    assert all(sub_string in string for sub_string in sub_strings)
    assert all(sub_string not in string for sub_string in not_sub_strings)

    config["prev_action"] = None
    config["payouts"] = [2, 2]
    config["done"] = True

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        viewer.render(config)
    string = stdout.getvalue()

    action_string = "Players 1, 2 won 2, 2 respectively"
    sub_strings = ["Ah", "Ad", "Ks", "Kd", action_string]
    not_sub_strings = []
    assert all(sub_string in string for sub_string in sub_strings)
    assert all(sub_string not in string for sub_string in not_sub_strings)

    config["payouts"] = [10, 0]
    config["done"] = True

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        viewer.render(config)
    string = stdout.getvalue()

    action_string = "Player 1 won 10"
    sub_strings = ["Ah", "Ad", "Ks", "Kd", action_string]
    not_sub_strings = []
    assert all(sub_string in string for sub_string in sub_strings)
    assert all(sub_string not in string for sub_string in not_sub_strings)
