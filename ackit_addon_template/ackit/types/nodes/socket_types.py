from typing import TypeVar, Any, TYPE_CHECKING, Tuple
from enum import Enum

from bpy.types import Context, Node, UILayout, Object, Material, Mesh, Texture, Collection, Scene, World, Image, Armature, Action, Text
from mathutils import Color, Vector, Matrix

from ...registry.reg_types.nodes.node_socket import NodeSocket
from ...registry.props.typed import WrappedTypedPropertyTypes as Prop


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
    'NodeSocketObject',
    'NodeSocketMaterial',
    'NodeSocketMesh',
    'NodeSocketTexture',
    'NodeSocketCollection',
    'NodeSocketScene',
    'NodeSocketWorld',
    'NodeSocketImage',
    'NodeSocketArmature',
    'NodeSocketAction',
    'NodeSocketText'
]


class SocketColor(Enum):
    VALUE = (0.5, 0.5, 0.5, 1.0)  # Grey (Float)
    INTEGER = (0.0, 0.62, 0.0, 1.0) # Green
    VECTOR = (0.35, 0.35, 1.0, 1.0) # Blue
    BOOLEAN = (1.0, 0.4, 0.4, 1.0)   # Pink/Red
    STRING = (0.2, 0.7, 0.7, 1.0)   # Cyan
    COLOR = (0.78, 0.78, 0.16, 1.0) # Yellow
    DATA = (0.8, 0.5, 0.2, 1.0)   # Orange (Object, Material, etc.)
    MATRIX = (0.35, 0.35, 1.0, 1.0) # Blue (same as Vector)


class NodeSocketFloat(NodeSocket):
    label = 'Value'
    property = Prop.Float(name="Value", default=0.0)
    value: float
    color = SocketColor.VALUE.value

class NodeSocketFloatVector3(NodeSocket):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=float)
    value: Tuple[float, float, float]
    color = SocketColor.VECTOR.value

class NodeSocketFloatVector2(NodeSocket):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=float)
    value: Tuple[float, float]
    color = SocketColor.VECTOR.value

class NodeSocketInt(NodeSocket):
    label = 'Value'
    property = Prop.Int(name="Value", default=0)
    value: int
    color = SocketColor.INTEGER.value

class NodeSocketIntVector3(NodeSocket):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=int)
    value: Tuple[int, int, int]
    color = SocketColor.VECTOR.value

class NodeSocketIntVector2(NodeSocket):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=int)
    value: Tuple[int, int]
    color = SocketColor.VECTOR.value
    
class NodeSocketBool(NodeSocket):
    label = 'State'
    property = Prop.Bool(name="State", default=False)
    value: bool
    color = SocketColor.BOOLEAN.value

class NodeSocketString(NodeSocket):
    label = 'Text'
    property = Prop.String(name="Text", default="")
    value: str
    color = SocketColor.STRING.value

class NodeSocketDirPath(NodeSocket):
    label = 'Directory Path'
    property = Prop.DirPath(name="Directory Path")
    value: str
    color = SocketColor.STRING.value

class NodeSocketFilePath(NodeSocket):
    label = 'File Path'
    property = Prop.FilePath(name="File Path")
    value: str
    color = SocketColor.STRING.value

class NodeSocketFileName(NodeSocket):
    label = 'File Name'
    property = Prop.FileName(name="File Name")
    value: str
    color = SocketColor.STRING.value


class NodeSocketRGB(NodeSocket):
    label = 'RGB'
    property = Prop.Color(name="RGB", use_alpha=False)
    value: Tuple[float, float, float]
    color = SocketColor.COLOR.value

class NodeSocketRGBA(NodeSocket):
    label = 'RGBA'
    property = Prop.Color(name="RGBA", use_alpha=True)
    value: Tuple[float, float, float, float]
    color = SocketColor.COLOR.value

class NodeSocketAngle(NodeSocket):
    label = 'Angle'
    property = Prop.Angle(name="Angle", default=0.0)
    value: float
    color = SocketColor.VALUE.value

class NodeSocketFactor(NodeSocket):
    label = 'Factor'
    property = Prop.Factor(name="Factor", default=0.5)
    value: float
    color = SocketColor.VALUE.value

class NodeSocketMatrix3x3(NodeSocket):
    label = 'Matrix 3x3'
    property = Prop.Matrix3x3(name="Matrix 3x3")
    value: Matrix
    color = SocketColor.MATRIX.value

class NodeSocketMatrix4x4(NodeSocket):
    label = 'Matrix 4x4'
    property = Prop.Matrix4x4(name="Matrix 4x4")
    value: Matrix
    color = SocketColor.MATRIX.value

# Data Sockets
class NodeSocketObject(NodeSocket):
    label = 'Object'
    property = Prop.Data.Object(name="Object")
    value: Object
    color = SocketColor.DATA.value

class NodeSocketMaterial(NodeSocket):
    label = 'Material'
    property = Prop.Data.Material(name="Material")
    value: Material
    color = SocketColor.DATA.value

class NodeSocketMesh(NodeSocket):
    label = 'Mesh'
    property = Prop.Data.Mesh(name="Mesh")
    value: Mesh
    color = SocketColor.DATA.value

class NodeSocketTexture(NodeSocket):
    label = 'Texture'
    property = Prop.Data.Texture(name="Texture")
    value: Texture
    color = SocketColor.DATA.value

class NodeSocketCollection(NodeSocket):
    label = 'Collection'
    property = Prop.Data.Collection(name="Collection")
    value: Collection
    color = SocketColor.DATA.value

class NodeSocketScene(NodeSocket):
    label = 'Scene'
    property = Prop.Data.Scene(name="Scene")
    value: Scene
    color = SocketColor.DATA.value

class NodeSocketWorld(NodeSocket):
    label = 'World'
    property = Prop.Data.World(name="World")
    value: World
    color = SocketColor.DATA.value

class NodeSocketImage(NodeSocket):
    label = 'Image'
    property = Prop.Data.Image(name="Image")
    value: Image
    color = SocketColor.DATA.value

class NodeSocketArmature(NodeSocket):
    label = 'Armature'
    property = Prop.Data.Armature(name="Armature")
    value: Armature
    color = SocketColor.DATA.value

class NodeSocketAction(NodeSocket):
    label = 'Action'
    property = Prop.Data.Action(name="Action")
    value: Action
    color = SocketColor.DATA.value

class NodeSocketText(NodeSocket):
    label = 'Text'
    property = Prop.Data.Text(name="Text")
    value: Text
    color = SocketColor.DATA.value
