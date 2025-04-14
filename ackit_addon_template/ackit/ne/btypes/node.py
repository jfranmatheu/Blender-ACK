from typing import Set, Dict, Any, Union, List, ItemsView
from uuid import uuid4

from bpy import types as bpy_types

from ...core.base_type import BaseType
from ...globals import GLOBALS
from ..annotations_internal import NodeSocketWrapper

__all__ = ['Node']



class Node(BaseType, bpy_types.Node):
    # Runtime.
    # Use default tree type value.
    _addon_short = GLOBALS.ADDON_MODULE_SHORT or "ACK" # Provide default if None
    _node_tree_type: str = f"{_addon_short.upper()}_TREETYPE"
    _node_category: str
    _color_tag: str = 'NONE'

    @property
    def uid(self) -> str:
        return self.name

    @classmethod
    def poll(cls, node_tree: bpy_types.NodeTree) -> bool:
        return node_tree.bl_idname == cls._node_tree_type

    @property
    def node_tree(self) -> bpy_types.NodeTree:
        return self.id_data

    @property
    def node_tree_type(self) -> str:
        return self.id_data.bl_idname

    @classmethod
    def _get_socket_descriptors(cls, io_type: str) -> ItemsView[str, NodeSocketWrapper]:
        """Helper to find socket descriptors of a specific io type."""
        descriptors = {}
        for name, value in cls.__dict__.items():
            if isinstance(value, NodeSocketWrapper):
                if io_type == 'INPUT' and (value.is_input or value.is_multi_input):
                    descriptors[name] = value
                elif io_type == 'OUTPUT' and value.is_output:
                    descriptors[name] = value
        return descriptors.items() # Return ItemsView like dict.items()

    @classmethod
    def get_input_socket_descriptors(cls) -> ItemsView[str, NodeSocketWrapper]:
        """Dynamically finds input socket descriptors defined on the class."""
        return cls._get_socket_descriptors('INPUT')

    @classmethod
    def get_output_socket_descriptors(cls) -> ItemsView[str, NodeSocketWrapper]:
        """Dynamically finds output socket descriptors defined on the class."""
        return cls._get_socket_descriptors('OUTPUT')

    def on_property_update(self, context: bpy_types.Context, prop_name: str):
        print(f"Node.on_property_update: {prop_name}")
        self.process()

    def init(self, context: bpy_types.Context) -> None:
        """When the node is created. """
        uid = uuid4().hex
        print("Node.init:", self.name, uid)
        self.label = self.name
        self.name = uid
        self.setup_sockets()

    def setup_sockets(self):
        # Call the new class methods to get descriptors
        input_descriptors = self.__class__.get_input_socket_descriptors()
        output_descriptors = self.__class__.get_output_socket_descriptors()

        ## print("Node.setup_sockets:", self.name, input_descriptors, output_descriptors)
        
        for input_name, input_wrapper in input_descriptors:
            input_wrapper._ensure_socket_exists(self)
            ## print("setup input socket!", input_name, input_wrapper)
            
        for output_name, output_wrapper in output_descriptors:
            output_wrapper._ensure_socket_exists(self)
            ## print("setup output socket!", output_name, output_wrapper)

    def get_dependent_nodes(self) -> List['Node']:
        """Get all nodes that depend on this node's outputs"""
        dependent_nodes = []
        for output in self.outputs:
            for link in output.links:
                if isinstance(link.to_node, Node) and link.to_node not in dependent_nodes:
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
            if hasattr(dependent, "process") and callable(dependent.process):
                dependent.process()
            else:
                print(f"WARN! Node {dependent.name} (type: {type(dependent)}) has no callable process method!")
