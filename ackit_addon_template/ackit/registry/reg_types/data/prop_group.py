from bpy import types as bpy_types

from ..base_type import BaseType


class PropertyGroup(BaseType, bpy_types.PropertyGroup):
    pass