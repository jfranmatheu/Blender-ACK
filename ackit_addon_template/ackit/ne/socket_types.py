from typing import TypeVar, Any, TYPE_CHECKING, Tuple, ClassVar, List
from enum import Enum

from bpy.types import (
    Object, Material, Mesh, Texture, Collection, Scene, World, Image, Armature,
    Action, Text, Light, Curve, Camera,
)
from mathutils import Color, Vector, Matrix

from .btypes.node_socket import NodeSocket
from ..data.props_typed import WrappedTypedPropertyTypes as Prop
from .socket_casting import SocketCast
from ..metadata import NodeSocket as add_socket_metadata


__all__ = [
    'NodeSocketFloat',
    'NodeSocketFloatVector3',
    'NodeSocketFloatVector2',
    'NodeSocketInt',
    'NodeSocketIntVector3',
    'NodeSocketIntVector2',
    'NodeSocketBool', 
    'NodeSocketString',
    'NodeSocketDirPath',
    'NodeSocketFilePath',
    'NodeSocketFileName',
    'NodeSocketRGB',
    'NodeSocketRGBA',
    'NodeSocketAngle',
    'NodeSocketFactor',
    'NodeSocketMatrix3x3',
    'NodeSocketMatrix4x4',
    'NodeSocketDataObject',
    'NodeSocketDataMaterial',
    'NodeSocketDataMesh',
    'NodeSocketDataTexture',
    'NodeSocketDataCollection',
    'NodeSocketDataScene',
    'NodeSocketDataWorld',
    'NodeSocketDataImage',
    'NodeSocketDataArmature',
    'NodeSocketDataAction',
    'NodeSocketDataText',
    'NodeSocketDataLight',
    'NodeSocketDataCurve',
    'NodeSocketDataCamera',
    'SocketTypes',
]


TYPE_MATRIX_3X3 = Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]
TYPE_MATRIX_4X4 = Tuple[Tuple[float, float, float, float], Tuple[float, float, float, float], Tuple[float, float, float, float], Tuple[float, float, float, float]]
TYPE_VECTOR_3 = Tuple[float, float, float]
TYPE_VECTOR_2 = Tuple[float, float]
TYPE_IVECTOR_3 = Tuple[int, int, int]
TYPE_IVECTOR_2 = Tuple[int, int]
TYPE_BVECTOR_2 = Tuple[bool, bool]
TYPE_BVECTOR_3 = Tuple[bool, bool, bool]
TYPE_RGB = Tuple[float, float, float]
TYPE_RGBA = Tuple[float, float, float, float]


# --- Socket Colors by value/property type ---

class SocketColor(Enum):
    VALUE = (0.5, 0.5, 0.5, 1.0)  # Grey (Float)
    INTEGER = (0.0, 0.62, 0.0, 1.0) # Green
    VECTOR = (0.35, 0.35, 1.0, 1.0) # Blue
    BOOLEAN = (1.0, 0.4, 0.4, 1.0)   # Pink/Red
    STRING = (0.2, 0.7, 0.7, 1.0)   # Cyan
    COLOR = (0.78, 0.78, 0.16, 1.0) # Yellow
    DATA = (0.8, 0.5, 0.2, 1.0)   # Orange (Object, Material, etc.)
    MATRIX = (0.35, 0.35, 1.0, 1.0) # Blue (same as Vector)
    PY_DATA = (0.8, 0.2, 0.8, 1.0) # Violet-red


# --- Socket definitions ---

@add_socket_metadata(label='Value', color=SocketColor.VALUE.value)
class NodeSocketFloat(NodeSocket[float]):
    property = Prop.Float(name="Value", default=0.0)
    cast_from_types = {
        int: float,
        bool: float,
    }

@add_socket_metadata(label='Vector3', color=SocketColor.VECTOR.value)
class NodeSocketFloatVector3(NodeSocket[TYPE_VECTOR_3]):
    property = Prop.Vector(name="Vector3", size=3, type=float)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    cast_from_socket = {
        'NodeSocketIntVector3': lambda v: (float(v[0]), float(v[1]), float(v[2])),
        'NodeSocketBoolVector3': lambda v: (float(v[0]), float(v[1]), float(v[2])),
    }

@add_socket_metadata(label='Vector2', color=SocketColor.VECTOR.value)
class NodeSocketFloatVector2(NodeSocket[TYPE_VECTOR_2]):
    property = Prop.Vector(name="Vector2", size=2, type=float)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    cast_from_socket = {
        'NodeSocketIntVector2': lambda v: (float(v[0]), float(v[1])),
        'NodeSocketBoolVector2': lambda v: (float(v[0]), float(v[1])),
    }

@add_socket_metadata(label='Integer', color=SocketColor.INTEGER.value)
class NodeSocketInt(NodeSocket[int]):
    property = Prop.Int(name="Value", default=0)
    cast_from_types = {
        float: int,
        bool: int,
    }

