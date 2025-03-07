from typing import Set, Dict

from mathutils import Color, Vector
from bpy import types as bpy_types

from ..base_type import BaseType
from ....globals import GLOBALS


__all__ = ['NodeTree']


class NodeTree(BaseType):
    _bpy_type = bpy_types.NodeTree

    bl_idname: str = f"{GLOBALS.ADDON_MODULE_SHORT.upper()}_TREETYPE"
    bl_label: str
    bl_description: str
    bl_icon: str = 'DOT'

    # Attributes.
    animation_data: bpy_types.AnimData
    color_tag: str
    default_group_node_width: int
    description: str
    grease_pencil: bpy_types.GreasePencil
    interface: bpy_types.NodeTreeInterface
    links: bpy_types.NodeLinks
    nodes: bpy_types.Nodes
    view_center: Vector

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        """Check visibility in the editor"""
        return True

    '''@classmethod
    def get_from_context(cls, context: bpy_types.Context) -> tuple[bpy_types.NodeTree, bpy_types.ID, bpy_types.ID]:
        """ Get the node tree from the context.
        Return (result_1, result_2, result_3):
        result_1, Active node tree from context, NodeTree
        result_2, ID data-block that owns the node tree, ID
        result_3, Original ID data-block selected from the context, ID
        """
        return super().get_from_context(context)

    @classmethod
    def valid_socket_type(cls, socket_idname: str) -> bool:
        """ Check if the socket type is valid. """
        return super().valid_socket_type(socket_idname)

    def contains_tree(self, subtree: bpy_types.NodeTree) -> bool:
        """ Check if the node tree contains another. Used to avoid creating recursive node groups. """
        return super().contains_tree(subtree)'''
    
    def update(self) -> None:
        """ Update on editor changes. """
        super().update()

    '''def interface_update(self, context: bpy_types.Context) -> None:
        """ Update the node group interface. """
        super().interface_update(context)
    
    def debug_lazy_function_graph(self) -> None:
        """ Debug the lazy function graph. """
        super().debug_lazy_function_graph()'''
