from ....ackit import ACK


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="Float", tooltip="Float input")
class FloatInput(ACK.NE.Node):
    # Outputs.
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="FloatVector3", tooltip="Float Vector3 input")
class FloatVector3Input(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT_VECTOR3)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="FloatVector2", tooltip="Float Vector2 input")
class FloatVector2Input(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT_VECTOR2)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="Int", tooltip="Integer input")
class IntInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.INT)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="IntVector3", tooltip="Int Vector3 input")
class IntVector3Input(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.INT_VECTOR3)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="IntVector2", tooltip="Int Vector2 input")
class IntVector2Input(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.INT_VECTOR2)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="Bool", tooltip="Boolean input")
class BoolInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.BOOL)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="String", tooltip="String input")
class StringInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.STRING)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="Dir Path", tooltip="Directory Path input")
class DirPathInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.DIR_PATH)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="File Path", tooltip="File Path input")
class FilePathInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FILE_PATH)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="File Name", tooltip="File Name input")
class FileNameInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FILE_NAME)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="RGB", tooltip="RGB Color input")
class RGBInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.RGB)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="RGBA", tooltip="RGBA Color input")
class RGBAInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.RGBA)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="Angle", tooltip="Angle input")
class AngleInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.ANGLE)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="Factor", tooltip="Factor input")
class FactorInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FACTOR)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="Matrix3x3", tooltip="Matrix 3x3 input")
class Matrix3x3Input(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.MATRIX3X3)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="Matrix4x4", tooltip="Matrix 4x4 input")
class Matrix4x4Input(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.MATRIX4X4)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Object", tooltip="Object input")
class ObjectInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.OBJECT)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Material", tooltip="Material input")
class MaterialInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.MATERIAL)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Mesh", tooltip="Mesh input")
class MeshInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.MESH)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Texture", tooltip="Texture input")
class TextureInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.TEXTURE)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Collection", tooltip="Collection input")
class CollectionInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.COLLECTION)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Scene", tooltip="Scene input")
class SceneInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.SCENE)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="World", tooltip="World input")
class WorldInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.WORLD)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Image", tooltip="Image input")
class ImageInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.IMAGE)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Armature", tooltip="Armature input")
class ArmatureInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.ARMATURE)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Action", tooltip="Action input")
class ActionInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.ACTION)


@ACK.NE.add_node_to_category("Inputs/Data")
@ACK.NE.add_node_metadata(label="Text", tooltip="Text input")
class TextInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.Data.TEXT)


# --- Custom-Property based Inputs ---


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="Custom Property", tooltip="Custom Property input")
class DictInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.PyData.DICT)


@ACK.NE.add_node_to_category("Inputs")
@ACK.NE.add_node_metadata(label="List", tooltip="List input")
class ListInput(ACK.NE.Node):
    value = ACK.NE.OutputSocket(ACK.NE.SocketTypes.PyData.LIST)
