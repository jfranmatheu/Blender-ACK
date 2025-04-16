from .node import Node
from typing import Dict, Any, Type

from bpy import types as bpy_types

from .node_socket_exec import NodeSocketExec


class NodeExec(Node):
    """Node that can be executed inside an executable tree (NodeTreeExec).
        They don't support casting between sockets yet, so they are more restrictive.
        Data type between sockets must be the same or the socket type must be the same.
    """

    def verify_link(self, link: bpy_types.NodeLink) -> bool:
        """Verify if the link is valid"""
        from_socket: NodeSocketExec = link.from_socket  # cast to ACK NodeSocketExec
        to_socket: NodeSocketExec = link.to_socket  # cast to ACK NodeSocketExec
        if from_socket.__class__ == to_socket.__class__:
            # Same socket type.
            return True
        from_socket_type: Type[Any] | None = from_socket.value_type
        to_socket_type: Type[Any] | None = to_socket.value_type
        assert from_socket_type is not None and to_socket_type is not None, f"Link {link} has invalid socket types: {from_socket_type} -> {to_socket_type}"
        '''if from_socket_type == to_socket_type:
            # Strictly equal types. (tho they could be vector/matrix with different lengths that should be casted)
            return True'''
        if from_socket_type == to_socket_type:
            return True
        return False

    def process(self) -> None:
        raise NotImplementedError("Method not available for NodeExec.")

    def evaluate(self) -> None:
        raise NotImplementedError("Method not available for NodeExec.")
