"""
el_data

Helper functions for accessing internationalisation data.
"""

__version__ = "0.2.0"
__author__ = 'Andrew Cunningham'
__credits__ = 'Enabling Languages'

from .unihan import *
from .encodings import *
from .data import *

del(unihan)
del(encodings)
del(data)
