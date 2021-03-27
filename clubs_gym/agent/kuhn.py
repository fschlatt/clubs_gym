import random

from . import base


class NashKuhnAgent(base.BaseAgent):
    def __init__(self, alpha):
        super().__init__()
        if alpha < 0 or alpha > 1 / 3:
            raise ValueError(
                f"invalid alpha value, expected 0 <= alpha <= 1/3, got {alpha}"
            )
        self.alpha = alpha

    def player_1_check(self, obs):
        if obs["hole_cards"][0][0] == "Q":
            if random.random() < self.alpha:
                return 1
            return 0
        if obs["hole_cards"][0][0] == "K":
            return 0
        if obs["hole_cards"][0][0] == "A":
            if random.random() < 3 * self.alpha:
                return 1
            return 0

    def player_1_bet(self, obs):
        if obs["hole_cards"][0][0] == "Q":
            return 0
        if obs["hole_cards"][0][0] == "K":
            if random.random() < 1 / 3 + self.alpha:
                return 1
            return 0
        if obs["hole_cards"][0][0] == "A":
            return 1

    def _player_1(self, obs):
        if obs["pot"] == 2:
            return self.player_1_check(obs)
        return self.player_1_bet(obs)

    def _player_2_check(self, obs):
        if obs["hole_cards"][0][0] == "Q":
            if random.random() < 1 / 3:
                return 1
            return 0
        if obs["hole_cards"][0][0] == "K":
            return 0
        if obs["hole_cards"][0][0] == "A":
            return 1

    def _player_2_bet(self, obs):
        if obs["hole_cards"][0][0] == "Q":
            return 0
        if obs["hole_cards"][0][0] == "K":
            if random.random() < 1 / 3:
                return 1
            return 0
        if obs["hole_cards"][0][0] == "A":
            return 1

    def _player_2(self, obs):
        if obs["pot"] == 2:
            return self._player_2_check(obs)
        return self._player_2_bet(obs)

    def act(self, obs):
        if obs["action"] == 0:
            return self._player_1(obs)
        return self._player_2(obs)
