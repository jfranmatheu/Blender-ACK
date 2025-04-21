from typing import Set, Dict, List, Optional, Any, Type, Tuple
from collections import defaultdict
import bpy
from bpy import types as bpy_types

from ...core.base_type import BaseType

from .node_socket_exec import NodeSocketExec
from .base_tree import BaseNodeTree
from .node_exec import NodeExec # Import NodeExec


__all__ = ['NodeTreeExec']


class NodeTreeExec(BaseNodeTree, BaseType, bpy_types.NodeTree):
    bl_icon: str = 'SETTINGS'
    output_node_type: Type[Any] | None = None
    
    @property
    def output_node(self) -> Optional[bpy_types.Node]:
        if not self.nodes:
            print(f"NodeTreeExec: Tree '{self.name}' has no nodes.")
            return None
        return next((node for node in self.nodes if node.__class__ == self.output_node_type), None)

    def update(self) -> None:
        """Called when the node tree is modified.
           Currently, no pre-calculation needed for execution order.
           May be used for validation or other updates later.
        """
        self.clear_tagged_links()
        # No tree walking needed here anymore
        pass

    def execute(self, *args, **kwargs) -> None:
        """Execute the node tree logic starting from the designated output node.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        # 1. Find the Output Node
        output_node: Optional[bpy_types.Node] = self.output_node

        if output_node is None:
            print(f"Error: Output node of type '{self.output_node_type}' not found in tree '{self.name}'.")
            return

        # Check for the internal execute method now
        if not hasattr(output_node, '_internal_execute'):
            print(f"Error: Output node '{output_node.name}' has no _internal_execute method.")
            return

        # 2. Initialize Execution Context
        execution_tracker: Set[str] = set()

        print(f"Executing Tree: {self.name} starting from Output Node: {output_node.name}")

        # 3. Start Execution from the Output Node's internal method
        try:
            # Pass all received args/kwargs directly, plus the tracker
            output_node._internal_execute(*args, _execution_tracker=execution_tracker, **kwargs)
        except Exception as e:
            import traceback
            print(f"Error executing output node '{output_node.name}': {e}")
            traceback.print_exc()
