from enum import Enum, auto
from typing import Callable, Type, Any, Literal, overload, Union, Annotated, TypeVar

# --- Core Imports ---
from . import core # For potential access if needed

# --- Domain Imports ---
from . import ops
from . import ui
from . import ne
from . import data
from . import app

# --- Utility Imports ---
from . import enums # Keep top-level enums
from . import flags # Top-level flags module
from . import metadata # Top-level metadata module
from . import utils # Top-level utils module (contains Polling)

# --- Specific Imports for Facade Aliases ---
# Note: Imports below assume __init__.py files expose necessary symbols

# Ops
from .ops import Generic as _GenericOperator # Avoid collision with typing.Generic if used
from .ops import Action
from .ops import Modal

# UI
from .ui import Panel, PanelFromFunction
from .ui import Menu
from .ui import PieMenu
from .ui import Popover
from .ui import UIList

# NE
from .ne import Node
from .ne import NodeTree
from .ne import NodeSocket
from .ne import NodeInput # From ne.annotations
from .ne import NodeOutput # From ne.annotations
from .ne import socket_types # The module itself

# Data
from .data import AddonPreferences
from .data import PropertyGroup
from .data import PropertyTypes # From data.props
from .data import WrappedTypedPropertyTypes # From data.props
from .data import register_property # From data.helpers
from .data import batch_register_properties # From data.helpers
from .data import subscribe_to_rna_change # From data.subscriptions
from .data import subscribe_to_rna_change_based_on_context # From data.subscriptions

# App
from .app import Handlers # From app.handlers
from .app import new_timer_as_decorator, new_timer # Renamed? Check app.timers
from .app import RegisterKeymap # From app.keymaps

# Utils
from .utils import Polling # From utils.polling


__all__ = [
    'ACK',
]


# Definir TypeVar. Esto nos ayuda a tener tipado del tipo de NodeSocket suyacente,
# el cual usamos para definir el tipo de socket para inputs y outputs.
# SocketT = TypeVar('SocketT', bound=NodeSocket) # REMOVED


# Explicitly annotate the NodeInput and NodeOutput with proper signatures
# def NodeInput(socket_type: Type[SocketT], multi: bool = False) -> SocketT: # REMOVED
#     """
#     Create an input socket annotation.
#     
#     Args:
#         socket_type: The type of node socket (e.g., NodeSocketFloat)
#         multi: Whether this is a multi-input socket
#         
#     Returns:
#         A NodeSocketWrapper descriptor for the input socket
#     """
#     return _NodeSocketInput(socket_type, multi) # type: ignore

# def NodeOutput(socket_type: Type[SocketT]) -> SocketT: # REMOVED
#     """
#     Create an output socket annotation.
#     
#     Args:
#         socket_type: The type of node socket (e.g., NodeSocketFloat)
#         
#     Returns:
#         A NodeSocketWrapper descriptor for the output socket
#     """
#     return _NodeSocketOutput(socket_type) # type: ignore


class ACK:
    # Core utility polling functions/decorators.
    Poll = Polling

    # Fast-access to Props. (they should not be here for consistency but they are heavily used and need a more direct access)
    Prop = PropertyTypes  # Alias for DATA.Prop.
    PropTyped = WrappedTypedPropertyTypes  # Alias for DATA.PropTyped.

    class Ops:
        """Base types, creators, and config for Operators."""
        Generic = _GenericOperator
        Action = Action
        Modal = Modal
        # Creators
        create_action_from_func = Action.from_function
        # Configuration
        add_metadata = metadata.Operator
        add_flag = flags.OPERATOR
        add_modal_flag = flags.MODAL
        add_run_condition = Polling # alias of ACK.Poll
        # Other (Example)
        # register_shortcut = ... # TODO

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
        add_panel_flag = flags.PANEL
        add_display_condition = Polling # alias of ACK.Poll

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

    class Data:
        """Base types, property definitions, and data-related registration."""
        # Base Types
        AddonPreferences = AddonPreferences
        PropertyGroup = PropertyGroup
        # Property Definition Types
        Prop = PropertyTypes  # annotation
        PropTyped = WrappedTypedPropertyTypes  # descriptor
        # Property Registration Helpers
        register_property = register_property
        batch_register_properties = batch_register_properties
        # PropertyGroup Registration (Conceptual)
        # PropertyGroupRole = object()  # use as decorator
        # RNA Subscription (MsgBus)
        subscribe_to_rna = subscribe_to_rna_change
        subscribe_to_rna_context = subscribe_to_rna_change_based_on_context

    class App: # Or Application?
        """Application-level handlers, timers, etc."""
        Handler = Handlers # Enum from app.handlers
        Timer = new_timer_as_decorator # Decorator func from app.timers
        # Keymap = RegisterKeymap # Class from app.keymaps
