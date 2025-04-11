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
    # Core utility - Keep top-level? OK for now.
    Poll = Polling

    class OPS:
        """Base types, creators, and config for Operators."""
        Generic = Operator
        Action = Action
        Modal = Modal
        # Creators
        create_action_from_func = Action.from_function
        # Configuration
        add_metadata = metadata.Operator
        add_flag = flags.OPERATOR
        add_modal_flag = flags.MODAL
        add_condition = Polling # Standardized alias
        # Registration/Other
        register_shortcut = object() # TODO

    class UI:
        """Base types, creators, and config for UI elements."""
        Panel = Panel
        Menu = Menu
        PieMenu = PieMenu
        Popover = Popover
        UIList = UIList
        # Creators
        create_panel_from_func = PanelFromFunction # Standardized name
        create_menu_from_func = Menu.from_function # Standardized name
        create_piemenu_from_func = PieMenu.from_function # Standardized name
        create_popover_from_func = Popover.from_function # Standardized name
        # Configuration
        add_flag = flags.PANEL # Keep specific name? add_panel_flag maybe better
        add_condition = Polling # Standardized alias

    class NE: # Node Editor
        """Base types, creators, and config for Node Editor."""
        Node = Node
        Tree = NodeTree
        Socket = NodeSocket
        # Configuration
        add_node_metadata = metadata.Node # Keep specific name
        add_socket_metadata = metadata.NodeSocket # Keep specific name
        add_node_to_category = flags.NODE_CATEGORY # Keep specific name
        # Socket Definition
        new_input = NodeInput
        new_output = NodeOutput
        socket_types = socket_types

    class DATA:
        """Base types and property definitions for Data."""
        AddonPreferences = AddonPreferences
        PropertyGroup = PropertyGroup
        # Property Definition Types (Moved from top-level)
        Prop = PropertyTypes
        PropTyped = WrappedTypedPropertyTypes

    class Register:
        """Centralized registration functions/decorators."""
        # Property registration (Moved from DATA aliases)
        property = reg_helpers.register_property
        properties_batch = reg_helpers.batch_register_properties
        # TODO: Add others (PG, Handler, Timer, Msgbus...)
        # PropertyGroup = _register_pg_deco
        # AppHandler = _register_handler_deco
        # AppTimer = _register_timer_deco
        # MsgbusListener = _register_msgbus_deco
        # ... etc


# __all__ = ['ACK'] # Ensure __all__ is updated if needed
