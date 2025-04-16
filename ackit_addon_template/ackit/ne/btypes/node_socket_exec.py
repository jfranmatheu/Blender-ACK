import typing
import uuid
from typing import Any, TypeVar, Generic, Optional, cast, Union, Type, Dict, Set, ClassVar, Tuple, Callable, List

from bpy import types as bpy_types

from ...core.base_type import BaseType
from ...data.props import PropertyTypes as Prop
from .node_socket import _get_generic_type


__all__ = ['NodeSocketExec']


T = TypeVar('T')


RUNTIME_DATA = {}


class NodeSocketExec(BaseType, bpy_types.NodeSocket, Generic[T]):
    label: str
    color: tuple[float, float, float, float] = (.5, .5, .5, 1.0)

    uid: Prop.STRING(default='', options={'HIDDEN'})

    @property
    def is_input(self) -> bool:
        """ Checks if the socket is an input socket. """
        return not self.is_output

    @property
    def value(self) -> T | List[T] | None:
        """ Gets the value from the connected output socket(s).
            For multi-input, returns a list of values.
            Returns None if not connected or if the connected socket has no value.
            NOTE: For structural connections (like ElementSocket), use get_connected_nodes() instead.
        """
        if self.is_input:
            if self.is_linked:
                if self.is_multi_input:
                    # Return list of values from connected sockets
                    vals = []
                    for link in self.links:
                        # Ensure the connected socket is also NodeSocketExec or compatible
                        if hasattr(link.from_socket, 'value'):
                            vals.append(link.from_socket.value)
                        else:
                            vals.append(None) # Or handle error/warning
                    return vals
                else:
                    # Return single value from the first link
                    if self.links and hasattr(self.links[0].from_socket, 'value'):
                         return self.links[0].from_socket.value
                    else:
                         return None # No links or incompatible socket
            else:
                return None # Not linked
        else: # Is Output
            global RUNTIME_DATA
            return RUNTIME_DATA.get(self.uid, None)

    @value.setter
    def value(self, value: T | None):
        """ Sets the **default** value of the socket. """
        self.set_value(value)

    def set_value(self, value: T | None):
        """ Sets the **default** value of the socket. """
        global RUNTIME_DATA
        RUNTIME_DATA[self.uid] = value

    @property
    def value_type(self) -> Type[T] | None:
        """ Gets the type of the socket value. """
        return _get_generic_type(self)
    
    def clear_value(self):
        """ Clears the **default** value of the socket. """
        global RUNTIME_DATA
        RUNTIME_DATA.pop(self.uid, None)

    def init(self, node: bpy_types.Node):
        """ Called when the socket is created for the first time. """
        self.uid = str(uuid.uuid4())

    def get_links(self):
        """ Gets the links of the socket. """
        return self.links
    
    def execute(self, *args, **kwargs) -> Dict[str, Any] | None:
        """Execute the node's logic.
        Receives execution context args/kwargs from the NodeTreeExec, if any.
        """
        raise NotImplementedError(f"Execute method not implemented in {self.__class__.__name__}")

    def draw_color(self, context: bpy_types.Context, node: bpy_types.Node) -> tuple[float, float, float, float]:
        """ Draws the color of the socket. """
        # print(node, self, self.name, self.property_name, self.property, node.tree_prop_idname)
        return self.color

    def draw(self, context: bpy_types.Context, layout: bpy_types.UILayout, node: bpy_types.Node, text: str):
        """ Draws the socket layout. """
        layout.label(text=self.name)  # no prop since it's custom data or runtime data.

    def get_connected_nodes(self) -> List[bpy_types.Node]:
        """Gets the list of nodes connected to this input socket."""
        if not self.is_input or not self.is_linked:
            return []
        return [link.from_node for link in self.links if link.from_node]
