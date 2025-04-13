from typing import Any, TypeVar, Generic

from bpy import types as bpy_types

from ...core.base_type import BaseType
from ...data.props import PropertyTypes as Prop


__all__ = ['NodeSocket']


T = TypeVar('T')

class NodeSocket(BaseType, bpy_types.NodeSocket, Generic[T]):
    label: str
    color: tuple[float, float, float, float] = (.5, .5, .5, 1.0)
    property_name: str = 'property'
    use_custom_property: bool = False

    # Extended properties
    block_property_update: Prop.BOOL(default=False)

    @property
    def is_input(self):
        return not self.is_output

    @property
    def value(self) -> T:
        return self.get_value()

    @value.setter
    def value(self, value: T):
        self.set_value(value)

    def get_value(self) -> T:
        if self.is_input:
            if self.is_linked:
                # TODO: support multi-input sockets.
                from_socket: NodeSocket = self.links[0].from_socket
                return from_socket.get_value()
        if self.use_custom_property:
            if self.property_name in self:
                return self[self.property_name]
            return None
        return getattr(self, self.property_name)

    def set_value(self, value: T):
        if self.use_custom_property:
            self[self.property_name] = value
        else:
            setattr(self, self.property_name, value)

    def set_value_with_block_update(self, value):
        self.block_property_update = True
        self.set_value(value)
        self.block_property_update = False

    def on_property_update(self, context: bpy_types.Context):
        if not self.is_input:
            return
        print(f"NodeSocket.on_property_update: {self.property_name}")
        if self.block_property_update:
            return
        self.block_property_update = True
        self.node.process()
        self.block_property_update = False

    def get_links(self):
        return self.links if self.is_linked else []
        # return (*self.links, *self.portal_links) if self.use_portal_links and self.is_linked else self.links if not self.use_portal_links and self.is_linked else self.portal_links if self.use_portal_links else []

    def draw_color(self, context: bpy_types.Context, node: bpy_types.Node) -> tuple[float]:
        # print(node, self, self.name, self.property_name, self.property, node.tree_prop_idname)
        return self.color
    
    def draw(self, context: bpy_types.Context, layout: bpy_types.UILayout, node: bpy_types.Node, text: str):
        if self.is_input and not self.is_linked:
            layout.prop(self, self.property_name, text=self.name)
        else:
            layout.label(text=self.name)
