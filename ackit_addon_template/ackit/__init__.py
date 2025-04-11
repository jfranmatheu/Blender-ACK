"""
Addon Creator Kit (ackit or ACKit) - A comprehensive toolkit for Blender addon development
"""

# Expose the main Facade class
from ._ack import ACK

# Expose top-level enums if desired
from . import enums

# Expose globals utility facade class.
from .globals import GLOBALS

# Expose core loader for addon registration
from .core.addon_loader import AddonLoader
from .core.auto_load import AutoLoad

# Expose AutoCode if needed
from .auto_code import AutoCode # Assuming auto_code.py is still top-level

# Version (Consider moving this to a dedicated version file or metadata)
__version__ = (0, 1, 0)

__all__ = [
    'ACK',
    'enums',
    'AddonLoader',
    'AutoCode',
    '__version__',
]
