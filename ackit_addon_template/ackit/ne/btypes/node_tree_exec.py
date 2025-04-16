from typing import Set, Dict, List, Optional
from collections import defaultdict

from bpy import types as bpy_types

from ...core.base_type import BaseType

from .node_socket_exec import NodeSocketExec
from .base_tree import BaseNodeTree


__all__ = ['NodeTreeExec']


nodes_to_execute: Dict[int, List[str]] = defaultdict(list)
_visited_nodes_walk: Dict[int, Set[str]] = defaultdict(set)


class NodeTreeExec(BaseNodeTree, BaseType, bpy_types.NodeTree):
    bl_icon: str = 'SETTINGS'

    def update(self) -> None:
        """Called when the node tree is modified"""
        self.clear_tagged_links()

        global nodes_to_execute, _visited_nodes_walk

        if not self.nodes:
            nodes_to_execute.clear()
            return

        # The executable NodeTree has no evaluation logic.
        # Instead, in the update method, we will do a tree walk to sort and gather the nodes in RTL branching order.
        # This is so that the interpreter can execute the nodes in the correct order via 'tree.execute()' method.
        try:
            self.walk_tree()
        except Exception as e:
            import traceback
            print(f"Error walking node tree: {e}")
            traceback.print_exc()
            nodes_to_execute.clear()  # Clear on error

    def _walk_backwards(self, node: Optional[bpy_types.Node]) -> None:
        """Recursive helper for post-order traversal."""
        global nodes_to_execute, _visited_nodes_walk

        if not node or node.name in _visited_nodes_walk:
            return
        _visited_nodes_walk[id(self)].add(node.name)

        # Recursively visit nodes connected to the inputs of this node
        for input_socket in node.inputs:
            for link in input_socket.links:
                # Check if the link originates from a valid node within the tree
                if link.from_node:
                    # Recursively call on the dependency (node connected to input)
                    self._walk_backwards(link.from_node)

        # After visiting all preceding nodes (dependencies), add this node
        # ensuring it hasn't been added already through another path.
        if node.name not in nodes_to_execute[id(self)]:
            nodes_to_execute[id(self)].append(node.name)

    def walk_tree(self) -> None:
        """Walk the tree backwards and gather nodes in execution order using post-order traversal."""
        # Clear previous results and visited set for the new walk
        global nodes_to_execute, _visited_nodes_walk

        nodes_to_execute[id(self)].clear()
        _visited_nodes_walk[id(self)].clear()

        if not self.nodes:
            return # Nothing to walk

        # Iterate through all nodes to ensure disconnected graphs are handled.
        # The `_visited_nodes_walk` set prevents processing nodes multiple times.
        for node in self.nodes:
            # If a node hasn't been visited yet, start a walk from it.
            # This ensures all nodes (even in disconnected parts) are considered.
            if node.name not in _visited_nodes_walk[id(self)]:
                self._walk_backwards(node)
        # self.nodes_to_execute now contains the node names in execution order

    def execute(self, *args, **kwargs) -> None:
        """Execute the node tree logic sequentially.

        Args:
            *args: Positional arguments passed down to each node's execute method.
            **kwargs: Keyword arguments passed down to each node's execute method.
                      These can be used for passing context (like 'context', 'layout').
        """
        
        global nodes_to_execute

        # Ensure execution order is up-to-date
        if not nodes_to_execute:
            self.update()

        if not nodes_to_execute:
            print("NodeTreeExec: No nodes to execute.")
            return

        # Iterate through nodes in execution order
        tree_id = id(self)
        print(f"Executing Tree: {self.name} with nodes {nodes_to_execute.get(tree_id, [])}") # Debug
        for node_name in nodes_to_execute.get(tree_id, []): # Iterate over names for this tree_id
            node: Optional[bpy_types.Node] = self.nodes.get(node_name, None) # Use node_name string key
            
            if node is None:
                print(f"Warning: Node '{node_name}' not found in tree.")
                continue

            if not hasattr(node, 'execute'):
                print(f"Warning: Node '{node_name}' has no execute method.")
                continue

            # Execute the node
            try:
                # Cast to expected type if needed, or ensure NodeSocketExec is the base type
                # Assuming nodes retrieved are compatible with execute call signature
                print("Executing node:", node.label)
                node.execute(*args, **kwargs) 
            except Exception as e:
                import traceback
                print(f"Error executing node '{node_name}': {e}")
                traceback.print_exc()
                # Optionally, stop execution or continue with next node
                break


    def evaluate(self) -> None:
        """Manual evaluation of the entire node tree"""
        self.update()
