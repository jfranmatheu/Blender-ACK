from bpy import types as bpy_types

# Updated relative imports
from ...core.base_type import BaseType # Assuming BaseType moves to core or similar


class PropertyGroup(BaseType, bpy_types.PropertyGroup):
    pass