from bpy import types as bpy_types
import math

from ....ackit import ACK


@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Math: Add", tooltip="Add 2 numbers", icon='ADD')
class Add(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)
    B = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.A.value + self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Math: Subtract", tooltip="Subtract 2 numbers", icon='REMOVE')
class Subtract(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)
    B = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.A.value - self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Math: Multiply", tooltip="Multiply 2 numbers", icon='X')
class Multiply(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)
    B = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.A.value * self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Math: Divide", tooltip="Divide 2 numbers", icon='FIXED_SIZE')
class Divide(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)
    B = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)

    def evaluate(self) -> None:
        if self.B.value == 0:
            self.mute = True
            return
        elif self.mute:
            self.mute = False
        result = round(self.A.value / self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Math: Modulo", tooltip="Modulo 2 numbers")
class Modulo(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)
    B = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.A.value % self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Math: Power", tooltip="Power 2 numbers", icon='CON_TRANSLIKE')
class Power(ACK.NE.Node):
    # Inputs.
    Base = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)
    Exponent = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(self.Base.value ** self.Exponent.value, 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Math: Square Root", tooltip="Square root of a number", icon='IPO_QUAD')
class SquareRoot(ACK.NE.Node):
    # Inputs.
    Number = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(math.sqrt(self.Number.value), 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Math: Logarithm", tooltip="Logarithm of a number")
class Logarithm(ACK.NE.Node):
    # Inputs.
    Number = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)
    Base = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)

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


@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Math: Exponential", tooltip="Exponential of a number", icon='IPO_CIRC')
class Exponential(ACK.NE.Node):
    # Inputs.
    Number = ACK.NE.new_input(ACK.NE.socket_types.NodeSocketFloat)

    # Outputs.
    Result = ACK.NE.new_output(ACK.NE.socket_types.NodeSocketFloat)

    def evaluate(self) -> None:
        result = round(math.exp(self.Number.value), 6)
        self.Result.value = result
        self.Result.name = str(result)
