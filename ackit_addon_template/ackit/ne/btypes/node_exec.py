from .node import Node
from typing import Dict, Any, Type, Set, List, Optional

from bpy import types as bpy_types
import bpy

from .node_socket_exec import NodeSocketExec

__all__ = ['NodeExec']


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

    def _internal_execute(self, *args, _execution_tracker: Set[str], **kwargs):
        """ Internal execution wrapper called by the tree or parent nodes. """
        # 1. Check execution tracker
        if self.name in _execution_tracker:
            return
        _execution_tracker.add(self.name)

        # 2. Call the user-defined execute method, passing generic args/kwargs
        returned_data: Optional[Dict[str, Any]] = None
        try:
            # Assume execute returns a dictionary of arguments for children, or None
            returned_data = self.execute(*args, **kwargs)
        except Exception as e:
            import traceback
            print(f"Error during user execute of node '{self.name}': {e}")
            traceback.print_exc()
            return # Stop processing this branch on error

        # 3. Prepare kwargs for children
        child_kwargs = kwargs.copy() # Start with the kwargs received by this node
        if isinstance(returned_data, dict):
            # Update the kwargs with the data returned by this node's execute
            # This allows the node to modify/pass data (like a new layout) to its children
            child_kwargs.update(returned_data)

        # 4. Execute children connected to NodeSocketExec inputs
        for socket in self.inputs:
            if isinstance(socket, NodeSocketExec) and socket.is_linked:
                for link in socket.links:
                    child_node = link.from_node
                    if child_node and hasattr(child_node, '_internal_execute'):
                        try:
                            # Pass original args, the potentially updated child_kwargs, and tracker
                            child_node._internal_execute(*args, _execution_tracker=_execution_tracker, **child_kwargs)
                        except Exception as e:
                            import traceback
                            print(f"Error calling _internal_execute on child node '{child_node.name}' from '{self.name}': {e}")
                            traceback.print_exc()
                    elif child_node:
                        print(f"Warning: Connected node '{child_node.name}' to '{self.name}.{socket.name}' has no _internal_execute method.")

    # User-defined execute method - MUST be overridden by subclasses
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        """
        User-defined execution logic for the node.

        Args:
            *args: Positional arguments passed down the execution chain.
            **kwargs: Keyword arguments passed down the execution chain.
                      Specific node systems will define expected keys (e.g., 'context', 'parent_layout').

        Returns:
            An optional dictionary containing keyword arguments to be passed to
            child nodes. This allows modifying the execution context for children
            (e.g., providing a new 'parent_layout'). Return None or {} if the
            context for children should not change.
        """
        print(f"Warning: Node '{self.name}' uses default NodeExec.execute(). Subclass should override this.")
        return None # Default: no changes to child kwargs

    def process(self) -> None:
        raise NotImplementedError("Method not available for NodeExec.")

    def evaluate(self) -> None:
        raise NotImplementedError("Method not available for NodeExec.")
