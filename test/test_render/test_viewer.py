import pytest

from clubs import render


def test_base():

    viewer = render.PokerViewer(0, 0, 0)
    with pytest.raises(NotImplementedError):
        viewer.render({})
