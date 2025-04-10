from bpy.types import Context, Node, UILayout
from mathutils import Color, Vector, Matrix
from typing import TypeVar, Any, TYPE_CHECKING, Tuple

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
    'NodeSocketRGB',
    'NodeSocketRGBA',
    'NodeSocketAngle',
    'NodeSocketFactor',
    'NodeSocketMatrix3x3',
    'NodeSocketMatrix4x4',
]


class NodeSocketFloat(NodeSocket):
    label = 'Value'
    property = Prop.Float(name="Value", default=0.0)
    value: float

class NodeSocketFloatVector3(NodeSocket):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=float)
    value: Tuple[float, float, float]

class NodeSocketFloatVector2(NodeSocket):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=float)
    value: Tuple[float, float]

class NodeSocketInt(NodeSocket):
    label = 'Value'
    property = Prop.Int(name="Value", default=0)
    value: int

class NodeSocketIntVector3(NodeSocket):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=int)
    value: Tuple[int, int, int]

class NodeSocketIntVector2(NodeSocket):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=int)
    value: Tuple[int, int]
    
class NodeSocketBool(NodeSocket):
    label = 'State'
    property = Prop.Bool(name="State", default=False)
    value: bool

class NodeSocketString(NodeSocket):
    label = 'Text'
    property = Prop.String(name="Text", default="")
    value: str

class NodeSocketRGB(NodeSocket):
    label = 'RGB'
    property = Prop.Color(name="RGB", use_alpha=False)
    value: Tuple[float, float, float]

class NodeSocketRGBA(NodeSocket):
    label = 'RGBA'
    property = Prop.Color(name="RGBA", use_alpha=True)
    value: Tuple[float, float, float, float]

class NodeSocketAngle(NodeSocket):
    label = 'Angle'
    property = Prop.Angle(name="Angle", default=0.0)
    value: float

class NodeSocketFactor(NodeSocket):
    label = 'Factor'
    property = Prop.Factor(name="Factor", default=0.5)
    value: float

class NodeSocketMatrix3x3(NodeSocket):
    label = 'Matrix 3x3'
    property = Prop.Matrix3x3(name="Matrix 3x3")
    value: Matrix

class NodeSocketMatrix4x4(NodeSocket):
    label = 'Matrix 4x4'
    property = Prop.Matrix4x4(name="Matrix 4x4")
    value: Matrix
