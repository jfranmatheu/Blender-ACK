from enum import Enum, auto
from typing import Callable, Type

from .types.btypes import *
from .decorators import *
from .helpers import *

__all__ = [
    'ACK',
]


class ACK:
    class Types:
        class Ops:
            GENERIC = Operator      # Base operator type
            ACTION = Action         # Simple operators with single action
            MODAL = Modal           # Complex operators with modal loop

        class Data:
            PREFS = AddonPreferences   # Addon preferences
            PROP_GROUP = PropertyGroup # Property group definitions
        
        class UI:
            PANEL = Panel       # Regular panels
            MENU = Menu         # Regular menus
            PIE_MENU = PieMenu  # Pie menus
            POPOVER = Popover   # Popover panels
            LIST = UIList       # UI Lists
        
        # class Tools:
        #     TOOL = Tool                 # Tool system definitions
        #     GIZMO = Gizmo               # Individual gizmos
        #     GIZMO_GROUP = GizmoGroup    # Gizmo collections
    
    class Props:
        Typed = typed_props
        Wrapped = wrapped_props
    
    class Deco:
        class UI:
            PANEL = PanelFromFunction
            MENU = menu_from_function

        class Options:
            OPERATOR = OperatorOptions  # Operator options (register, undo, etc)
            MODAL = ModalFlags          # Modal flags (mouse, raycast, draw3d, draw2d, etc)
            PANEL = PanelOptions        # Panel options (default_closed, hide_header, etc)
            # GIZMO = GizmoFlags          # Gizmo flags (raycast, mouse, draw3d, draw2d, etc)
        
        Poll = Poll




# --------------------------------------------------------------

