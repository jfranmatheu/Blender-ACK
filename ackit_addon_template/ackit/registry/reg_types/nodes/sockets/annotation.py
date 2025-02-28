from enum import Enum, auto
from .socket_types import NodeSocket


__all__ = ['NodeSocketAnnotation', 'NodeSocketWrapper']


class NodeSocketWrapper:
    def __init__(self, idname: str, io: str):
        self.idname = idname
        self.io = io

    @property
    def is_input(self) -> bool:
        return self.io == 'INPUT'

    @property
    def is_multi_input(self) -> bool:
        return self.io == 'MULTI_INPUT'

    @property
    def is_output(self) -> bool:
        return self.io == 'OUTPUT'


class NodeSocketAnnotation(Enum):
    INPUT = auto()
    OUTPUT = auto()
    MULTI_INPUT = auto()
    
    def __call__(self, socket: NodeSocket | str) -> NodeSocketWrapper:
        return NodeSocketWrapper(socket if isinstance(socket, str) else socket.bl_idname, self.name)
