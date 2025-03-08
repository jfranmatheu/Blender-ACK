from typing import Set, Dict

from mathutils import Color, Vector
from bpy import types as bpy_types

from ..base_type import BaseType
from ....globals import GLOBALS


__all__ = ['NodeSocket']


class NodeSocket(BaseType, bpy_types.NodeSocket):
    label: str
    color: tuple[float, float, float, float] = (.5, .5, .5, 1.0)
    property: callable
    property_name: str = 'default_value'
