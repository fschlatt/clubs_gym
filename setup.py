import os

from setuptools import find_packages, setup

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

PATH_ROOT = os.path.dirname(__file__)
builtins.__CLUBS_GYM__SETUP__: bool = True

import clubs_gym  # noqa

file_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(file_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

with open(os.path.join(file_dir, "requirements.txt")) as file:
    requirements = file.read().split("\n")

with open(os.path.join(file_dir, "extra-requirements.txt")) as file:
    extra_requirements = file.read().split("\n")


setup(
    name="clubs-gym",
    version=clubs_gym.__version__,
    description=clubs_gym.__docs__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=clubs_gym.__author__,
    url=clubs_gym.__homepage__,
    license=clubs_gym.__license__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=["reinforcement learning", "poker", "AI", "gym"],
    packages=find_packages(exclude=["test", "test.*"]),
    python_requires=">=3.6",
    install_requires=requirements,
    include_package_data=True,
    extras_requires={"render": extra_requirements},
    project_urls={
        "Bug Reports": "https://github.com/fschlatt/clubs_gym/issues",
        "Source": "https://github.com/fschlatt/clubs_gym/",
    },
)
