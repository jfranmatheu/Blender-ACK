import typing
import uuid
from typing import Any, TypeVar, Generic, Optional, cast, Union, Type, Dict, Set, ClassVar, Tuple, Callable, List

from bpy import types as bpy_types

from ...core.base_type import BaseType
from ...data.props import PropertyTypes as Prop
from .node_socket import _get_generic_type


__all__ = ['NodeSocketExec']


T = TypeVar('T')


class NodeSocketExec(BaseType, bpy_types.NodeSocket, Generic[T]):
    label: str
    color: tuple[float, float, float, float] = (.5, .5, .5, 1.0)

    uid: Prop.STRING(default='', options={'HIDDEN'})

    @property
    def is_input(self) -> bool:
        """ Checks if the socket is an input socket. """
        return not self.is_output

    @property
    def value_type(self) -> Type[T] | None:
        """ Gets the type hint of the socket value (e.g., None for ElementSocket). """
        return _get_generic_type(self)
    
    def init(self, node: bpy_types.Node):
        """ Called when the socket is created for the first time. """
        self.uid = str(uuid.uuid4())

    def get_links(self) -> List[bpy_types.NodeLink]:
        """ Gets the links connected to this socket. """
        return list(self.links)
    
    def get_connected_nodes(self) -> List[bpy_types.Node]:
        """ Gets the list of nodes connected TO this socket (if input)
            or FROM this socket (if output).
            Primarily useful for input sockets to find their source nodes.
        """
        if self.is_input:
            return [link.from_node for link in self.links if link.from_node]
        else: # is_output
            return [link.to_node for link in self.links if link.to_node]

    def draw_color(self, context: bpy_types.Context, node: bpy_types.Node) -> tuple[float, float, float, float]:
        """ Draws the color of the socket. """
        # print(node, self, self.name, self.property_name, self.property, node.tree_prop_idname)
        return self.color

    def draw(self, context: bpy_types.Context, layout: bpy_types.UILayout, node: bpy_types.Node, text: str):
        """ Draws the socket layout. """
        layout.label(text=self.name)  # no prop since it's custom data or runtime data.
