from typing import Set, Dict

from mathutils import Color, Vector
from bpy import types as bpy_types

from ..base_type import BaseType
from ....globals import GLOBALS


__all__ = ['NodeSocket']


class NodeSocket(BaseType):
    bl_idname: str
    bl_label: str
    bl_subtype_label: str
    
    # Attributes.
    description: str
    display_shape: str  # 'CIRCLE', 'SQUARE', 'DIAMOND', 'CIRCLE_FOT', 'SQUARE_DOT', 'DIAMOND_DOT'
    enabled: bool
    hide: bool
    hide_Value: bool
    identifier: str
    is_linked: bool
    is_multi_input: bool
    is_output: bool
    is_unavailable: bool
    label: str
    link_limit: int
    node: bpy_types.Node
    pin_gizmo: bool
    show_expanded: bool
    type: str
    links: bpy_types.NodeLinks


    @classmethod
    def tag_register(cls):
        return super().tag_register(bpy_types.NodeSocket, 'SOCKET')

    def draw(self, context: bpy_types.Context, layout: bpy_types.UILayout, node: bpy_types.Node, text: str) -> None:
        pass

    def draw_color(self, context: bpy_types.Context, node: bpy_types.Node) -> tuple[float, float, float, float]:
        pass
    
    @classmethod
    def draw_color_simple(cls) -> tuple[float, float, float, float]:
        pass
