import os

from setuptools import find_packages, setup

import pyker

file_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(file_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='pyker',
    version=pyker.__version__,
    description=pyker.__docs__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=pyker.__author__,
    url=pyker.__homepage__,
    license=pyker.__license__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Games/Entertainment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: GPL-3.0',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords=['reinforcment learning', 'poker', 'AI', 'gym'],
    packages=find_packages(where='pyker'),
    python_requires='>=3.6',
    install_requires=['numpy>=1.16'],
    project_urls={
        'Bug Reports': 'https://github.com/fschlatt/pyker/issues',
        'Source': 'https://github.com/fschlatt/pyker/',
    },
)
