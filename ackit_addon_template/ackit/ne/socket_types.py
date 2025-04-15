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

class NodeSocketFloat(NodeSocket[float]):
    label = 'Value'
    property = Prop.Float(name="Value", default=0.0)
    color = SocketColor.VALUE.value
    cast_from_types = {
        int: float,
        bool: float,
    }

class NodeSocketFloatVector3(NodeSocket[TYPE_VECTOR_3]):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=float)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    color = SocketColor.VECTOR.value
    cast_from_socket = {
        'NodeSocketIntVector3': lambda v: (float(v[0]), float(v[1]), float(v[2])),
        'NodeSocketBoolVector3': lambda v: (float(v[0]), float(v[1]), float(v[2])),
    }

class NodeSocketFloatVector2(NodeSocket[TYPE_VECTOR_2]):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=float)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    color = SocketColor.VECTOR.value
    cast_from_socket = {
        'NodeSocketIntVector2': lambda v: (float(v[0]), float(v[1])),
        'NodeSocketBoolVector2': lambda v: (float(v[0]), float(v[1])),
    }


class NodeSocketInt(NodeSocket[int]):
    label = 'Value'
    property = Prop.Int(name="Value", default=0)
    color = SocketColor.INTEGER.value
    cast_from_types = {
        float: int,
        bool: int,
    }

class NodeSocketIntVector3(NodeSocket[TYPE_IVECTOR_3]):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=int)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    color = SocketColor.VECTOR.value
    cast_from_socket = {
        'NodeSocketBoolVector3': lambda v: (int(v[0]), int(v[1]), int(v[2])),
        'NodeSocketFloatVector3': lambda v: (int(v[0]), int(v[1]), int(v[2])),
    }

class NodeSocketIntVector2(NodeSocket[TYPE_IVECTOR_2]):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=int)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    color = SocketColor.VECTOR.value
    cast_from_socket = {
        'NodeSocketBoolVector2': lambda v: (int(v[0]), int(v[1])),
        'NodeSocketFloatVector2': lambda v: (int(v[0]), int(v[1])),
    }

class NodeSocketBool(NodeSocket[bool]):
    label = 'State'
    property = Prop.Bool(name="State", default=False)
    color = SocketColor.BOOLEAN.value
    cast_from_types = {
        int: bool,
        float: bool,
    }

class NodeSocketBoolVector2(NodeSocket[TYPE_BVECTOR_2]):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=bool)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    color = SocketColor.VECTOR.value
    cast_from_socket = {
        'NodeSocketIntVector2': lambda v: (bool(v[0]), bool(v[1])),
        'NodeSocketFloatVector2': lambda v: (bool(v[0]), bool(v[1])),
    }

class NodeSocketBoolVector3(NodeSocket[TYPE_BVECTOR_3]):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=bool)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    color = SocketColor.VECTOR.value
    cast_from_socket = {
        'NodeSocketIntVector3': lambda v: (bool(v[0]), bool(v[1]), bool(v[2])),
        'NodeSocketFloatVector3': lambda v: (bool(v[0]), bool(v[1]), bool(v[2])),
    }

class NodeSocketString(NodeSocket[str]):
    label = 'Text'
    property = Prop.String(name="Text", default="")
    color = SocketColor.STRING.value
    cast_from_types = {
        int: str,
        float: str,
        bool: str,
    }

class NodeSocketDirPath(NodeSocket[str]):
    label = 'Directory Path'
    property = Prop.DirPath(name="Directory Path")
    color = SocketColor.STRING.value

class NodeSocketFilePath(NodeSocket[str]):
    label = 'File Path'
    property = Prop.FilePath(name="File Path")
    color = SocketColor.STRING.value

class NodeSocketFileName(NodeSocket[str]):
    label = 'File Name'
    property = Prop.FileName(name="File Name")
    color = SocketColor.STRING.value

class NodeSocketRGB(NodeSocket[Color]):
    label = 'Color (RGB)'
    property = Prop.Color(name="RGB", use_alpha=False)
    color = SocketColor.COLOR.value
    cast_from_types = {
        float: lambda val: (val, val, val),
    }
    cast_from_socket = {
        'NodeSocketRGBA': lambda color: (color.r, color.g, color.b),  # remove alpha channel
        'NodeSocketFloatVector3': lambda vec: (vec[0], vec[1], vec[2]),
    }

