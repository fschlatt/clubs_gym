import os

from setuptools import setup

import clubs

file_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(file_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="clubs-gym",
    version=clubs.__version__,
    description=clubs.__docs__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=clubs.__author__,
    url=clubs.__homepage__,
    license=clubs.__license__,
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
        "Bug Reports": "https://github.com/fschlatt/clubs/issues",
        "Source": "https://github.com/fschlatt/clubs/",
    },
)
