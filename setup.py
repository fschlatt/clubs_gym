import os

from setuptools import setup

__version__ = "0.1.0"
__author__ = "Ferdinand Schlatt"
__license__ = "GLP-3.0"
__copyright__ = f"Copyright (c) 2020, {__author__}."
__homepage__ = "https://github.com/fschlatt/clubs"
__docs__ = (
    "clubs is a general purpose python poker engine for"
    " running arbitrary poker configurations."
)

file_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(file_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="clubs-gym",
    version=__version__,
    description=__docs__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    url=__homepage__,
    license=__license__,
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
    ],
    keywords=["reinforcement learning", "poker", "AI", "gym"],
    packages=["clubs"],
    python_requires=">=3.6",
    install_requires=["numpy>=1.16.6"],
    extras_requires={"render": ["asciimatics>=1.0.0", "flask>=1.0.0"]},
    project_urls={
        "Bug Reports": "https://github.com/fschlatt/clubs_gym/issues",
        "Source": "https://github.com/fschlatt/clubs_gym/",
    },
)
