import math

from ....ackit import ACK


@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Add", tooltip="Add 2 numbers", icon='ADD')
@ACK.NE.NodeFlags.ColorTag.VECTOR
class Add(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)
    B = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)

    # Outputs.
    Result = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)

    def evaluate(self) -> None:
        result = round(self.A.value + self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Subtract", tooltip="Subtract 2 numbers", icon='REMOVE')
@ACK.NE.NodeFlags.ColorTag.VECTOR
class Subtract(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)
    B = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)

    # Outputs.
    Result = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)

    def evaluate(self) -> None:
        result = round(self.A.value - self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Multiply", tooltip="Multiply 2 numbers", icon='X')
class Multiply(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)
    B = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)

    # Outputs.
    Result = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)

    def evaluate(self) -> None:
        result = round(self.A.value * self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Divide", tooltip="Divide 2 numbers", icon='FIXED_SIZE')
class Divide(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)
    B = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)

    # Outputs.
    Result = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)

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
@ACK.NE.add_node_metadata(label="Modulo", tooltip="Modulo 2 numbers")
class Modulo(ACK.NE.Node):
    # Inputs.
    A = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)
    B = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)

    # Outputs.
    Result = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)

    def evaluate(self) -> None:
        result = round(self.A.value % self.B.value, 6)
        self.Result.value = result
        self.Result.name = str(result)

@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Power", tooltip="Power 2 numbers", icon='CON_TRANSLIKE')
@ACK.NE.NodeFlags.ColorTag.VECTOR
class Power(ACK.NE.Node):
    # Inputs.
    Base = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)
    Exponent = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)

    # Outputs.
    Result = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)

    def evaluate(self) -> None:
        result = round(self.Base.value ** self.Exponent.value, 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Square Root", tooltip="Square root of a number", icon='IPO_QUAD')
@ACK.NE.NodeFlags.ColorTag.VECTOR
class SquareRoot(ACK.NE.Node):
    # Inputs.
    Number = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)

    # Outputs.
    Result = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)

    def evaluate(self) -> None:
        result = round(math.sqrt(self.Number.value), 6)
        self.Result.value = result
        self.Result.name = str(result)


@ACK.NE.add_node_to_category("Math")
@ACK.NE.add_node_metadata(label="Logarithm", tooltip="Logarithm of a number")
@ACK.NE.NodeFlags.ColorTag.VECTOR
class Logarithm(ACK.NE.Node):
    # Inputs.
    Number = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)
    Base = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)

    # Outputs.
    Result = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)

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
@ACK.NE.add_node_metadata(label="Exponential", tooltip="Exponential of a number", icon='IPO_CIRC')
@ACK.NE.NodeFlags.ColorTag.VECTOR
class Exponential(ACK.NE.Node):
    # Inputs.
    Number = ACK.NE.InputSocket(ACK.NE.SocketTypes.FLOAT)

    # Outputs.
    Result = ACK.NE.OutputSocket(ACK.NE.SocketTypes.FLOAT)

    def evaluate(self) -> None:
        result = round(math.exp(self.Number.value), 6)
        self.Result.value = result
        self.Result.name = str(result)
