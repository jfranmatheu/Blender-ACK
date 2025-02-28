from typing import TypeVar

import bpy

from .node import Node
from .node_tree import NodeTree
from .node_socket import NodeSocket
from .sockets import NodeSocketTypes, NodeSocketAnnotation


__all__ = [
    'Node', 'NodeTree', 'NodeSocket',
    'NodeSocketTypes', 'NodeSocketAnnotation',
]

# Create a virtual type that combines bpy and ackit Operator types for proper typing.
T = TypeVar('T', bound=bpy.types.Node | Node)
