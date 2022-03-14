import clubs


class BaseAgent:
    def __init__(self) -> None:
        pass

    def act(self, obs: clubs.poker.engine.ObservationDict) -> int:
        raise NotImplementedError()
