from enum import Enum, auto
from typing import TypeVar, Generic, Union, Optional, Type, Any, cast, overload
import math

from bpy import types as bpy_types

# Updated relative imports
from .btypes.node_socket import NodeSocket
from .btypes.node_socket_exec import NodeSocketExec

__all__ = ['NodeSocketInput', 'NodeSocketOutput', 'NodeSocketWrapper']


# Define SocketT for the actual socket type (e.g., NodeSocketFloat)
# Define ValueT for the data type the socket holds (e.g., float)
SocketT = TypeVar('SocketT', bound=NodeSocket|NodeSocketExec)
ValueT = TypeVar('ValueT') # We won't bind this directly here

# Option to completely remove debug prints
DEBUG = False  # Set to True for debugging


class NodeSocketWrapper(Generic[SocketT]): # Make wrapper generic over SocketT
    def __init__(self, socket_type: Type[SocketT], io: str, label: str = ''):
        self.socket_type: Type[SocketT] = socket_type # Add type hint
        self.io = io
        self._name = ""
        self.socket_name = ""
        self.label = label
        # Don't store socket as instance attribute since it's node-specific

    def __set_name__(self, owner, name):
        """Called when the descriptor is assigned to a class attribute"""
        if DEBUG:
            print("NodeSocketWrapper.__set_name__()", owner, name)
        self.name = name

    # __get__ should return the actual socket instance, typed correctly.
    @overload
    def __get__(self, obj: None, objtype: Any) -> SocketT: ...
    @overload
    def __get__(self, obj: object, objtype: Any) -> SocketT: ...

    def __get__(self, obj, objtype=None) -> SocketT:
        """Get the descriptor itself when accessed from the class (approximated as SocketT),
           or the actual socket instance when accessed from an object instance.
        """
        if obj is None:  # Class access
            return cast(SocketT, self)

        # Instance access: Ensure socket exists and return it (already returns SocketT via cast)
        socket = self._ensure_socket_exists(obj)
        assert socket is not None, f"Socket not found for NodeSocketWrapper with name '{self.name}'"
        return cast(SocketT, socket)
    
    # __set__ is usually not needed when __get__ returns the socket instance
    # because you'd set the value directly on the socket: `self.MySocket.value = 5.0`
    # If you want to enable `self.MySocket = 5.0`, you'd need __set__.

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        if self.is_input or self.is_multi_input: # Check multi_input as well
            self.socket_name = f"in_{value}"
        else:
            self.socket_name = f"out_{value}"

    @property
    def is_input(self) -> bool:
        return self.io == 'INPUT'

    @property
    def is_multi_input(self) -> bool:
        return self.io == 'MULTI_INPUT'

    @property
    def is_output(self) -> bool:
        return self.io == 'OUTPUT'

    @property
    def bl_idname(self) -> str:
        # get_idname might not exist directly on Type[NodeSocket]
        # It's usually on the instance or class itself. Assuming it's a classmethod.
        if hasattr(self.socket_type, 'get_idname'):
            return self.socket_type.get_idname() # type: ignore
        # Fallback or error handling if get_idname is not available
        # Maybe use __name__? Requires careful handling of registration names.
        return self.socket_type.__name__ # Fallback, might not be the bl_idname

    # Changed return hint to Any temporarily, as bpy methods return bpy_prop_collection
    # which doesn't directly map to SocketT without casting later in __get__
    def _ensure_socket_exists(self, node: bpy_types.Node) -> Any | None:
        """Ensure the socket exists, creating it if necessary. Returns the bpy socket object.
           Casting to the specific SocketT happens in __get__.
        """
        target_collection = node.inputs if self.is_input or self.is_multi_input else node.outputs
        socket = target_collection.get(self.socket_name)
        if socket is None:
            # Use the bl_idname obtained earlier
            socket_idname = self.bl_idname
            socket = target_collection.new(socket_idname, self.label or self.name, identifier=self.socket_name)
            socket.init(node)
            if self.is_multi_input:
                # Assuming bpy has `use_multi_input` attribute on socket creation or afterwards
                # This might need adjustment based on Blender API version
                # socket.use_multi_input = True # Example, API might differ
                # Or pass it in .new() if supported like in the previous version snippet:
                # socket = node.inputs.new(..., use_multi_input=True)
                # Re-check Blender API for socket creation with multi_input
                pass # Placeholder - need to verify multi-input setting
            if DEBUG:
                print(f"NodeSocketWrapper._ensure_socket_exists. Node: {node.name} - Socket: {self.socket_name} - Type: {socket_idname}")
        return socket

    # copy method might not be needed or might need adjustment
    # def copy(self) -> 'NodeSocketWrapper':
    #     """Copy the socket wrapper. """
    #     return NodeSocketWrapper(self.socket_type, self.io, self.label)

# Factory functions return the descriptor instance, correctly typed.
def NodeSocketInput(socket_type: Type[SocketT], multi: bool = False) -> SocketT:
    """
    Create an input socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., NodeSocketFloat)
        multi: Whether this is a multi-input socket
        
    Returns:
        The actual socket instance (typed as SocketT) when accessed on a node instance.
    """
    # Return type hint SocketT tells the type checker what __get__ will return on an instance.
    return NodeSocketWrapper[SocketT](socket_type, 'INPUT' if not multi else 'MULTI_INPUT') # type: ignore

def NodeSocketOutput(socket_type: Type[SocketT]) -> SocketT:
    """
    Create an output socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., NodeSocketFloat)
        
    Returns:
        The actual socket instance (typed as SocketT) when accessed on a node instance.
    """
    # Return type hint SocketT tells the type checker what __get__ will return on an instance.
    return NodeSocketWrapper[SocketT](socket_type, 'OUTPUT') # type: ignore
