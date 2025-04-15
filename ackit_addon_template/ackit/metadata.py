from typing import Callable, Type, Any, TypeVar

# Updated imports to reflect the new structure
# Assuming base classes are imported into the __init__.py of their respective btypes folders
from .ne.btypes import Node as _NodeType
from .ne.btypes import NodeSocket as _NodeSocketType
from .ops.btypes import Generic as _OperatorType


# Define TypeVars bound to base classes
NodeTypeVar = TypeVar('NodeTypeVar', bound=_NodeType)
NodeSocketTypeVar = TypeVar('NodeSocketTypeVar', bound=_NodeSocketType)
OperatorTypeVar = TypeVar('OperatorTypeVar', bound=_OperatorType)


def Node(label: str | None = None, tooltip: str = "", icon: str = 'NONE') -> Callable[[Type[NodeTypeVar]], Type[NodeTypeVar]]:
    def wrapper(cls: Type[NodeTypeVar]) -> Type[NodeTypeVar]:
        cls.bl_label = label or cls.__name__
        cls.bl_description = tooltip
        cls.bl_icon = icon
        return cls
    return wrapper


def NodeSocket(label: str | None = None, tooltip: str = "", subtype_label: str = '', color: tuple[float, float, float, float] = (0.5, 0.5, 0.5, 1.0)) -> Callable[[Type[NodeSocketTypeVar]], Type[NodeSocketTypeVar]]:
    def wrapper(cls: Type[NodeSocketTypeVar]) -> Type[NodeSocketTypeVar]:
        cls.bl_label = label or cls.__name__
        cls.bl_description = tooltip
        cls.bl_subtype_label = subtype_label
        cls.color = color
        return cls
    return wrapper

def Operator(label: str | None = None, tooltip: str = "") -> Callable[[Type[OperatorTypeVar]], Type[OperatorTypeVar]]:
    def wrapper(cls: Type[OperatorTypeVar]) -> Type[OperatorTypeVar]:
        cls.bl_label = label or cls.__name__
        cls.bl_description = tooltip
        return cls
    return wrapper
