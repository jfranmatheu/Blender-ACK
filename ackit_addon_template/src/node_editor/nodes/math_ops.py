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
@ACK.Metadata.Node(label="Math: Modulo", tooltip="Modulo 2 numbers")
class Modulo(ACK.Register.Types.Nodes.Node):
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
@ACK.Metadata.Node(label="Math: Power", tooltip="Power 2 numbers", icon='CON_TRANSLIKE')
class Power(ACK.Register.Types.Nodes.Node):
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
@ACK.Metadata.Node(label="Math: Square Root", tooltip="Square root of a number", icon='IPO_QUAD')
class SquareRoot(ACK.Register.Types.Nodes.Node):
    # Inputs.
    Number = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(math.sqrt(self.Number.value), 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.Flags.NODE_CATEGORY("Math")
@ACK.Metadata.Node(label="Math: Logarithm", tooltip="Logarithm of a number")
class Logarithm(ACK.Register.Types.Nodes.Node):
    # Inputs.
    Number = ACK.NodeInput(ACK.Types.NodeSocketFloat)
    Base = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        if self.Base.value <= 1:
            self.mute = True
            return
        if self.Number.value <= 0:
            self.mute = True
            return
        elif self.mute:
            self.mute = False
        result = round(math.log(self.Number.value, self.Base.value), 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.Flags.NODE_CATEGORY("Math")
@ACK.Metadata.Node(label="Math: Exponential", tooltip="Exponential of a number", icon='IPO_CIRC')
class Exponential(ACK.Register.Types.Nodes.Node):
    # Inputs.
    Number = ACK.NodeInput(ACK.Types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NodeOutput(ACK.Types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(math.exp(self.Number.value), 6)
        self.Result.value = result
        self.Result.name = str(result)
