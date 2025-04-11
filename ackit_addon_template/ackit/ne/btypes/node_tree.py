from typing import Set, Dict

from mathutils import Color, Vector
from bpy import types as bpy_types

from ...core.base_type import BaseType
from ...globals import GLOBALS


__all__ = ['NodeTree']


class NodeTree(BaseType, bpy_types.NodeTree):
    bl_idname: str = f"{GLOBALS.ADDON_MODULE_SHORT.upper()}_TREETYPE"
    bl_label: str
    bl_description: str
    bl_icon: str = 'DOT'

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        """Check visibility in the editor"""
        return True

    '''def update(self) -> None:
        """ Update on editor changes. """
        super().update()'''
