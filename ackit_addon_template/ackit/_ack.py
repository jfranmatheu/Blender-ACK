from enum import Enum, auto
from typing import Callable, Type, Any, Literal, overload, Union, Annotated, TypeVar, ClassVar

from bpy import types as bpy_types

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
from . import flags
from . import metadata
from .metadata import Node as _MetadataNodeFunc, NodeSocket as _MetadataSocketFunc # Import the specific functions
from .metadata import Operator as _MetadataOperatorFunc
from .metadata import OperatorTypeVar as _MetadataOperatorTypeVar
from .flags import NODE_CATEGORY as _NodeCategoryFunc # Import the specific function
from .metadata import NodeTypeVar as _MetadataNodeTypeVar # Import TypeVar from metadata
from .flags import NodeT as _FlagsNodeT # Import TypeVar from flags
from .metadata import NodeSocketTypeVar as _MetadataNodeSocketTypeVar
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
from .ui import helpers as _ui_helpers # Import the helpers module
from .ui.helpers import ui_extend as _ui_extend_func
from .ui.helpers import UIOverride as _UIOverride_class

# NE
from .ne import Node as _Node
from .ne import NodeTree
from .ne import NodeSocket
from .ne.annotations_internal import NodeSocketInput as _NodeSocketInput # Alias internal
from .ne.annotations_internal import NodeSocketOutput as _NodeSocketOutput # Alias internal
from .ne import socket_types as _socket_types_module # The module itself

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

# Import flag classes/enums
from .flags import OPERATOR as _FlagsOperatorClass
from .flags import MODAL as _FlagsModalClass
from .flags import PANEL as _FlagsPanelEnum


__all__ = [
    'ACK',
]


# Definir TypeVar. Esto nos ayuda a tener tipado del tipo de NodeSocket suyacente,
# el cual usamos para definir el tipo de socket para inputs y outputs.
SocketT = TypeVar('SocketT', bound=NodeSocket)

