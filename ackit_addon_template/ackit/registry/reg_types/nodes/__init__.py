from typing import TypeVar

import bpy

from .node import Node
from .node_tree import NodeTree
from .node_socket import NodeSocket
from .sockets import NodeSocketInput, NodeSocketOutput, NodeSocketWrapper


__all__ = [
    'Node', 'NodeTree', 'NodeSocket',
    'NodeSocketInput', 'NodeSocketOutput', 'NodeSocketWrapper',
]

# Create a virtual type that combines bpy and ackit Operator types for proper typing.
T = TypeVar('T', bound=bpy.types.Node | Node)
