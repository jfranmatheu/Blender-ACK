from typing import Dict, List, Tuple, Any
from collections import defaultdict

from bpy import types as bpy_types

from ...core.base_type import BaseType


__all__ = ['BaseNodeTree']


to_remove_links: Dict[int, List[Tuple[bpy_types.NodeSocket, bpy_types.NodeSocket]]] = defaultdict(list)


class BaseNodeTree: # BaseType:
    bl_icon: str
    
    links: List[bpy_types.NodeLink]
    nodes: List[bpy_types.Node]

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
        """Manual evaluation of the entire node tree - intended for non-exec trees?"""
        # self.update() # Removed: BaseNodeTree doesn't have update
        pass # Or implement base evaluation if needed

    def serialize(self) -> Dict[str, List[Dict[str, Any]]]:
        """Serializes the entire node tree structure."""
        serialized_data = {"nodes": [], "links": []}

        # Serialize Nodes
        for node in self.nodes:
            if hasattr(node, 'serialize') and callable(node.serialize):
                try:
                    serialized_data["nodes"].append(node.serialize())
                except Exception as e:
                    node_name = getattr(node, 'name', 'UNKNOWN')
                    print(f"Error serializing node '{node_name}': {e}")
            else:
                # Handle nodes without a serialize method (optional warning)
                node_name = getattr(node, 'name', 'UNKNOWN')
                node_type_name = type(node).__name__
                print(f"Warning: Node '{node_name}' of type {node_type_name} has no serialize method. Skipping.")

        # Serialize Links
        for link in self.links:
            try:
                from_node_id = getattr(link.from_node, 'name', None)
                from_socket_id = getattr(link.from_socket, 'identifier', None)
                to_node_id = getattr(link.to_node, 'name', None)
                to_socket_id = getattr(link.to_socket, 'identifier', None)

                if not all([from_node_id, from_socket_id, to_node_id, to_socket_id]):
                    print(f"Warn: Skipping link {link}, missing info.")
                    continue

                serialized_data["links"].append({
                    "from_node": from_node_id,
                    "from_socket": from_socket_id,
                    "to_node": to_node_id,
                    "to_socket": to_socket_id,
                })
            except Exception as e:
                print(f"Error serializing link {link}: {e}")

        return serialized_data
