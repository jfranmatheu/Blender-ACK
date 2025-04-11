from enum import Enum, auto
from typing import Callable, Type, Any, Literal, overload, Union, Annotated, TypeVar

from .registry.reg_types import *
from .registry.reg_deco import *
from .registry.flags import *
from .registry.props import *
from .enums import *
from . import types as ack_types
from .registry.polling import *
from .registry.reg_types.nodes.sockets.annotation import NodeSocketWrapper, NodeSocketInput as _NodeSocketInput, NodeSocketOutput as _NodeSocketOutput
from .registry import reg_helpers
from .registry import metadata
from .registry import flags
from .types.nodes.node_socket import NodeSocket
from .types.nodes import socket_types


__all__ = [
    'ACK',
]


# Definir TypeVar. Esto nos ayuda a tener tipado del tipo de NodeSocket suyacente,
# el cual usamos para definir el tipo de socket para inputs y outputs.
SocketT = TypeVar('SocketT', bound=NodeSocket)


# Explicitly annotate the NodeInput and NodeOutput with proper signatures
def NodeInput(socket_type: Type[SocketT], multi: bool = False) -> SocketT:
    """
    Create an input socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., NodeSocketFloat)
        multi: Whether this is a multi-input socket
        
    Returns:
        A NodeSocketWrapper descriptor for the input socket
    """
    return _NodeSocketInput(socket_type, multi) # type: ignore

def NodeOutput(socket_type: Type[SocketT]) -> SocketT:
    """
    Create an output socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., NodeSocketFloat)
        
    Returns:
        A NodeSocketWrapper descriptor for the output socket
    """
    return _NodeSocketOutput(socket_type) # type: ignore


class ACK:
    # Polling functions/decorators.
    Poll = Polling

    # Property Accessors (Defining property types)
    Prop = PropertyTypes
    PropTyped = WrappedTypedPropertyTypes

    class OPS:
        """Base types and helpers for Blender Operators."""
        Generic = Operator
        Action = Action
        Modal = Modal

        # Create types from functions with these decorators.
        create_action_from_func = Action.from_function

        # Decorators for OPS BTypes classes.
        add_metadata = metadata.Operator
        add_flag = flags.OPERATOR
        add_modal_flag = flags.MODAL
        add_run_condition = Polling  # Alias.

        register_shortcut = object()  # TODO

    class UI:
        """Base types and helpers for Blender UI elements."""
        Panel = Panel
        Menu = Menu
        PieMenu = PieMenu
        Popover = Popover
        UIList = UIList
        
        # Create types from functions with these decorators.
        create_panel_from_function      = PanelFromFunction
        create_menu_from_function       = Menu.from_function
        create_piemenu_from_function    = PieMenu.from_function
        create_popover_from_function    = Popover.from_function

        # Decorators for UI BTypes classes.
        add_panel_flag = flags.PANEL
        add_display_condition = Polling  # Alias.

    class NE: # Node Editor
        """Base types and helpers for Blender Node Editor elements."""
        Node = Node
        Tree = NodeTree
        Socket = NodeSocket

        # Decorators for NodeEditor BTypes classes.
        add_node_metadata = metadata.Node
        add_socket_metadata = metadata.NodeSocket
        add_node_to_category = flags.NODE_CATEGORY

        # Used to define inputs and outputs in the custom Nodes.
        new_input = NodeInput
        new_output = NodeOutput
        socket_types = socket_types

    class DATA:
        """Base types and helpers for Blender Data storage."""
        AddonPreferences = AddonPreferences
        PropertyGroup = PropertyGroup

        # Helpers to register properties in bpy.types.
        register_property = reg_helpers.register_property  # Alias.
        batch_register_properties = reg_helpers.batch_register_properties  # Alias.

    class Register:
        """Register properties, property groups, app handlers, shortcuts etc."""
        property = reg_helpers.register_property
        properties_batch = reg_helpers.batch_register_properties
        # TODO: PG.CHILD AND PG.ROOT, Handler, Timer, RNA_SUB...
        '''PropertyGroup = _register_pg_deco
        AppHandler = _register_handler_deco
        AppTimer = _register_timer_deco
        MsgbusListener = _register_msgbus_deco'''

    Reg = Register  # Alias



'''
# Combined Approach: V4 Verb-Based + BType Accessor
class ACK_verb:
    """
    ACK Facade: Combines Verb-Based actions (Define, Register, Create, Configure)
    with a direct BType accessor grouped by Blender element type.
    """
    # ==================================================
    # Verb-Based Structure (Approach V4 - Primary)
    # ==================================================

    # === Define (Base types & Accessors for structure definition) ===
    class Define:
        """Access base types for inheritance and utilities for defining structure."""
        # --- BTypes for Inheritance (Canonical definitions) ---
        class Ops:
            Generic = Operator
            Action = Action # Often Operator + Flags
            Modal = Modal
        
        class UI:
            Panel = Panel
            Menu = Menu
            PieMenu = PieMenu
            Popover = Popover
            UIList = UIList

        class Data:
            AddonPreferences = AddonPreferences
            PropertyGroup = PropertyGroup

        class NE:
            # Node Editor (NE)
            Node = Node
            NodeTree = NodeTree
            NodeSocket = NodeSocket
        # --- End BTypes ---

        class FromFunction:
            """Create BTypes directly from functions using decorators."""
            ACTION = Action.from_function
            PANEL = PanelFromFunction
            MENU = Menu.from_function
            PIE_MENU = PieMenu.from_function
            POPOVER = Popover.from_function

        # Property Accessors (Defining property types)
        Prop = PropertyTypes
        PropTyped = WrappedTypedPropertyTypes

        # Node Utilities (Defining sockets)
        NodeInput = NodeInput
        NodeOutput = NodeOutput
        NodeSocketTypes = socket_types

    Def = Define  # Alias.

    # === Register (Direct calls & registering decorators) ===
    class Register:
        """Register properties, property groups, app handlers, shortcuts etc."""
        Property = reg_helpers.register_property
        PropertiesBatch = reg_helpers.batch_register_properties
        # PropertyGroup = _register_pg_deco
        # AppHandler = _register_handler_deco
        # AppTimer = _register_timer_deco
        # MsgbusListener = _register_msgbus_deco
        # OperatorShortcut = _register_shortcut_deco

    Reg = Register  # Alias.

    # === Configure (Decorators adding metadata/flags/poll to existing BTypes) ===
    class Configure:
        """Configure existing BType classes using decorators (Metadata, Flags, Polling)."""
        Metadata = metadata
        Flags = flags
        Polling = Polling

    Conf = Configure  # Alias.
    
    
    # ==================================================
    # BType Grouped Accessor (Alternative)
    # ==================================================
    class BTypes:
        """Alternative accessor for base BTypes, grouped by element type."""

        class Ops:
            """Base types for Blender Operators."""
            Generic = Operator        # Alias to canonical definition
            Action = Action   # Alias
            Modal = Modal     # Alias

        class UI:
            """Base types for Blender UI elements."""
            Panel = Panel             # Alias
            Menu = Menu               # Alias
            PieMenu = PieMenu         # Alias
            Popover = Popover         # Alias
            UIList = UIList           # Alias

        class NE: # Node Editor
            """Base types for Blender Node Editor elements."""
            Node = Node               # Alias
            Tree = NodeTree           # Alias
            Socket = NodeSocket       # Alias

        class Data:
            """Base types for Blender Data storage."""
            AddonPreferences = AddonPreferences # Alias
            PropertyGroup = PropertyGroup       # Alias
'''