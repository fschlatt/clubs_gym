'''Entry point into the pommerman module'''
import gym
import inspect
from . import configs
from . import poker

def register(config):
    gym.envs.registration.register(
        id=config['env_id'],
        entry_point=config['env_entry_point'],
        kwargs={'config': config['config']})


def _register():
    for name, func in inspect.getmembers(configs, inspect.isfunction):
        if not name.endswith('_env'):
            continue

        config = func()

        gym.envs.registration.register(
            id=config['env_id'],
            entry_point=config['env_entry_point'],
            kwargs={'config': config['config']})


# Register environments with gym
_register()
