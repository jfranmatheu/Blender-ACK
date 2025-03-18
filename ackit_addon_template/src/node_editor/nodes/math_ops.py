from bpy import types as bpy_types
import math

from ....ackit import ACK


@ACK.Flags.NODE_CATEGORY("Math")
@ACK.Metadata.Node(label="Math: Add", tooltip="Add 2 numbers", icon='ADD')
class Add(ACK.Register.Types.Nodes.Node):
    # Inputs.
    A = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    B = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.A.value + self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
@ACK.Metadata.Node(label="Math: Substract", tooltip="Substract 2 numbers", icon='REMOVE')
class Subtract(ACK.Register.Types.Nodes.Node):
    bl_label = "Subtract"
    bl_description = "Subtract two numbers"

    # Inputs.
    A = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    B = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.A.value - self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
@ACK.Metadata.Node(label="Math: Multiply", tooltip="Multiply 2 numbers", icon='X')
class Multiply(ACK.Register.Types.Nodes.Node):
    bl_label = "Multiply"
    bl_description = "Multiply two numbers"

    # Inputs.
    A = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    B = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.A.value * self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
@ACK.Metadata.Node(label="Math: Divide", tooltip="Substract 2 numbers", icon='FIXED_SIZE')
class Divide(ACK.Register.Types.Nodes.Node):
    bl_label = "Divide"
    bl_description = "Divide two numbers"

    # Inputs.
    A = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    B = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        if self.B.value == 0:
            self.mute = True
            return
        elif self.mute:
            self.mute = False
        result = round(self.A.value / self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
class Modulo(ACK.Register.Types.Nodes.Node):
    bl_label = "Modulo"
    bl_description = "Modulo two numbers"

    # Inputs.
    A = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    B = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.A.value % self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.Flags.NODE_CATEGORY("Math")
class Power(ACK.Register.Types.Nodes.Node):
    bl_label = "Power"
    bl_description = "Power two numbers"

    # Inputs.
    Base = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    Exponent = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.Base.value ** self.Exponent.value, 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.Flags.NODE_CATEGORY("Math")
class SquareRoot(ACK.Register.Types.Nodes.Node):
    bl_label = "Square Root"
    bl_description = "Square root of a number"

    # Inputs.
    Number = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(math.sqrt(self.Number.value), 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.Flags.NODE_CATEGORY("Math")
class Logarithm(ACK.Register.Types.Nodes.Node):
    bl_label = "Logarithm"
    bl_description = "Logarithm of a number"
    
    # Inputs.
    Number = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    Base = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(math.log(self.Number.value, self.Base.value), 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.Flags.NODE_CATEGORY("Math")
class Exponential(ACK.Register.Types.Nodes.Node):
    bl_label = "Exponential"
    bl_description = "Exponential of a number"

    # Inputs.
    Number = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(math.exp(self.Number.value), 6)
        self.Result.value = result
        self.Result.name = str(result)
