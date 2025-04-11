from enum import Enum, auto
from typing import TypeVar, Generic, Union, Optional, Type, Any, cast, overload, Generic
import math

from bpy import types as bpy_types

# Updated relative imports
from .btypes.node_socket import NodeSocket


__all__ = ['NodeSocketInput', 'NodeSocketOutput', 'NodeSocketWrapper']


T = TypeVar('T')  # Type variable for the socket value type

# Option to completely remove debug prints
DEBUG = False  # Set to True for debugging


class NodeSocketWrapper(Generic[T]):
    def __init__(self, socket_type: Type[NodeSocket], io: str, label: str = ''):
        self.socket_type = socket_type
        self.io = io
        self._name = ""
        self.socket_name = ""
        self.label = label
        # Don't store socket as instance attribute since it's node-specific

    def __set_name__(self, owner, name):
        """Called when the descriptor is assigned to a class attribute"""
        print("NodeSocketWrapper.__set_name__()", owner, name)
        self.name = name

    '''def __get__(self, obj, objtype=None):
        """Get the value of the socket from the node instance"""
        print("NodeSocketWrapper.__get__()", obj, objtype, self.name)

        if obj is None:  # Class access instead of instance access
            return self
            
        # Ensure socket exists and is up-to-date
        socket = self._ensure_socket_exists(obj)
        
        # Return the socket value
        if socket is not None:
            if hasattr(socket, "get_value"):
                return socket.get_value()
            return socket.default_value
        return None

    def __set__(self, obj, value):
        """Set the value of the socket for the node instance"""
        print("NodeSocketWrapper.__set__()", obj, value, self.name)

        if obj is None:
            return

        # Ensure socket exists and is up-to-date
        socket = self._ensure_socket_exists(obj)
        
        # Set the socket value
        if socket is not None:
            if hasattr(socket, "set_value"):
                socket.set_value(value)
            else:
                socket.default_value = value'''

    def __get__(self, obj, objtype=None):
        """Get the wrapper itself"""
        if obj is None:  # Class access instead of instance access
            return self

        # Ensure socket exists
        socket = self._ensure_socket_exists(obj)
        assert socket is not None, f"Socket not found for NodeSocketWrapper with name '{self.name}'"
        return socket

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        if self.is_input:
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
        return self.socket_type.get_idname()

    def _ensure_socket_exists(self, node: bpy_types.Node, name: str | None = None):
        """Ensure the socket exists, creating it if necessary"""
        if self.is_input:
            socket = node.inputs.get(self.socket_name)
            if socket is None:
                socket = node.inputs.new(self.socket_type.get_idname(), self.label or self.name, identifier=self.socket_name, use_multi_input=self.is_multi_input)
                if DEBUG:
                    print(f"NodeSocketWrapper._ensure_socket_exists. Node: {node.name} - InputSocket: {self.socket_name} - Type: {self.socket_type.get_idname()}")
        else:
            socket = node.outputs.get(self.socket_name)
            if socket is None:
                socket = node.outputs.new(self.socket_type.get_idname(), self.label or self.name, identifier=self.socket_name)
                if DEBUG:
                    print(f"NodeSocketWrapper._ensure_socket_exists. Node: {node.name} - OutputSocket: {self.socket_name} - Type: {self.socket_type.get_idname()}")
        return socket

    def copy(self) -> 'NodeSocketWrapper':
        """Copy the socket wrapper. """
        return NodeSocketWrapper(self.socket_type, self.io)


def _NodeSocketInput(socket_type: Type[NodeSocket], multi: bool = False) -> NodeSocket:
    """
    Create an input socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., NodeSocketFloat)
        multi: Whether this is a multi-input socket
        
    Returns:
        A NodeSocketWrapper descriptor for the input socket
    """
    return NodeSocketWrapper[T](socket_type, 'INPUT' if not multi else 'MULTI_INPUT')

def _NodeSocketOutput(socket_type: Type[NodeSocket]) -> NodeSocket:
    """
    Create an output socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., NodeSocketFloat)
        
    Returns:
        A NodeSocketWrapper descriptor for the output socket
    """
    return NodeSocketWrapper[T](socket_type, 'OUTPUT')
