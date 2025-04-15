from typing import Set, Dict, List, Tuple

from mathutils import Color, Vector
from bpy import types as bpy_types

from ...core.base_type import BaseType
from ...globals import GLOBALS


__all__ = ['NodeTree']


class NodeTree(BaseType, bpy_types.NodeTree):
    bl_idname: str = f"{GLOBALS.ADDON_MODULE_SHORT.upper()}_TREETYPE"
    bl_label: str
    bl_description: str
    bl_icon: str = 'DOT'
    
    to_remove_links: List[Tuple[bpy_types.NodeSocket, bpy_types.NodeSocket]] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_remove_links = []

    @classmethod
    def poll_space(cls, context: bpy_types.Context) -> bool:
        """Check if the space is a node editor"""
        return context.space_data.type == 'NODE_EDITOR' and context.space_data.tree_type == cls.bl_idname

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        """Check visibility in the editor"""
        return True

    def tag_remove_link(self, link: bpy_types.NodeLink):
        """Tag a link for removal"""
        if not hasattr(self, "to_remove_links"):
            self.to_remove_links = []
        self.to_remove_links.append((link.from_socket.uid, link.to_socket.uid))

    def get_input_nodes(self):
        """Get all nodes that have no inputs or unconnected inputs"""
        input_nodes = []
        for node in self.nodes:
            is_input = True
            for input in node.inputs:
                if input.links:
                    is_input = False
                    break
            if is_input:
                input_nodes.append(node)
        return input_nodes

    def update(self) -> None:
        """Called when the node tree is modified"""
        if not self.nodes:
            return

        # Remove links
        if hasattr(self, "to_remove_links") and len(self.to_remove_links) > 0:
            for (from_socket, to_socket) in self.to_remove_links:
                for link in reversed(from_socket.links):
                    if link.to_socket.uid == to_socket and link.from_socket.uid == from_socket:
                        self.links.remove(link)
            self.to_remove_links.clear()

        # Only evaluate from input nodes
        for input_node in self.get_input_nodes():
            if not hasattr(input_node, "process"):
                print(f"WARN! Node {input_node.name} has no process method!")
                continue
            input_node.process()

    def evaluate(self) -> None:
        """Manual evaluation of the entire node tree"""
        self.update()
