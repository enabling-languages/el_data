"""
el_data

Helper functions for accessing internationalisation related data.
"""

__version__ = "0.3.5"
__author__ = 'Andrew Cunningham'
__credits__ = 'Enabling Languages'

from .unihan import *
from .ethiopic import *
from .encodings import *
from .cldr import *
from .data import *

del(unihan)
del(ethiopic)
del(encodings)
del(cldr)
del(data)
