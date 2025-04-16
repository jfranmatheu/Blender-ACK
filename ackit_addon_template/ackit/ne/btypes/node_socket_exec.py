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
        """ Gets the **default** value of the socket.
            During execution, linked input values are retrieved by the NodeTreeExec.
        """
        if self.is_input:
            if self.is_linked:
                if self.is_multi_input:
                    return [link.from_socket.value for link in self.links]
                else:
                    return self.links[0].from_socket.value
            else:
                return None
        else:
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