class NodeSocketRGBA(NodeSocket[TYPE_RGBA]):
    label = 'Color (RGBA)'
    property = Prop.Color(name="RGBA", use_alpha=True)
    property_cast = tuple  # Blender interprets the property as 'bpy_prop_array', so we need to cast it to a tuple.
    color = SocketColor.COLOR.value

class NodeSocketAngle(NodeSocket[float]):
    label = 'Angle'
    property = Prop.Angle(name="Angle", default=0.0)
    color = SocketColor.VALUE.value

class NodeSocketFactor(NodeSocket[float]):
    label = 'Factor'
    property = Prop.Factor(name="Factor", default=0.5)
    color = SocketColor.VALUE.value
    cast_from_types = {
        int: float,
        bool: float,
    }

class NodeSocketMatrix3x3(NodeSocket[Matrix]):
    label = 'Matrix 3x3'
    property = Prop.Matrix3x3(name="Matrix 3x3")
    color = SocketColor.MATRIX.value
    cast_from_socket = {
        'NodeSocketMatrix4x4': lambda mat: mat.to_3x3(),
    }

class NodeSocketMatrix4x4(NodeSocket[Matrix]):
    label = 'Matrix 4x4'
    property = Prop.Matrix4x4(name="Matrix 4x4")
    color = SocketColor.MATRIX.value
    cast_from_socket = {
        'NodeSocketMatrix3x3': lambda mat: mat.to_4x4(),
    }

# Data Sockets
class NodeSocketDataObject(NodeSocket[Object]):
    label = 'Object'
    property = Prop.Data.Object(name="Object")
    color = SocketColor.DATA.value

class NodeSocketDataMaterial(NodeSocket[Material]):
    label = 'Material'
    property = Prop.Data.Material(name="Material")
    color = SocketColor.DATA.value

class NodeSocketDataMesh(NodeSocket[Mesh]):
    label = 'Mesh'
    property = Prop.Data.Mesh(name="Mesh")
    color = SocketColor.DATA.value
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'MESH' else None,
    }

class NodeSocketDataTexture(NodeSocket[Texture]):
    label = 'Texture'
    property = Prop.Data.Texture(name="Texture")
    color = SocketColor.DATA.value

class NodeSocketDataCollection(NodeSocket[Collection]):
    label = 'Collection'
    property = Prop.Data.Collection(name="Collection")
    color = SocketColor.DATA.value

class NodeSocketDataScene(NodeSocket[Scene]):
    label = 'Scene'
    property = Prop.Data.Scene(name="Scene")
    color = SocketColor.DATA.value

class NodeSocketDataWorld(NodeSocket[World]):
    label = 'World'
    property = Prop.Data.World(name="World")
    color = SocketColor.DATA.value

class NodeSocketDataImage(NodeSocket[Image]):
    label = 'Image'
    property = Prop.Data.Image(name="Image")
    color = SocketColor.DATA.value

class NodeSocketDataArmature(NodeSocket[Armature]):
    label = 'Armature'
    property = Prop.Data.Armature(name="Armature")
    color = SocketColor.DATA.value
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'ARMATURE' else None,
    }

class NodeSocketDataAction(NodeSocket[Action]):
    label = 'Action'
    property = Prop.Data.Action(name="Action")
    color = SocketColor.DATA.value
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.animation_data.action if obj.animation_data and obj.animation_data.action else None,
    }

class NodeSocketDataText(NodeSocket[Text]):
    label = 'Text'
    property = Prop.Data.Text(name="Text")
    color = SocketColor.DATA.value

class NodeSocketDataLight(NodeSocket[Light]):
    label = 'Light'
    property = Prop.Data.Light(name="Light")
    color = SocketColor.DATA.value
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'LIGHT' else None,
    }

class NodeSocketDataCurve(NodeSocket[Curve]):
    label = 'Curve'
    property = Prop.Data.Curve(name="Curve")
    color = SocketColor.DATA.value
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'CURVE' else None,
    }

class NodeSocketDataCamera(NodeSocket[Camera]):
    label = 'Camera'
    property = Prop.Data.Camera(name="Camera")
    color = SocketColor.DATA.value
    cast_from_socket = {
        'NodeSocketObject': lambda obj: obj.data if obj.type == 'CAMERA' else None,
    }



# --- Custom-Property based Sockets ---

class NodeSocketPyDict(NodeSocket[dict]):
    label = 'PyDict'
    use_custom_property = True
    color = SocketColor.PY_DATA.value
    property_cast = dict

class NodeSocketPyList(NodeSocket[list]):
    label = 'PyList'
    use_custom_property = True
    color = SocketColor.PY_DATA.value
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
