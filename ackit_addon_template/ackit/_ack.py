from enum import Enum, auto
from typing import Callable, Type

from .registry.reg_types import *
from .registry.reg_deco import *
from .registry.flags import *
from .registry.props import *
from .enums import *
from .registry.polling import *

__all__ = [
    'ACK',
]


class ACK:
    
    class Register:
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

    '''class Types:
        Event = FakeEvent
        EventType = EventType
        EventValue = EventValue'''

    class Returns:
        Operator = OpsReturn
        Submodal = SubmodalReturn

    Props = PropertyTypes
    PropsWrapped = WrappedTypedPropertyTypes
    PropsLayout = DescriptorTypedPropertyTypes

    class Flags:
        OPERATOR = OperatorOptions
        MODAL = ModalFlags
        PANEL = PanelOptions
        NODE_CATEGORY = node_category

    Poll = Polling

    class Nodes:
        Socket = NodeSocketAnnotation
        SocketTypes = NodeSocketTypes
