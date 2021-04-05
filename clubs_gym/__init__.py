__version__ = "0.1.3"
__author__ = "Ferdinand Schlatt"
__license__ = "GPL-3.0"
__copyright__ = f"Copyright (c) 2020, {__author__}."
__homepage__ = "https://github.com/fschlatt/clubs_gym"
__docs__ = (
    "clubs is an open ai gym environment for running arbitrary poker configurations."
)

try:
    # This variable is injected in the __builtins__ by the build
    # process. It used to enable importing subpackages of skimage when
    # the binaries are not built
    __CLUBS_GYM_SETUP__  # type: ignore
except NameError:
    __CLUBS_GYM_SETUP__ = False

if __CLUBS_GYM_SETUP__:  # type: ignore
    pass
else:
    from . import agent, envs

import clubs

__all__ = ["agent", "envs"]
ENVS = []


def __register():
    try:
        env_configs = {}
        for name, config in clubs.configs.__dict__.items():
            if not name.endswith("_PLAYER"):
                continue
            env_id = "".join(sub_string.title() for sub_string in name.split("_"))
            env_id += "-v0"
            env_configs[env_id] = config
            ENVS.append(env_id)
        envs.register(env_configs)
    except ImportError:
        pass


__register()
