import random

import clubs

from . import base


class NashKuhnAgent(base.BaseAgent):
    def __init__(self, alpha: float) -> None:
        super().__init__()
        if alpha < 0 or alpha > 1 / 3:
            raise ValueError(
                f"invalid alpha value, expected 0 <= alpha <= 1/3, got {alpha}"
            )
        self.alpha = alpha

    def player_1_check(self, obs: clubs.poker.engine.ObservationDict) -> int:
        rank = obs["hole_cards"][0].rank
        if rank == "Q":
            if random.random() < self.alpha:
                return 1
            return 0
        if rank == "K":
            return 0
        if rank == "A":
            if random.random() < 3 * self.alpha:
                return 1
            return 0
        raise ValueError("got invalid card rank, expected one of [Q, K, A] got {f.}")

    def player_1_bet(self, obs: clubs.poker.engine.ObservationDict) -> int:
        rank = obs["hole_cards"][0].rank
        if rank == "Q":
            return 0
        if rank == "K":
            if random.random() < 1 / 3 + self.alpha:
                return 1
            return 0
        if rank == "A":
            return 1
        raise ValueError("got invalid card rank, expected one of [Q, K, A] got {f.}")

    def _player_1(self, obs: clubs.poker.engine.ObservationDict) -> int:
        if obs["pot"] == 2:
            return self.player_1_check(obs)
        return self.player_1_bet(obs)

    def _player_2_check(self, obs: clubs.poker.engine.ObservationDict) -> int:
        rank = obs["hole_cards"][0].rank
        if rank == "Q":
            if random.random() < 1 / 3:
                return 1
            return 0
        if rank == "K":
            return 0
        if rank == "A":
            return 1
        raise ValueError("got invalid card rank, expected one of [Q, K, A] got {f.}")

    def _player_2_bet(self, obs: clubs.poker.engine.ObservationDict) -> int:
        rank = obs["hole_cards"][0].rank
        if rank == "Q":
            return 0
        if rank == "K":
            if random.random() < 1 / 3:
                return 1
            return 0
        if rank == "A":
            return 1
        raise ValueError("got invalid card rank, expected one of [Q, K, A] got {f.}")

    def _player_2(self, obs: clubs.poker.engine.ObservationDict) -> int:
        if obs["pot"] == 2:
            return self._player_2_check(obs)
        return self._player_2_bet(obs)

    def act(self, obs: clubs.poker.engine.ObservationDict) -> int:
        if obs["action"] == 0:
            return self._player_1(obs)
        return self._player_2(obs)
