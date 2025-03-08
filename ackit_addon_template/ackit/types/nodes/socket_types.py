from ...registry.reg_types.nodes.node_socket import NodeSocket
from ...registry.props.property import PropertyTypes


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
    default_value: PropertyTypes.FLOAT(0.0, name="Value")

class NodeSocketFloatVector3(NodeSocket):
    default_value: PropertyTypes.VECTOR_3((0.0, 0.0, 0.0), name="Vector")

class NodeSocketFloatVector2(NodeSocket):
    default_value: PropertyTypes.VECTOR_2((0.0, 0.0), name="Vector")

class NodeSocketInt(NodeSocket):
    default_value: PropertyTypes.INT(default=0, name="Value")

class NodeSocketIntVector3(NodeSocket):
    default_value: PropertyTypes.IVECTOR_3((0, 0, 0), name="Vector")

class NodeSocketIntVector2(NodeSocket):
    default_value: PropertyTypes.IVECTOR_2((0, 0), name="Vector")
    
class NodeSocketBool(NodeSocket):
    default_value: PropertyTypes.BOOL(default=False, name="State")

class NodeSocketString(NodeSocket):
    default_value: PropertyTypes.STRING(default="", name="Text")

class NodeSocketRGB(NodeSocket):
    default_value: PropertyTypes.COLOR_RGB('Color', (0.0, 0.0, 0.0))

class NodeSocketRGBA(NodeSocket):
    default_value: PropertyTypes.COLOR_RGBA('Color', (0.0, 0.0, 0.0, 0.0))
