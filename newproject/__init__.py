"""
New Project package
"""

import warnings

from packaging.version import Version

from newproject.interfaces import *

warnings.simplefilter("ignore")

__version__ = Version("2021.1.2b3")