UIDrawFunc = Callable[[bpy_types.Context, bpy_types.UILayout], None]


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
        # Configuration
        @staticmethod
        def add_metadata(label: str | None = None, tooltip: str = "") -> Callable[[Type[_MetadataOperatorTypeVar]], Type[_MetadataOperatorTypeVar]]:
            """Adds metadata to an Operator class. Alias for metadata.Operator."""
            return _MetadataOperatorFunc(label=label, tooltip=tooltip)

        # --- Renamed Aliases for Flags/Polling --- 
        Flags: ClassVar[Type[_FlagsOperatorClass]] = _FlagsOperatorClass
        ModalFlags: ClassVar[Type[_FlagsModalClass]] = _FlagsModalClass
        
        # Other (Example)
        # register_shortcut = ... # TODO

    class UI:
        """Base types, creators, and config for UI elements."""
        Panel = Panel
        Menu = Menu
        PieMenu = PieMenu
        Popover = Popover
        UIList = UIList
        # Configuration
        # --- Renamed Aliases for Flags/Polling --- 
        PanelFlags: ClassVar[Type[_FlagsPanelEnum]] = _FlagsPanelEnum
        # UI Draw Helpers
        @staticmethod
        def extend_layout(target_cls: Type[bpy_types.Panel] | Type[bpy_types.Menu], prepend: bool = False) -> Callable[[UIDrawFunc], UIDrawFunc]:
            """
            Decorator to register a function to be appended or prepended to a Blender UI class's draw method.
            
            Usage:
                @ACK.UI.extend_layout(bpy.types.SOME_PT_panel, prepend=True)
                def my_draw_func(context, layout):
                    layout.label(text="Hello")

            Args:
                target_cls: The Blender Panel or Menu class (e.g., bpy.types.OBJECT_MT_context_menu).
                prepend: Whether to prepend the function instead of appending.
                
            Returns:
                Callable: The decorated function with (bpy.types.Context, bpy.types.UILayout) arguments.
            """
            return _ui_extend_func(target_cls, prepend)

        @staticmethod
        def override_layout(target_cls: Type[bpy_types.Panel] | Type[bpy_types.Menu], poll: Callable[[bpy_types.Context], bool]):
            """
            Decorator to override the layout of a Blender UI class.
            
            Usage:
                @ACK.UI.override_layout(bpy.types.SOME_PT_panel, poll=lambda context: context.scene.some_prop)
                class OverrideOfSomePanel(bpy.types.Panel):
                    def draw(self, context):
                        # Method to override from the original 'bpy.types.SOME_PT_panel' class.
                        self.layout.label(text="Hello")
            
            Args:
                target_cls: The Blender Panel or Menu class (e.g., bpy.types.OBJECT_PT_context_menu).
                poll: A function that returns a boolean indicating if the override should be applied.

            Returns:
                Callable: The decorated class with the overridden draw method (or any other overriden methods).
            """
            return _UIOverride_class.decodecorator(target_cls, poll)

    class NE: # Node Editor
        """Base types, creators, and config for Node Editor.
            WARNING: You might get quite some ACkNE if writing too much NodeEditor code."""
        # Define base types as direct aliases
        Node = _Node
        Tree = NodeTree
        Socket = NodeSocket
        # Configuration - Wrap original functions in staticmethods with precise signatures
        
        @staticmethod
        def add_node_metadata(label: str | None = None, tooltip: str = "", icon: str = 'NONE') -> Callable[[Type[_MetadataNodeTypeVar]], Type[_MetadataNodeTypeVar]]:
            """Adds metadata to a Node class. Alias for metadata.Node."""
            return _MetadataNodeFunc(label=label, tooltip=tooltip, icon=icon)

        @staticmethod
        def add_socket_metadata(label: str | None = None, tooltip: str = "", subtype_label: str = '', color: tuple[float, float, float, float] = (0.5, 0.5, 0.5, 1.0)) -> Callable[[Type[_MetadataNodeSocketTypeVar]], Type[_MetadataNodeSocketTypeVar]]:
            """Adds metadata to a NodeSocket class. Alias for metadata.NodeSocket."""
            return _MetadataSocketFunc(label=label, tooltip=tooltip, subtype_label=subtype_label, color=color)

        @staticmethod
        def add_node_to_category(category: str) -> Callable[[Type[_FlagsNodeT]], Type[_FlagsNodeT]]:
            """Adds a category to a Node class. Alias for flags.NODE_CATEGORY."""
            return _NodeCategoryFunc(category=category)

        NodeFlags = flags.NodeFlags

        # Socket Definition
        SocketTypes = _socket_types_module.SocketTypes
        
        # Socket Casting
        SocketCast = ne.SocketCast

        # Explicitly annotate the NodeInput and NodeOutput with proper signatures
        @staticmethod
        def InputSocket(socket_type: Type[SocketT], multi: bool = False) -> SocketT:
            """
            Create an input socket annotation.
            
            Args:
                socket_type: The type of node socket (e.g., socket_types.NodeSocketFloat)
                multi: Whether this is a multi-input socket
                
            Returns:
                The actual socket instance (typed as SocketT) when accessed on a node instance.
            """
            # Call the correctly typed internal function
            # The type ignore might still be needed if the IDE struggles with the descriptor protocol
            return _NodeSocketInput(socket_type, multi) # type: ignore

        @staticmethod
        def OutputSocket(socket_type: Type[SocketT]) -> SocketT:
            """
            Create an output socket annotation.
            
            Args:
                socket_type: The type of node socket (e.g., socket_types.NodeSocketFloat)
                
            Returns:
                The actual socket instance (typed as SocketT) when accessed on a node instance.
            """
            # Call the correctly typed internal function
            # The type ignore might still be needed
            return _NodeSocketOutput(socket_type) # type: ignore

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
