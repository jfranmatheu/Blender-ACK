from enum import Enum, auto
from typing import TypeVar, Generic, Union, Optional, Type, Any

from bpy import types as bpy_types

from ..node_socket import NodeSocket


__all__ = ['NodeSocketInput', 'NodeSocketOutput', 'NodeSocketWrapper', 'NodeSocketWrapperInstance']


T = TypeVar('T')  # Type variable for the socket value type


class NodeSocketWrapper(Generic[T]):
    def __init__(self, socket_type: Type[NodeSocket], io: str):
        self.socket_type = socket_type
        self.io = io
        self.name = ""

    def __set_name__(self, owner, name):
        """This is called when the descriptor is assigned to a class attribute"""
        print(f"Info: NodeSocketWrapper.__set_name__: {owner} - {name}, {self.socket_type}")
        self.name = name

    def create_instance(self, node: bpy_types.Node | None = None) -> 'NodeSocketWrapperInstance':
        print(f"Info: NodeSocketWrapper.create_instance: {self.name}, {self.socket_type}")
        wrapper_instance = NodeSocketWrapperInstance(self.socket_type, self.io)
        wrapper_instance.name = self.name
        if node is not None:
            wrapper_instance._ensure_socket_exists(node)
        return wrapper_instance


class NodeSocketWrapperInstance(Generic[T]):
    def __init__(self, socket_type: Type[NodeSocket], io: str):
        self.socket_type = socket_type
        self.io = io
        self.socket = None
        self._name = ""
        self.socket_name = ""

    @property
    def name(self) -> str:
        return self._name
    
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

    def _ensure_socket_exists(self, node: bpy_types.Node):
        """Ensure the socket exists, creating it if necessary"""
        if self.is_input:
            self.socket = node.inputs.get(self.socket_name)
            if self.socket is None:
                self.socket = node.inputs.new(self.socket_type.get_idname(), self.socket_name, use_multi_input=self.is_multi_input)
                print(f"NodeSocketWrapper._ensure_socket_exists. Node: {node.name} - InputSocket: {self.socket_name} - Type: {self.socket_type.get_idname()}")
        else:
            self.socket = node.outputs.get(self.socket_name)
            if self.socket is None:
                self.socket = node.outputs.new(self.socket_type.get_idname(), self.socket_name)
                print(f"NodeSocketWrapper._ensure_socket_exists. Node: {node.name} - OutputSocket: {self.socket_name} - Type: {self.socket_type.get_idname()}")
        return self.socket

    # Implement descriptor protocol
    def __get__(self, instance, owner) -> Union[T, 'NodeSocketWrapper[T]']:
        print(f"NodeSocketWrapper.__get__: {instance} - for socket type '{self.socket_type.__name__ if self.socket_type else 'None'}', with name: '{self.socket_name}'")
        if instance is None:
            return self
 
        # Ensure socket exists
        socket = self._ensure_socket_exists(instance)
        if socket is None:
            return None  # type: ignore

        return self  # type: ignore
        # Return the socket instead of self
        # return socket.default_value  # type: ignore

    def __set__(self, instance, value: T) -> None:
        print(f"NodeSocketWrapper.__set__: {instance} - for socket type '{self.socket_type.__name__ if self.socket_type else 'None'}', with name: '{self.socket_name}'")
        # Ensure socket exists
        socket = self._ensure_socket_exists(instance)
        if socket is not None:
            socket.default_value = value

    def __delete__(self, instance) -> None:
        print(f"NodeSocketWrapper.__delete__: {instance} - for socket type '{self.socket_type.__name__ if self.socket_type else 'None'}', with name: '{self.socket_name}'")

    def copy(self) -> 'NodeSocketWrapper':
        """Copy the socket wrapper. """
        return NodeSocketWrapper(self.socket_type, self.io)


def NodeSocketInput(socket_type: Type[NodeSocket], multi: bool = False) -> NodeSocketWrapperInstance:
    """
    Create an input socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., NodeSocketFloat)
        multi: Whether this is a multi-input socket
        
    Returns:
        A NodeSocketWrapper descriptor for the input socket
    """
    return NodeSocketWrapper(socket_type, 'INPUT' if not multi else 'MULTI_INPUT')

def NodeSocketOutput(socket_type: Type[NodeSocket]) -> NodeSocketWrapperInstance:
    """
    Create an output socket annotation.
    
    Args:
        socket_type: The type of node socket (e.g., NodeSocketFloat)
        
    Returns:
        A NodeSocketWrapper descriptor for the output socket
    """
    return NodeSocketWrapper(socket_type, 'OUTPUT')
