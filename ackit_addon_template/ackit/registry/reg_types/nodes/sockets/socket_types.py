from ..node_socket import NodeSocket
from ....props.property import PropertyTypes



class NodeSocketFloat(NodeSocket):
    default_value: PropertyTypes.FLOAT(default=0.0)

class NodeSocketFloatVector3(NodeSocket):
    default_value: PropertyTypes.VECTOR_3()

class NodeSocketFloatVector2(NodeSocket):
    default_value: PropertyTypes.VECTOR_2()

class NodeSocketInt(NodeSocket):
    default_value: PropertyTypes.INT()

class NodeSocketIntVector3(NodeSocket):
    default_value: PropertyTypes.IVECTOR_3()

class NodeSocketIntVector2(NodeSocket):
    default_value: PropertyTypes.IVECTOR_2()
    
class NodeSocketBool(NodeSocket):
    default_value: PropertyTypes.BOOL()

class NodeSocketString(NodeSocket):
    default_value: PropertyTypes.STRING()

class NodeSocketColor(NodeSocket):
    default_value: PropertyTypes.COLOR_RGB('Color')
