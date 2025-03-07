from bpy import types as bpy_types
import math

from ....ackit import ACK


@ACK.Flags.NODE_CATEGORY("Math")
class Add(ACK.Register.Types.Nodes.Node):
    bl_label = "Add"
    bl_description = "Add two numbers"

    a: ACK.Nodes.Socket.INPUT(ACK.Nodes.SocketTypes.FLOAT)
    b: ACK.Nodes.Socket.INPUT(ACK.Nodes.SocketTypes.FLOAT)
    result: ACK.Nodes.Socket.OUTPUT(ACK.Nodes.SocketTypes.FLOAT)

    '''def init(self, context: bpy_types.Context) -> None:
        self.inputs.new("NodeSocketFloat", "A")
        self.inputs.new("NodeSocketFloat", "B")
        self.outputs.new("NodeSocketFloat", "Result")'''

    def evaluate(self, inputs) -> None:
        result = round(inputs["A"] + inputs["B"], 6)
        self.outputs[0].default_value = result
        self.outputs[0].name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
class Subtract(ACK.Register.Types.Nodes.Node):
    bl_label = "Subtract"
    bl_description = "Subtract two numbers"

    def init(self, context: bpy_types.Context) -> None:
        self.inputs.new("NodeSocketFloat", "A")
        self.inputs.new("NodeSocketFloat", "B")
        self.outputs.new("NodeSocketFloat", "Result")

    def evaluate(self, inputs) -> None:
        result = round(inputs["A"] - inputs["B"], 6)
        self.outputs[0].default_value = result
        self.outputs[0].name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
class Multiply(ACK.Register.Types.Nodes.Node):
    bl_label = "Multiply"
    bl_description = "Multiply two numbers"

    def init(self, context: bpy_types.Context) -> None:
        self.inputs.new("NodeSocketFloat", "A")
        self.inputs.new("NodeSocketFloat", "B")
        self.outputs.new("NodeSocketFloat", "Result")

    def evaluate(self, inputs) -> None:
        result = round(inputs["A"] * inputs["B"], 6)
        self.outputs[0].default_value = result
        self.outputs[0].name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
class Divide(ACK.Register.Types.Nodes.Node):
    bl_label = "Divide"
    bl_description = "Divide two numbers"

    def init(self, context: bpy_types.Context) -> None:
        self.inputs.new("NodeSocketFloat", "A")
        self.inputs.new("NodeSocketFloat", "B")
        self.outputs.new("NodeSocketFloat", "Result")

    def evaluate(self, inputs) -> None:
        result = round(inputs["A"] / inputs["B"], 6)
        self.outputs[0].default_value = result
        self.outputs[0].name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
class Modulo(ACK.Register.Types.Nodes.Node):
    bl_label = "Modulo"
    bl_description = "Modulo two numbers"

    def init(self, context: bpy_types.Context) -> None:
        self.inputs.new("NodeSocketFloat", "A")
        self.inputs.new("NodeSocketFloat", "B")
        self.outputs.new("NodeSocketFloat", "Result")

    def evaluate(self, inputs) -> None:
        result = round(inputs["A"] % inputs["B"], 6)
        self.outputs[0].default_value = result
        self.outputs[0].name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
class Power(ACK.Register.Types.Nodes.Node):
    bl_label = "Power"
    bl_description = "Power two numbers"

    def init(self, context: bpy_types.Context) -> None:
        self.inputs.new("NodeSocketFloat", "Base")
        self.inputs.new("NodeSocketFloat", "Exponent")
        self.outputs.new("NodeSocketFloat", "Result")

    def evaluate(self, inputs) -> None:
        result = round(inputs["Base"] ** inputs["Exponent"], 6)
        self.outputs[0].default_value = result
        self.outputs[0].name = str(result)


@ACK.Flags.NODE_CATEGORY("Math")
class SquareRoot(ACK.Register.Types.Nodes.Node):
    bl_label = "Square Root"
    bl_description = "Square root of a number"

    def init(self, context: bpy_types.Context) -> None:
        self.inputs.new("NodeSocketFloat", "Number")
        self.outputs.new("NodeSocketFloat", "Result")

    def evaluate(self, inputs) -> None:
        result = round(math.sqrt(inputs["Number"]), 6)
        self.outputs[0].default_value = result
        self.outputs[0].name = str(result)


@ACK.Flags.NODE_CATEGORY("Math")
class Logarithm(ACK.Register.Types.Nodes.Node):
    bl_label = "Logarithm"
    bl_description = "Logarithm of a number"
    
    def init(self, context: bpy_types.Context) -> None:
        self.inputs.new("NodeSocketFloat", "Number")
        self.inputs.new("NodeSocketFloat", "Base")
        self.outputs.new("NodeSocketFloat", "Result")

    def evaluate(self, inputs) -> None:
        result = round(math.log(inputs["Number"], inputs["Base"]), 6)
        self.outputs[0].default_value = result
        self.outputs[0].name = str(result)


@ACK.Flags.NODE_CATEGORY("Math")
class Exponential(ACK.Register.Types.Nodes.Node):
    bl_label = "Exponential"
    bl_description = "Exponential of a number"

    def init(self, context: bpy_types.Context) -> None:
        self.inputs.new("NodeSocketFloat", "Number")
        self.outputs.new("NodeSocketFloat", "Result")

    def evaluate(self, inputs) -> None:
        result = round(math.exp(inputs["Number"]), 6)
        self.outputs[0].default_value = result
        self.outputs[0].name = str(result)
