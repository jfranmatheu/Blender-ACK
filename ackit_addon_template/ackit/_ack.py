from enum import Enum, auto
from typing import Callable, Type, Any, Literal, overload, Union, Annotated

from .registry.reg_types import *
from .registry.reg_deco import *
from .registry.flags import *
from .registry.props import *
from .enums import *
from . import types as ack_types
from .registry.polling import *
from .registry.reg_types.nodes.sockets.annotation import NodeSocketWrapper, NodeSocketInput as _NodeSocketInput, NodeSocketOutput as _NodeSocketOutput
from .registry import reg_helpers


__all__ = [
    'ACK',
]


class ACK:

    class Register:
        Property = reg_helpers.register_property
        Properties = reg_helpers.batch_register_properties

        class Types:
            class Ops:
                Generic = Operator
                Action = Action
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
            
            class Nodes:
                Node = Node
                Tree = NodeTree
                Socket = NodeSocket

        class FromFunction:
            ACTION = Action.from_function
            PANEL = PanelFromFunction
            MENU = Menu.from_function
            PIE_MENU = PieMenu.from_function
            POPOVER = Popover.from_function

    Types = ack_types
    '''Event = FakeEvent
    EventType = EventType
    EventValue = EventValue'''

    class Returns:
        Operator = OpsReturn
        Submodal = SubmodalReturn

    Props = PropertyTypes
    PropsWrapped = WrappedTypedPropertyTypes

    # Explicitly annotate the NodeInput and NodeOutput with proper signatures
    @staticmethod
    def NodeInput(socket_type: Type[NodeSocket], multi: bool = False) -> NodeSocketWrapperInstance:
        """
        Create an input socket annotation.
        
        Args:
            socket_type: The type of node socket (e.g., NodeSocketFloat)
            multi: Whether this is a multi-input socket
            
        Returns:
            A NodeSocketWrapper descriptor for the input socket
        """
        return _NodeSocketInput(socket_type, multi) # type: ignore

    @staticmethod
    def NodeOutput(socket_type: Type[NodeSocket]) -> NodeSocketWrapperInstance:
        """
        Create an output socket annotation.
        
        Args:
            socket_type: The type of node socket (e.g., NodeSocketFloat)
            
        Returns:
            A NodeSocketWrapper descriptor for the output socket
        """
        return _NodeSocketOutput(socket_type) # type: ignore


    class Flags:
        OPERATOR = OperatorOptions
        MODAL = ModalFlags
        PANEL = PanelOptions
        NODE_CATEGORY = node_category

    Poll = Polling
