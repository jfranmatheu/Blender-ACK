from .node import Node
from typing import Dict, Any, Type, Set, List, Optional

from bpy import types as bpy_types
import bpy

from .node_socket_exec import NodeSocketExec

__all__ = ['NodeExec']


class NodeExec(Node):
    """Node that can be executed inside an executable tree (NodeTreeExec).
        Execution flow passes arguments tailored to specific input sockets.
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
        # Allow Any or specific type matches (adjust as needed)
        if from_socket_type is Any or to_socket_type is Any:
             return True
        if from_socket_type == to_socket_type:
             return True
        # Add more sophisticated checks if needed (e.g., inheritance)
        # print(f"Link verification failed: {from_socket_type} -> {to_socket_type}")
        return False # Default to False if types don't match explicitly

    def _internal_execute(self, *args, _execution_tracker: Set[str], **kwargs):
        """ Internal execution wrapper called by the tree or parent nodes.
            Calls the node's execute method and passes context down specific
            input socket branches based on the returned mapping.
        """
        # 1. Check execution tracker
        if self.name in _execution_tracker:
            return
        _execution_tracker.add(self.name)

        # 2. Call the user-defined execute method
        #    It now returns a mapping from input socket identifiers to their specific kwargs.
        socket_specific_kwargs_map: Optional[Dict[str, Dict[str, Any]]] = None
        try:
            socket_specific_kwargs_map = self.execute(*args, **kwargs)
        except Exception as e:
            import traceback
            print(f"Error during user execute of node '{self.name}': {e}")
            traceback.print_exc()
            return # Stop processing this branch on error

        # 3. Execute children connected to NodeSocketExec inputs
        for socket in self.inputs:
            # Ensure it's an executable socket and is linked
            if isinstance(socket, NodeSocketExec) and socket.is_linked:

                # Determine the kwargs for children connected to *this* socket
                child_kwargs = kwargs.copy() # Start with kwargs passed to this node
                if isinstance(socket_specific_kwargs_map, dict) and socket in socket_specific_kwargs_map:
                    # Get the specific args for this socket from the map
                    socket_specific_args = socket_specific_kwargs_map[socket] # Use socket.identifier
                    if isinstance(socket_specific_args, dict):
                        # Update the base kwargs with the socket-specific ones
                        child_kwargs.update(socket_specific_args)
                        # print(f"Node '{self.name}': Passing specific kwargs for socket '{socket.identifier}': {list(socket_specific_args.keys())}")
                else:
                    child_kwargs.update(socket_specific_kwargs_map)

                # Execute all children connected to this socket
                for link in socket.links:
                    child_node = link.from_node
                    if child_node and hasattr(child_node, '_internal_execute'):
                        try:
                            # Pass original args, the potentially updated child_kwargs, and tracker
                            child_node._internal_execute(*args, _execution_tracker=_execution_tracker, **child_kwargs)
                        except Exception as e:
                            import traceback
                            print(f"Error calling _internal_execute on child node '{child_node.name}' from '{self.name}.{socket.identifier}': {e}")
                            traceback.print_exc()
                    elif child_node:
                        print(f"Warning: Connected node '{child_node.name}' to '{self.name}.{socket.identifier}' has no _internal_execute method.")


    # User-defined execute method - MUST be overridden by subclasses
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        User-defined execution logic for the node.

        Args:
            *args: Positional arguments passed down the execution chain.
            **kwargs: Keyword arguments passed down the execution chain.
                      Nodes should extract needed arguments using kwargs.get('key').
                      Layout nodes typically expect 'parent_layout'.

        Returns:
            An optional dictionary mapping this node's input socket identifiers
            (e.g., 'InContent', 'InHeader') to a dictionary of keyword arguments
            that should be passed specifically to children connected to that
            respective input socket. Return None if no specific context needs
            to be passed or if the node doesn't execute children via inputs.
        """
        print(f"Warning: Node '{self.name}' uses default NodeExec.execute(). Subclass should override this.")
        return None # Default: no specific context for any input socket

    def process(self) -> None:
        raise NotImplementedError("Method not available for NodeExec.")

    def evaluate(self) -> None:
        raise NotImplementedError("Method not available for NodeExec.")
    
    def on_property_update(self, context: bpy_types.Context, prop_name: str):
        pass
