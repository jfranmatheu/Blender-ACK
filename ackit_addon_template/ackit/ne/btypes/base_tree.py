from typing import Dict, List, Tuple
from collections import defaultdict

from bpy import types as bpy_types

from ...core.base_type import BaseType


__all__ = ['BaseNodeTree']


to_remove_links: Dict[int, List[Tuple[bpy_types.NodeSocket, bpy_types.NodeSocket]]] = defaultdict(list)


class BaseNodeTree: # BaseType:
    bl_icon: str

    @classmethod
    def poll_space(cls, context: bpy_types.Context) -> bool:
        """Check if the space is a node editor"""
        if not hasattr(cls, 'bl_idname'):
            return False
        return context.space_data.type == 'NODE_EDITOR' and context.space_data.tree_type == cls.bl_idname

    @classmethod
    def poll(cls, context: bpy_types.Context) -> bool:
        """Check visibility in the editor"""
        return True

    def tag_remove_link(self, link: bpy_types.NodeLink):
        """Tag a link for removal"""
        # Check if sockets have uid attribute before trying to access it
        from_uid = getattr(link.from_socket, "uid", None)
        to_uid = getattr(link.to_socket, "uid", None)
        
        # Only add the link for removal if both UIDs are valid
        if from_uid is not None and to_uid is not None:
            global to_remove_links
            to_remove_links[id(self)].append((from_uid, to_uid))
        else:
            # Alternative: try to remove directly if no uid
            try:
                self.links.remove(link)
            except Exception as e:
                print(f"Error removing link: {e}")

    def clear_tagged_links(self) -> None:
        """Called when the node tree is modified"""
        if not self.nodes:
            return

        # Remove links
        global to_remove_links
        links_to_remove = to_remove_links[id(self)]
        if len(links_to_remove) > 0:
            for (from_socket, to_socket) in links_to_remove:
                for link in reversed(self.links):
                    if (hasattr(link.to_socket, "uid") and hasattr(link.from_socket, "uid") and
                        link.to_socket.uid == to_socket and link.from_socket.uid == from_socket):
                        self.links.remove(link)
                        break
            to_remove_links[id(self)] = []

    def evaluate(self) -> None:
        """Manual evaluation of the entire node tree"""
        self.update()
