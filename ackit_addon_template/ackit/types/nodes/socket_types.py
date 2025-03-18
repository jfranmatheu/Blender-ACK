from bpy.types import Context, Node, UILayout
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
]


class NodeSocketFloat(NodeSocket):
    label = 'Value'
    property = Prop.Float(name="Value", default=0.0)

class NodeSocketFloatVector3(NodeSocket):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=float)

class NodeSocketFloatVector2(NodeSocket):
    label = 'Vector2'
    property = Prop.Vector(name="Vector2", size=2, type=float)

class NodeSocketInt(NodeSocket):
    label = 'Value'
    property = Prop.Int(name="Value", default=0)
    value: int

class NodeSocketIntVector3(NodeSocket):
    label = 'Vector3'
    property = Prop.Vector(name="Vector3", size=3, type=int)

class NodeSocketIntVector2(NodeSocket):
    property = Prop.Vector(name="Vector2", size=2, type=int)
    
class NodeSocketBool(NodeSocket):
    property = Prop.Bool(name="State", default=False)

class NodeSocketString(NodeSocket):
    property = Prop.String(name="Text", default="")

class NodeSocketRGB(NodeSocket):
    property = Prop.Color(name="RGB", use_alpha=False)

class NodeSocketRGBA(NodeSocket):
    property = Prop.Color(name="RGBA", use_alpha=True)
