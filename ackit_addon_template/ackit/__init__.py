"""
Addon Creator Kit (ackit or ACKit) - A comprehensive toolkit for Blender addon development
"""

from .registry import AutoLoad, AddonLoader
from .globals import GLOBALS
from .auto_code import AutoCode
from .utils.operator import OpsReturn, SubmodalReturn
from .utils.cursor import Cursor


__version__ = (0, 1, 0)
