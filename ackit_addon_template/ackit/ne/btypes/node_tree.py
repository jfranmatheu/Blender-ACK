from typing import Dict, List, Tuple
from collections import defaultdict

from bpy import types as bpy_types

from ...core.base_type import BaseType
from .base_tree import BaseNodeTree


__all__ = ['NodeTree']


to_remove_links: Dict[int, List[Tuple[bpy_types.NodeSocket, bpy_types.NodeSocket]]] = defaultdict(list)


class NodeTree(BaseNodeTree, BaseType, bpy_types.NodeTree):
    bl_icon: str = 'DOT'

    def update(self) -> None:
        """Called when the node tree is modified"""
        self.clear_tagged_links()

        # Only evaluate from input nodes
        try:
            # Get all input nodes
            input_nodes = []
            for node in self.nodes:
                is_input = True
                for input in node.inputs:
                    if hasattr(input, "links") and input.links:
                        is_input = False
                        break
                if is_input:
                    input_nodes.append(node)
            
            # Process input nodes
            for input_node in input_nodes:
                if not hasattr(input_node, "process"):
                    print(f"WARN! Node {input_node.name} has no process method!")
                    continue
                input_node.process()
        except Exception as e:
            print(f"Error in NodeTree.update: {e}")
