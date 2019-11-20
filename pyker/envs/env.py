import gym
from gym import spaces
import numpy as np

from .. import poker


class NLGym(gym.Env):

    metadata = {'render.modes': ['ascii', 'asciimatics']}

    def __init__(self, config=None):

        if config is None and isinstance(config, dict):
            raise TypeError(
                'config ({}) is not config dict'.format(type(config)))

        self.dealer = poker.dealer.Dealer(config)

        max_bet = config['start_stack'] * config['num_players']
        self.action_space = spaces.Dict({'fold': spaces.MultiBinary(1),
                                         'bet': spaces.Box(low=0,
                                                           high=max_bet,
                                                           shape=(1,),
                                                           dtype=np.float32)})
        self.observation_space = None  # TODO add observation space

    def step(self, action):
        return self.dealer.step(action)

    def reset(self, reset_stacks=True):
        return self.dealer.reset(reset_stacks)

    def render(self, mode='ascii'):
        self.dealer.render(mode=mode)

    def close(self):
        pass
