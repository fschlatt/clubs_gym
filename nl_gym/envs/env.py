import gym


class NLGym(gym.Env):

    metadata = {'render.modes': ['human', 'rgb_array', 'rgb_pixel']}

    def __init__(self):
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass
