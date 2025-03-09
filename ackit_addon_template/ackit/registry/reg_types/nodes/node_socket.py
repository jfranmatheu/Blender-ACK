from bpy import types as bpy_types

from ..base_type import BaseType
from ...props.property import PropertyTypes as Prop


__all__ = ['NodeSocket']


class NodeSocket(BaseType, bpy_types.NodeSocket):
    label: str
    color: tuple[float, float, float, float] = (.5, .5, .5, 1.0)
    property_name: str = 'default_value'

    # Extended properties
    block_property_update: Prop.BOOL(default=False)

    @property
    def is_input(self):
        return not self.is_output

    def get_value(self):
        return getattr(self, self.property_name)

    def set_value(self, value):
        setattr(self, self.property_name, value)

    def set_value_with_block_update(self, value):
        self.block_property_update = True
        self.set_value(value)
        self.block_property_update = False
    
    def on_property_update(self, context: bpy_types.Context):
        print(f"NodeSocket.on_property_update: {self.property_name}")
        if self.block_property_update:
            return
        self.node.process()

    def get_links(self):
        return self.links if self.is_linked else []
        # return (*self.links, *self.portal_links) if self.use_portal_links and self.is_linked else self.links if not self.use_portal_links and self.is_linked else self.portal_links if self.use_portal_links else []

    def draw_color(self, context: bpy_types.Context, node: bpy_types.Node) -> tuple[float]:
        # print(node, self, self.name, self.property_name, self.property, node.tree_prop_idname)
        return self.color
    
    def draw(self, context: bpy_types.Context, layout: bpy_types.UILayout, node: bpy_types.Node, text: str):
        if self.is_input:
            layout.prop(self, self.property_name, text=self.label)
        else:
            layout.label(text=self.label)
