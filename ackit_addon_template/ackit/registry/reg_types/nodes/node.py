from typing import Set, Dict, Any, Union, List
from collections.abc import Sequence

from mathutils import Color, Vector
from bpy import types as bpy_types

from ..base_type import BaseType
from ....globals import GLOBALS
from .node_socket import NodeSocket
from .sockets.annotation import NodeSocketWrapper

__all__ = ['Node']



class Node(BaseType, bpy_types.Node):
    # Runtime.
    # Use default tree type value.
    _node_tree_type: str = f"{GLOBALS.ADDON_MODULE_SHORT.upper()}_TREETYPE"
    _node_category: str
    _input_descriptors: Dict[str, NodeSocketWrapper] = {}
    _output_descriptors: Dict[str, NodeSocketWrapper] = {}

    @classmethod
    def poll(cls, node_tree: bpy_types.NodeTree) -> bool:
        return node_tree.bl_idname == cls._node_tree_type

    @property
    def node_tree(self) -> bpy_types.NodeTree:
        return self.id_data

    @property
    def node_tree_type(self) -> str:
        return self.id_data.bl_idname

    def on_property_update(self, context: bpy_types.Context, prop_name: str):
        print(f"Node.on_property_update: {prop_name}")
        self.process()

    def init(self, context: bpy_types.Context) -> None:
        """When the node is created. """
        print("Node.init:", self.name)
        self.setup_sockets()

    def setup_sockets(self):
        for input_name, input_wrapper in self._input_descriptors.items():
            assert input_wrapper.socket is not None, f"InputNodeSocketWrapper.socket is not None! Maybe wrapper instance is shared with another node? - {self} vs {input_wrapper.socket.node}"
            input_wrapper._ensure_socket_exists(self, input_name)
            print("setup input socket!", input_name, input_wrapper)
        for output_name, output_wrapper in self._output_descriptors.items():
            assert output_wrapper.socket is not None, f"OutNodeSocketWrapper.socket is not None! Maybe wrapper instance is shared with another node? - {self} vs {output_wrapper.socket.node}"
            output_wrapper._ensure_socket_exists(self, output_name)
            print("setup output socket!", output_name, output_wrapper)

    def get_dependent_nodes(self) -> List['Node']:
        """Get all nodes that depend on this node's outputs"""
        dependent_nodes = []
        for output in self.outputs:
            for link in output.links:
                if link.to_node not in dependent_nodes:
                    dependent_nodes.append(link.to_node)
        return dependent_nodes

    def evaluate(self) -> None:
        """
        Evaluate the node with the given input values.
        This method should be overridden by node subclasses.
        """
        pass

    def process(self) -> None:
        """
        Process this node and trigger updates to dependent nodes.
        This is the main entry point for node evaluation.
        """
        # Evaluate this node
        self.evaluate()
        
        # Trigger updates for dependent nodes
        for dependent in self.get_dependent_nodes():
            dependent.process()
