from enum import Enum
from math import pi
from typing import Any, Callable, Type, TypeVar, Union, Generic

from bpy.props import *
from bpy import types as btypes
from mathutils import Color, Vector, Matrix

# Updated relative imports - adjust paths as necessary
from ..ne.btypes import Node, NodeSocket # From ne/btypes/node.py and ne/btypes/node_socket.py
from ..utils.callback import CallbackList # Check if utils/callback.py exists


__all__ = [
    'PropertyTypes',
]


IdentityMatrix_2 = Matrix.Identity(2)
IdentityMatrix_3 = Matrix.Identity(3)
IdentityMatrix_4 = Matrix.Identity(4)

class PropertyTypes:
    ''' Utility to fast create different property types, some based on presets.
        Use it for PropertyGroup properties or to register properties in bpy.types. '''

    FLOAT = FloatProperty
    INT = IntProperty
    BOOL = BoolProperty
    FLOAT_VECTOR = FloatVectorProperty
    INT_VECTOR = IntVectorProperty
    BOOL_VECTOR = BoolVectorProperty
    ENUM = EnumProperty
    STRING = StringProperty
    POINTER_CUSTOM = PointerProperty

    ANGLE_DEGREE = lambda name, default = 0, min = -pi, max = pi, **kwargs: FloatProperty(name=name, default=default, min=min, max=max, subtype='ANGLE', unit='ROTATION', **kwargs)
    FACTOR = lambda name, default = 0, **kwargs: FloatProperty(name=name, default=default, min=0, max=1, **kwargs)

    IVECTOR_2 = lambda default = (0, 0), **kwargs: IntVectorProperty(default=default, size=2, **kwargs)
    IVECTOR_3 = lambda default = (0, 0, 0), **kwargs: IntVectorProperty(default=default, size=3, **kwargs)
    IVECTOR_XY = lambda default = (0, 0), **kwargs: IntVectorProperty(default=default, size=2, subtype='XYZ', **kwargs)
    IVECTOR_XYZ = lambda default = (0, 0, 0), **kwargs: IntVectorProperty(default=default, size=3, subtype='XYZ', **kwargs)
    IVECTOR_N = lambda default, **kwargs: IntVectorProperty(default=default, size=len(default), **kwargs)
    VECTOR_2 = lambda default = (0, 0), **kwargs: FloatVectorProperty(default=default, size=2, **kwargs)
    VECTOR_3 = lambda default = (0, 0, 0), **kwargs: FloatVectorProperty(default=default, size=3, **kwargs)
    VECTOR_XY = lambda default = (0, 0), **kwargs: FloatVectorProperty(default=default, size=2, subtype='XYZ', **kwargs)
    VECTOR_XYZ = lambda default = (0, 0, 0), **kwargs: FloatVectorProperty(default=default, size=3, subtype='XYZ', **kwargs)
    VECTOR_AXISANGLE = lambda default = (0, 0, 0), **kwargs: FloatVectorProperty(default=default, size=3, subtype='AXISANGLE', **kwargs)
    VECTOR_N = lambda default, **kwargs: FloatVectorProperty(default=default, size=len(default), **kwargs)

    COLOR_RGB = lambda name, default_color = (0.0, 0.0, 0.0), **kwargs: FloatVectorProperty(name=name, default=default_color, min=0.0, max=1.0, size=3, subtype='COLOR', **kwargs)
    COLOR_RGBA = lambda name, default_color = (0.0, 0.0, 0.0, 1.0), **kwargs: FloatVectorProperty(name=name, default=default_color, min=0.0, max=1.0, size=4, subtype='COLOR', **kwargs)

    MATRIX_2 = lambda name, **kwargs: FloatVectorProperty(name=name, default=IdentityMatrix_2, size=(2, 2), **kwargs)
    MATRIX_3 = lambda name, **kwargs: FloatVectorProperty(name=name, default=IdentityMatrix_3, size=(3, 3), **kwargs)
    MATRIX_4 = lambda name, **kwargs: FloatVectorProperty(name=name, default=IdentityMatrix_4, size=(4, 4), **kwargs)
    MATRIX_N = lambda name, default, **kwargs: FloatVectorProperty(name=name, default=default, size=(len(default), len(default[0])), **kwargs)

    DIRPATH = lambda **kwargs: StringProperty(subtype='DIR_PATH', **kwargs)
    FILEPATH = lambda **kwargs: StringProperty(subtype='FILE_PATH', **kwargs)

    COLLECTION = lambda type, **kwargs: CollectionProperty(type=type, **kwargs)

    class POINTER(Enum):
        OBJECT = btypes.Object
        MESH = btypes.Mesh
        CAMERA = btypes.Camera
        LIGHT = btypes.Light
        ARMATURE = btypes.Armature
        NODE_TREE = btypes.NodeTree
        NODE_GROUP = btypes.NodeGroup
        BRUSH = btypes.Brush
        IMAGE = btypes.Image
        TEXTURE = btypes.Texture

        @staticmethod
        def CUSTOM(name: str, type, **kwargs) -> PointerProperty:
            return PointerProperty(name=name, type=type, **kwargs)

        def __call__(self, name: str = '', **kwargs: dict) -> PointerProperty:
            return PointerProperty(type=self.value, name=name, **kwargs)
