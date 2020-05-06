from . import agent, configs, envs, poker
from .poker.engine import Dealer

__all__ = ["agent", "configs", "envs", "poker", "Dealer"]
__version__ = "0.1.0"
__author__ = "Ferdinand Schlatt"
__license__ = "GLP-3.0"
__copyright__ = f"Copyright (c) 2020, {__author__}."
__homepage__ = "https://github.com/fschlatt/clubs_gym"
__docs__ = (
    "clubs is an open ai gym environment for" " running arbitrary poker configurations."
)


def __register():
    try:
        env_configs = {}
        for name, config in configs.__dict__.items():
            if not name.endswith("_PLAYER"):
                continue
            env_id = "".join(sub_string.title() for sub_string in name.split("_"))
            env_id += "-v0"
            env_configs[env_id] = config
        envs.register(env_configs)
    except ImportError:
        pass


__register()
