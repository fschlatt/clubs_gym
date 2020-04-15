from typing import Dict, List, Optional, Union

import gym
from gym import spaces

import clubs


class ClubsEnv(gym.Env):

    metadata = {'render.modes': ['ascii', 'asciimatics']}

    def __init__(self, num_players: int, num_streets: int,
                 blinds: Union[int, List[int]], antes: Union[int, List[int]],
                 raise_sizes: Union[float, str, List[Union[float, str]]],
                 num_raises: Union[float, List[float]], num_suits: int,
                 num_ranks: int, num_hole_cards: int,
                 num_community_cards: Union[int, List[int]],
                 num_cards_for_hand: int, mandatory_num_hole_cards: int,
                 start_stack: int, low_end_straight: bool = True,
                 order: Optional[List[str]] = None) -> None:

        self.dealer = clubs.Dealer(
            num_players, num_streets, blinds, antes, raise_sizes, num_raises,
            num_suits, num_ranks, num_hole_cards, num_community_cards,
            num_cards_for_hand, mandatory_num_hole_cards, start_stack,
            low_end_straight, order
        )

        max_bet = start_stack * num_players
        if isinstance(num_community_cards, list):
            num_comm_cards = sum(num_community_cards)
        self.action_space = spaces.Discrete(max_bet)
        card_space = spaces.Tuple((
            spaces.Discrete(num_ranks),
            spaces.Discrete(num_suits)
        ))
        hole_card_space = spaces.Tuple(
            (card_space,) * num_hole_cards
        )
        self.observation_space = spaces.Dict({
            'action': spaces.Discrete(num_players),
            'active': spaces.MultiBinary(num_players),
            'button': spaces.Discrete(num_players),
            'call': spaces.Discrete(max_bet),
            'community_cards': spaces.Tuple(
                (card_space,) * num_comm_cards
            ),
            'hole_cards': spaces.Tuple(
                (hole_card_space,) * num_players
            ),
            'max_raise': spaces.Discrete(max_bet),
            'min_raise': spaces.Discrete(max_bet),
            'pot': spaces.Discrete(max_bet),
            'stacks': spaces.Tuple(
                (spaces.Discrete(max_bet),) * num_players
            ),
            'street_commits': spaces.Tuple(
                (spaces.Discrete(max_bet),) * num_players
            )
        })

    def step(self, bet: int):
        return *self.dealer.step(bet), None

    def reset(self, reset_button: bool = False,
              reset_stacks: bool = False) -> Dict:
        return self.dealer.reset(reset_button, reset_stacks)

    def render(self, mode='ascii', **kwargs):
        self.dealer.render(mode=mode, **kwargs)

    def close(self):
        pass


def register(configs: Dict) -> None:
    '''Registers dict of clubs configs as gym environments

    Parameters
    ----------
    configs : Dict
        dictionary of clubs configs, keys must environment ids and
        values valid clubs configs, example:
            configs = {
                'NoLimitHoldemTwoPlayer-v0: {
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
    '''
    env_entry_point = 'clubs.envs.env:ClubsEnv'
    for env_id, config in configs.items():
        gym.envs.registration.register(
            id=env_id,
            entry_point=env_entry_point,
            kwargs={**config}
        )
