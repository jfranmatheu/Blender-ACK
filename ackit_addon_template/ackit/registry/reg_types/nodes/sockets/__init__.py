from .annotation import NodeSocketAnnotation, NodeSocketWrapper
from .socket_types import *

__all__ = ['NodeSocketAnnotation', 'NodeSocketTypes']


class NodeSocketTypes:
    FLOAT = NodeSocketFloat
    FLOAT_VECTOR_3 = NodeSocketFloatVector3
    FLOAT_VECTOR_2 = NodeSocketFloatVector2
    INT = NodeSocketInt
    INT_VECTOR_3 = NodeSocketIntVector3
    INT_VECTOR_2 = NodeSocketIntVector2
    BOOL = NodeSocketBool
    STRING = NodeSocketString
    COLOR = NodeSocketColor
