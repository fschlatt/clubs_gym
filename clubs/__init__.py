from . import configs, poker
from .poker.engine import Dealer

__all__ = ['configs', 'poker', 'Dealer']
__version__ = '0.1.0'
__author__ = 'Ferdinand Schlatt'
__license__ = 'GLP-3.0'
__copyright__ = f'Copyright (c) 2020, {__author__}.'
__homepage__ = 'https://github.com/fschlatt/clubs'
__docs__ = ('clubs is a general purpose python poker engine for'
            ' running arbitrary poker configurations.')