@add_socket_metadata(label='Vector3', color=SocketColor.VECTOR.value)
class NodeSocketIntVector3(NodeSocket[TYPE_IVECTOR_3]):
    property = Prop.Vector(name="Vector3", size=3, type=int)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    cast_from_socket = {
        'NodeSocketBoolVector3': lambda v: (int(v[0]), int(v[1]), int(v[2])),
        'NodeSocketFloatVector3': lambda v: (int(v[0]), int(v[1]), int(v[2])),
    }

@add_socket_metadata(label='Vector2', color=SocketColor.VECTOR.value)
class NodeSocketIntVector2(NodeSocket[TYPE_IVECTOR_2]):
    property = Prop.Vector(name="Vector2", size=2, type=int)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    cast_from_socket = {
        'NodeSocketBoolVector2': lambda v: (int(v[0]), int(v[1])),
        'NodeSocketFloatVector2': lambda v: (int(v[0]), int(v[1])),
    }

@add_socket_metadata(label='State', color=SocketColor.BOOLEAN.value)
class NodeSocketBool(NodeSocket[bool]):
    property = Prop.Bool(name="State", default=False)
    cast_from_types = {
        int: bool,
        float: bool,
    }

@add_socket_metadata(label='Vector2', color=SocketColor.VECTOR.value)
class NodeSocketBoolVector2(NodeSocket[TYPE_BVECTOR_2]):
    property = Prop.Vector(name="Vector2", size=2, type=bool)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    cast_from_socket = {
        'NodeSocketIntVector2': lambda v: (bool(v[0]), bool(v[1])),
        'NodeSocketFloatVector2': lambda v: (bool(v[0]), bool(v[1])),
    }

@add_socket_metadata(label='Vector3', color=SocketColor.VECTOR.value)
class NodeSocketBoolVector3(NodeSocket[TYPE_BVECTOR_3]):
    property = Prop.Vector(name="Vector3", size=3, type=bool)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    cast_from_socket = {
        'NodeSocketIntVector3': lambda v: (bool(v[0]), bool(v[1]), bool(v[2])),
        'NodeSocketFloatVector3': lambda v: (bool(v[0]), bool(v[1]), bool(v[2])),
    }

@add_socket_metadata(label='Text', color=SocketColor.STRING.value)
class NodeSocketString(NodeSocket[str]):
    property = Prop.String(name="Text", default="")
    cast_from_types = {
        int: str,
        float: str,
        bool: str,
    }

@add_socket_metadata(label='Directory Path', color=SocketColor.STRING.value)
class NodeSocketDirPath(NodeSocket[str]):
    property = Prop.DirPath(name="Directory Path")

@add_socket_metadata(label='File Path', color=SocketColor.STRING.value)
class NodeSocketFilePath(NodeSocket[str]):
    property = Prop.FilePath(name="File Path")

@add_socket_metadata(label='File Name', color=SocketColor.STRING.value)
class NodeSocketFileName(NodeSocket[str]):
    property = Prop.FileName(name="File Name")

@add_socket_metadata(label='Color (RGB)', color=SocketColor.COLOR.value)
class NodeSocketRGB(NodeSocket[Color]):
    property = Prop.Color(name="RGB", use_alpha=False)
    cast_from_types = {
        float: lambda val: (val, val, val),
    }
    cast_from_socket = {
        'NodeSocketRGBA': lambda color: (color.r, color.g, color.b),  # remove alpha channel
        'NodeSocketFloatVector3': lambda vec: (vec[0], vec[1], vec[2]),
    }

@add_socket_metadata(label='Color (RGBA)', color=SocketColor.COLOR.value)
class NodeSocketRGBA(NodeSocket[TYPE_RGBA]):
    property = Prop.Color(name="RGBA", use_alpha=True)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    cast_from_socket = {
        'NodeSocketRGB': lambda color: (color.r, color.g, color.b, 1.0),
        'NodeSocketFloatVector4': lambda vec: (vec[0], vec[1], vec[2], vec[3]),
    }

@add_socket_metadata(label='Angle', color=SocketColor.VALUE.value)
class NodeSocketAngle(NodeSocket[float]):
    property = Prop.Angle(name="Angle", default=0.0)

@add_socket_metadata(label='Factor', color=SocketColor.VALUE.value)
class NodeSocketFactor(NodeSocket[float]):
    property = Prop.Factor(name="Factor", default=0.5)
    cast_from_types = {
        int: float,
        bool: float,
    }

@add_socket_metadata(label='Matrix 3x3', color=SocketColor.MATRIX.value)
class NodeSocketMatrix3x3(NodeSocket[Matrix]):
    property = Prop.Matrix3x3(name="Matrix 3x3")
    cast_from_socket = {
        'NodeSocketMatrix4x4': lambda mat: mat.to_3x3(),
    }

@add_socket_metadata(label='Matrix 4x4', color=SocketColor.MATRIX.value)
class NodeSocketMatrix4x4(NodeSocket[Matrix]):
    property = Prop.Matrix4x4(name="Matrix 4x4")
    cast_from_socket = {
        'NodeSocketMatrix3x3': lambda mat: mat.to_4x4(),
    }

# Data Sockets
@add_socket_metadata(label='Object', color=SocketColor.DATA.value)
class NodeSocketDataObject(NodeSocket[Object]):
    property = Prop.Data.Object(name="Object")

