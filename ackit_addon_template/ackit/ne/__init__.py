from .btypes import *
from .categories import register as register_node_categories, unregister as unregister_node_categories
from .socket_types import * # Expose all specific socket types
from .annotations import NodeInput, NodeOutput
from .socket_casting import SocketCast

# Expose base types
__all__ = [
    'Node',
    'NodeSocket',
    'NodeTree',
    'NodeInput',
    'NodeOutput',
    'register_node_categories', # Function to register categories
    'unregister_node_categories', # Function to unregister categories
    'SocketTypes',
    'SocketCast',
]

# Add all socket types from socket_types.py to __all__
# _socket_type_names = [name for name in globals() if name.startswith('NodeSocket') and name != 'NodeSocket']
# __all__.extend(_socket_type_names)
