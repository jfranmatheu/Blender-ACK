from bpy import types as bpy_types

from ..base_type import BaseType


class PropertyGroup(BaseType):
    _bpy_type = bpy_types.PropertyGroup