@add_socket_metadata(label='Material', color=SocketColor.DATA.value)
class NodeSocketDataMaterial(NodeSocket[Material]):
    property = Prop.Data.Material(name="Material")

@add_socket_metadata(label='Mesh', color=SocketColor.DATA.value)
class NodeSocketDataMesh(NodeSocket[Mesh]):
    property = Prop.Data.Mesh(name="Mesh")
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'MESH' else None,
    }

@add_socket_metadata(label='Texture', color=SocketColor.DATA.value)
class NodeSocketDataTexture(NodeSocket[Texture]):
    property = Prop.Data.Texture(name="Texture")

@add_socket_metadata(label='Collection', color=SocketColor.DATA.value)
class NodeSocketDataCollection(NodeSocket[Collection]):
    property = Prop.Data.Collection(name="Collection")

@add_socket_metadata(label='Scene', color=SocketColor.DATA.value)
class NodeSocketDataScene(NodeSocket[Scene]):
    property = Prop.Data.Scene(name="Scene")

@add_socket_metadata(label='World', color=SocketColor.DATA.value)
class NodeSocketDataWorld(NodeSocket[World]):
    property = Prop.Data.World(name="World")

@add_socket_metadata(label='Image', color=SocketColor.DATA.value)
class NodeSocketDataImage(NodeSocket[Image]):
    property = Prop.Data.Image(name="Image")

@add_socket_metadata(label='Armature', color=SocketColor.DATA.value)
class NodeSocketDataArmature(NodeSocket[Armature]):
    property = Prop.Data.Armature(name="Armature")
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'ARMATURE' else None,
    }

@add_socket_metadata(label='Action', color=SocketColor.DATA.value)
class NodeSocketDataAction(NodeSocket[Action]):
    property = Prop.Data.Action(name="Action")
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.animation_data.action if obj.animation_data and obj.animation_data.action else None,
    }

@add_socket_metadata(label='Text', color=SocketColor.DATA.value)
class NodeSocketDataText(NodeSocket[Text]):
    property = Prop.Data.Text(name="Text")

@add_socket_metadata(label='Light', color=SocketColor.DATA.value)
class NodeSocketDataLight(NodeSocket[Light]):
    property = Prop.Data.Light(name="Light")
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'LIGHT' else None,
    }

@add_socket_metadata(label='Curve', color=SocketColor.DATA.value)
class NodeSocketDataCurve(NodeSocket[Curve]):
    property = Prop.Data.Curve(name="Curve")
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'CURVE' else None,
    }

@add_socket_metadata(label='Camera', color=SocketColor.DATA.value)
class NodeSocketDataCamera(NodeSocket[Camera]):
    property = Prop.Data.Camera(name="Camera")
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'CAMERA' else None,
    }



# --- Custom-Property based Sockets ---

@add_socket_metadata(label='PyDict', color=SocketColor.PY_DATA.value)
class NodeSocketPyDict(NodeSocket[dict]):
    use_custom_property = True
    property_cast = dict

@add_socket_metadata(label='PyList', color=SocketColor.PY_DATA.value)
class NodeSocketPyList(NodeSocket[list]):
    use_custom_property = True
    property_cast = list


# --- Socket Types Facade helper ---

class SocketTypes:
    # Basic types
    FLOAT = NodeSocketFloat
    INT = NodeSocketInt
    BOOL = NodeSocketBool
    STRING = NodeSocketString

    # Vector types
    FLOAT_VECTOR3 = NodeSocketFloatVector3
    FLOAT_VECTOR2 = NodeSocketFloatVector2
    INT_VECTOR3 = NodeSocketIntVector3
    INT_VECTOR2 = NodeSocketIntVector2
    BOOL_VECTOR2 = NodeSocketBoolVector2
    BOOL_VECTOR3 = NodeSocketBoolVector3

    # Path types
    DIR_PATH = NodeSocketDirPath
    FILE_PATH = NodeSocketFilePath
    FILE_NAME = NodeSocketFileName

    # Color types
    RGB = NodeSocketRGB
    RGBA = NodeSocketRGBA
    
    # Angle types
    ANGLE = NodeSocketAngle

    # Matrix types
    MATRIX3X3 = NodeSocketMatrix3x3
    MATRIX4X4 = NodeSocketMatrix4x4

    # Other types
    FACTOR = NodeSocketFactor

    # Data types
    class Data:
        OBJECT = NodeSocketDataObject
        MATERIAL = NodeSocketDataMaterial
        MESH = NodeSocketDataMesh
        TEXTURE = NodeSocketDataTexture
        COLLECTION = NodeSocketDataCollection
        SCENE = NodeSocketDataScene
        WORLD = NodeSocketDataWorld
        IMAGE = NodeSocketDataImage
        ARMATURE = NodeSocketDataArmature
        ACTION = NodeSocketDataAction
        TEXT = NodeSocketDataText
        LIGHT = NodeSocketDataLight
        CURVE = NodeSocketDataCurve
        CAMERA = NodeSocketDataCamera

    # Custom-Property based types
    class PyData:
        DICT = NodeSocketPyDict
        LIST = NodeSocketPyList
