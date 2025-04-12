from typing import Callable, Type, Any

# Updated imports to reflect the new structure
# Assuming base classes are imported into the __init__.py of their respective btypes folders
from .ne.btypes import Node
from .ne.btypes import NodeSocket
from .ops.btypes import Generic # Assuming Operator base class is in ops.btypes


# Type hints updated to use Any for now, or specific types if available

def Node(label: str | None = None, tooltip: str = "", icon: str = 'NONE') -> Callable[[Type[Node]], Type[Node]]:
    def wrapper(cls: Type[Node]):
        cls.bl_label = label or cls.__name__
        cls.bl_description = tooltip
        cls.bl_icon = icon
        return cls
    return wrapper


def NodeSocket(label: str | None = None, tooltip: str = "", subtype_label: str = '') -> Callable[[Type[NodeSocket]], Type[NodeSocket]]:
    def wrapper(cls: Type[NodeSocket]):
        cls.bl_label = label or cls.__name__
        cls.description = tooltip
        cls.bl_subtype_label = subtype_label
        return cls
    return wrapper

def Operator(label: str | None = None, tooltip: str = "") -> Callable[[Type[Generic]], Type[Generic]]:
    def wrapper(cls: Type[Generic]):
        cls.bl_label = label or cls.__name__
        cls.bl_description = tooltip
        return cls
    return wrapper
