from typing import TypeVar, Any, TYPE_CHECKING, Tuple
from enum import Enum

from bpy.types import Context, Node, UILayout, Object, Material, Mesh, Texture, Collection, Scene, World, Image, Armature, Action, Text
from mathutils import Color, Vector, Matrix

from .btypes.node_socket import NodeSocket
from ..data.props_typed import WrappedTypedPropertyTypes as Prop


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

class NodeSocketFloatVector3(NodeSocket[Tuple[float, float, float]]):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=float)
    color = SocketColor.VECTOR.value

class NodeSocketFloatVector2(NodeSocket[Tuple[float, float]]):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=float)
    color = SocketColor.VECTOR.value

class NodeSocketInt(NodeSocket[int]):
    label = 'Value'
    property = Prop.Int(name="Value", default=0)
    color = SocketColor.INTEGER.value

class NodeSocketIntVector3(NodeSocket[Tuple[int, int, int]]):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=int)
    color = SocketColor.VECTOR.value

class NodeSocketIntVector2(NodeSocket[Tuple[int, int]]):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=int)
    color = SocketColor.VECTOR.value
    
class NodeSocketBool(NodeSocket[bool]):
    label = 'State'
    property = Prop.Bool(name="State", default=False)
    color = SocketColor.BOOLEAN.value

class NodeSocketBoolVector2(NodeSocket[Tuple[bool, bool]]):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=bool)
    color = SocketColor.VECTOR.value

class NodeSocketBoolVector3(NodeSocket[Tuple[bool, bool, bool]]):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=bool)
    color = SocketColor.VECTOR.value

class NodeSocketString(NodeSocket[str]):
    label = 'Text'
    property = Prop.String(name="Text", default="")
    color = SocketColor.STRING.value

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

class NodeSocketRGB(NodeSocket[Tuple[float, float, float]]):
    label = 'Color (RGB)'
    property = Prop.Color(name="RGB", use_alpha=False)
    color = SocketColor.COLOR.value

class NodeSocketRGBA(NodeSocket[Tuple[float, float, float, float]]):
    label = 'Color (RGBA)'
    property = Prop.Color(name="RGBA", use_alpha=True)
    color = SocketColor.COLOR.value

class NodeSocketAngle(NodeSocket[float]):
    label = 'Angle'
    property = Prop.Angle(name="Angle", default=0.0)
    color = SocketColor.VALUE.value

class NodeSocketFactor(NodeSocket[float]):
    label = 'Factor'
    property = Prop.Factor(name="Factor", default=0.5)
    color = SocketColor.VALUE.value

class NodeSocketMatrix3x3(NodeSocket[Matrix]):
    label = 'Matrix 3x3'
    property = Prop.Matrix3x3(name="Matrix 3x3")
    color = SocketColor.MATRIX.value

class NodeSocketMatrix4x4(NodeSocket[Matrix]):
    label = 'Matrix 4x4'
    property = Prop.Matrix4x4(name="Matrix 4x4")
    color = SocketColor.MATRIX.value

# Data Sockets
class NodeSocketObject(NodeSocket[Object]):
    label = 'Object'
    property = Prop.Data.Object(name="Object")
    color = SocketColor.DATA.value

class NodeSocketMaterial(NodeSocket[Material]):
    label = 'Material'
    property = Prop.Data.Material(name="Material")
    color = SocketColor.DATA.value

class NodeSocketMesh(NodeSocket[Mesh]):
    label = 'Mesh'
    property = Prop.Data.Mesh(name="Mesh")
    color = SocketColor.DATA.value

class NodeSocketTexture(NodeSocket[Texture]):
    label = 'Texture'
    property = Prop.Data.Texture(name="Texture")
    color = SocketColor.DATA.value

class NodeSocketCollection(NodeSocket[Collection]):
    label = 'Collection'
    property = Prop.Data.Collection(name="Collection")
    color = SocketColor.DATA.value

class NodeSocketScene(NodeSocket[Scene]):
    label = 'Scene'
    property = Prop.Data.Scene(name="Scene")
    color = SocketColor.DATA.value

class NodeSocketWorld(NodeSocket[World]):
    label = 'World'
    property = Prop.Data.World(name="World")
    color = SocketColor.DATA.value

class NodeSocketImage(NodeSocket[Image]):
    label = 'Image'
    property = Prop.Data.Image(name="Image")
    color = SocketColor.DATA.value

class NodeSocketArmature(NodeSocket[Armature]):
    label = 'Armature'
    property = Prop.Data.Armature(name="Armature")
    color = SocketColor.DATA.value

class NodeSocketAction(NodeSocket[Action]):
    label = 'Action'
    property = Prop.Data.Action(name="Action")
    color = SocketColor.DATA.value

class NodeSocketText(NodeSocket[Text]):
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


class NodeSocketDataCamera(NodeSocket[Camera]):
    label = 'Camera'
    property = Prop.Data.Camera(name="Camera")
    color = SocketColor.DATA.value



# --- Custom-Property based Sockets ---

class NodeSocketPyDict(NodeSocket[dict]):
    label = 'PyDict'
    use_custom_property = True
    color = SocketColor.PY_DATA.value

class NodeSocketPyList(NodeSocket[list]):
    label = 'PyList'
    use_custom_property = True
    color = SocketColor.PY_DATA.value


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
