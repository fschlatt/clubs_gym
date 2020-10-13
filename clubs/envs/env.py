from typing import Dict, List, Optional, Tuple, Union

import gym
import numpy as np
from gym import spaces

from clubs import agent, error, poker


class ClubsEnv(gym.Env):
    """Runs a range of different of poker games dependent on the
    given configuration. Supports limit, no limit and pot limit
    bet sizing, arbitrary deck sizes, arbitrary hole and community
    cards and many other options.

    Parameters
    ----------
    num_players : int
        maximum number of players
    num_streets : int
        number of streets including preflop, e.g. for texas hold'em
        num_streets=4
    blinds : Union[int, List[int]]
        blind distribution as a list of ints, one for each player
        starting from the button e.g. [0, 1, 2] for a three player game
        with a sb of 1 and bb of 2, passed ints will be expanded to
        all players i.e. pass blinds=0 for no blinds
    antes : Union[int, List[int]]
        ante distribution as a list of ints, one for each player
        starting from the button e.g. [0, 0, 5] for a three player game
        with a bb ante of 5, passed ints will be expanded to all
        players i.e. pass antes=0 for no antes
    raise_sizes : Union[float, str, List[Union[float, str]]]
        max raise sizes for each street, valid raise sizes are ints,
        floats, and 'pot', e.g. for a 1-2 limit hold'em the raise sizes
        should be [2, 2, 4, 4] as the small and big bet are 2 and 4.
        float('inf') can be used for no limit games. pot limit raise
        sizes can be set using 'pot'. if only a single int, float or
        string is passed the value is expanded to a list the length
        of number of streets, e.g. for a standard no limit game pass
        raise_sizes=float('inf')
    num_raises : Union[float, List[float]]
        max number of bets for each street including preflop, valid
        raise numbers are ints and floats. if only a single int or float
        is passed the value is expanded to a list the length of number
        of streets, e.g. for a standard limit game pass num_raises=4
    num_suits : int
        number of suits to use in deck, must be between 1 and 4
    num_ranks : int
        number of ranks to use in deck, must be between 1 and 13
    num_hole_cards : int
        number of hole cards per player, must be greater than 0
    num_community_cards : Union[int, List[int]]
        number of community cards per street including preflop, e.g.
        for texas hold'em pass num_community_cards=[0, 3, 1, 1]. if only
        a single int is passed, it is expanded to a list the length of
        number of streets
    num_cards_for_hand : int
        number of cards for a valid poker hand, e.g. for texas hold'em
        num_cards_for_hand=5
    mandatory_num_hole_cards : int
        number of hole cards which have to be used for the hand, e.g.
        for pot limit omaha mandatory_num_hole_cards=2
    start_stack : int
        number of chips each player starts with
    low_end_straight : bool, optional
        toggle to include the low ace straight within valid hands, by
        default True
    order : Optional[List[str]], optional
        optional custom order of hand ranks, must be permutation of
        ['sf', 'fk', 'fh', 'fl', 'st', 'tk', 'tp', 'pa', 'hc']. if
        order=None, hands are ranked by rarity. by default None

    Examples
    ----------
    1-2 Heads Up No Limit Texas Hold'em:

        Dealer(num_players=2, num_streets=4, blinds=[1, 2], antes=0,
               raise_sizes=float('inf'), num_raises=float('inf'),
               num_suits=4, num_ranks=13, num_hole_cards=2,
               mandatory_num_hole_cards=0, start_stack=200)

    1-2 6 Player PLO

        Dealer(num_players=6, num_streets=4, blinds=[0, 1, 2, 0, 0, 0],
               antes=0, raise_sizes='pot', num_raises=float('inf'),
               num_suits=4, num_ranks=13, num_hole_cards=4,
               mandatory_num_hole_cards=2, start_stack=200)

    1-2 Heads Up No Limit Short Deck

        Dealer(num_players=2, num_streets=4, blinds=[1, 2], antes=0,
               raise_sizes=float('inf'), num_raises=float('inf'),
               num_suits=4, num_ranks=9, num_hole_cards=2,
               mandatory_num_hole_cards=0, start_stack=200,
               order=['sf', 'fk', 'fl', 'fh', 'st',
                      'tk', 'tp', 'pa', 'hc'])
    """

    metadata = {"render.modes": ["ascii", "asciimatics"]}

    def __init__(
        self,
        num_players: int,
        num_streets: int,
        blinds: Union[int, List[int]],
        antes: Union[int, List[int]],
        raise_sizes: Union[float, str, List[Union[float, str]]],
        num_raises: Union[float, List[float]],
        num_suits: int,
        num_ranks: int,
        num_hole_cards: int,
        num_community_cards: Union[int, List[int]],
        num_cards_for_hand: int,
        mandatory_num_hole_cards: int,
        start_stack: int,
        low_end_straight: bool = True,
        order: Optional[List[str]] = None,
    ) -> None:

        self.dealer = poker.Dealer(
            num_players,
            num_streets,
            blinds,
            antes,
            raise_sizes,
            num_raises,
            num_suits,
            num_ranks,
            num_hole_cards,
            num_community_cards,
            num_cards_for_hand,
            mandatory_num_hole_cards,
            start_stack,
            low_end_straight,
            order,
        )

        max_bet = start_stack * num_players
        if isinstance(num_community_cards, list):
            num_comm_cards = sum(num_community_cards)
        self.action_space = spaces.Discrete(max_bet)
        card_space = spaces.Tuple(
            (spaces.Discrete(num_ranks), spaces.Discrete(num_suits))
        )
        hole_card_space = spaces.Tuple((card_space,) * num_hole_cards)
        self.observation_space = spaces.Dict(
            {
                "action": spaces.Discrete(num_players),
                "active": spaces.MultiBinary(num_players),
                "button": spaces.Discrete(num_players),
                "call": spaces.Discrete(max_bet),
                "community_cards": spaces.Tuple((card_space,) * num_comm_cards),
                "hole_cards": spaces.Tuple((hole_card_space,) * num_players),
                "max_raise": spaces.Discrete(max_bet),
                "min_raise": spaces.Discrete(max_bet),
                "pot": spaces.Discrete(max_bet),
                "stacks": spaces.Tuple((spaces.Discrete(max_bet),) * num_players),
                "street_commits": spaces.Tuple(
                    (spaces.Discrete(max_bet),) * num_players
                ),
            }
        )

        self.agents: Optional[Dict[int, agent.BaseAgent]] = None
        self.prev_obs: Optional[Dict] = None

    def act(self, obs: dict) -> int:
        if self.agents is None:
            raise error.NoRegisteredAgentsError(
                "register agents using env.register_agents(...) before"
                "calling act(obs)"
            )
        if self.prev_obs is None:
            raise error.EnvironmentResetError(
                "call reset() before calling first step()"
            )
        action = self.prev_obs["action"]
        bet = self.agents[action].act(obs)
        return bet

    @staticmethod
    def _parse_obs(obs):
        obs["hole_cards"] = obs["hole_cards"][obs["action"]]
        return obs

    def step(self, bet: int) -> Tuple[Dict, np.ndarray, np.ndarray, None]:
        obs, rewards, done = self.dealer.step(bet)
        obs = self._parse_obs(obs)
        if self.agents is not None:
            self.prev_obs = obs
        return obs, rewards, done, None

    def reset(self, reset_button: bool = False, reset_stacks: bool = False) -> Dict:
        obs = self.dealer.reset(reset_button, reset_stacks)
        obs = self._parse_obs(obs)
        if self.agents is not None:
            self.prev_obs = obs
        return obs

    def render(self, mode="ascii", **kwargs) -> None:
        self.dealer.render(mode=mode, **kwargs)

    def close(self):
        pass

    def register_agents(self, agents: Union[List, Dict]) -> None:
        error_msg = "invalid agent configuration, got {}, expected {}"
        if not isinstance(agents, (dict, list)):
            raise error.InvalidAgentConfigurationError(
                error_msg.format(type(agents), "list or dictionary of agents")
            )
        if len(agents) != self.dealer.num_players:
            raise error.InvalidAgentConfigurationError(
                error_msg.format(
                    f"{len(agents)} number of agents",
                    f"{self.dealer.num_players} number of agents",
                )
            )
        if isinstance(agents, list):
            agent_keys = list(range(len(agents)))
        else:
            agent_keys = list(agents.keys())
            if set(agent_keys) != set(range(len(agents))):
                raise error.InvalidAgentConfigurationError(
                    f"invalid agent configuration, got {agent_keys}, "
                    f"expected permutation of {list(range(len(agents)))}"
                )
            agents = list(agents.values())
        all_base_agents = all(isinstance(_agent, agent.BaseAgent) for _agent in agents)
        if not all_base_agents:
            raise error.InvalidAgentConfigurationError(
                error_msg.format(
                    f"agent types {[type(_agent) for _agent in agents]}",
                    "only subtypes of clubs.agent.BaseAgent",
                )
            )
        self.agents = dict(zip(agent_keys, agents))


def register(configs: Dict) -> None:
    """Registers dict of clubs configs as gym environments

    Parameters
    ----------
    configs : Dict
        dictionary of clubs configs, keys must environment ids and
        values valid clubs configs, example:
            configs = {
                'NoLimitHoldemTwoPlayer-v0': {
                    'num_players': 2,
                    'num_streets': 4,
                    'blinds': [1, 2],
                    'antes': 0,
                    'raise_sizes': float('inf'),
                    'num_raises': float('inf'),
                    'num_suits': 4,
                    'num_ranks': 13,
                    'num_hole_cards': 2,
                    'num_community_cards': [0, 3, 1, 1],
                    'num_cards_for_hand': 5,
                    'mandatory_num_hole_cards': 0,
                    'start_stack': 200
                }
            }
    """
    env_entry_point = "clubs.envs.env:ClubsEnv"
    for env_id, config in configs.items():
        gym.envs.registration.register(
            id=env_id, entry_point=env_entry_point, kwargs={**config}
        )
