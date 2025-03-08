from typing import Set, Dict, Any, Union, List
from collections.abc import Sequence

from mathutils import Color, Vector
from bpy import types as bpy_types

from ..base_type import BaseType
from ....globals import GLOBALS
from .node_socket import NodeSocket
from .sockets.annotation import NodeSocketWrapper

__all__ = ['Node']


class InputValues(Dict[str, Any], Sequence):
    """
    A dictionary that also supports index access for node input values.
    Can be accessed by input name (dict style) or by index (list style).
    """
    def __init__(self, names: list[str], values: list[Any]):
        super().__init__(zip(names, values))
        self._values = values
    
    def __getitem__(self, key: Union[int, str]) -> Any:
        if isinstance(key, int):
            return self._values[key]
        return super().__getitem__(key)
    
    def __len__(self) -> int:
        return len(self._values)
    
    def __iter__(self):
        return iter(self._values)


class Node(BaseType, bpy_types.Node):
    # Runtime.
    # Use default tree type value.
    _node_tree_type: str = f"{GLOBALS.ADDON_MODULE_SHORT.upper()}_TREETYPE"
    _node_category: str

    @classmethod
    def poll(cls, node_tree: bpy_types.NodeTree) -> bool:
        return node_tree.bl_idname == cls._node_tree_type

    @property
    def node_tree(self) -> bpy_types.NodeTree:
        return self.id_data
    
    @property
    def node_tree_type(self) -> str:
        return self.id_data.bl_idname

    def init(self, context: bpy_types.Context) -> None:
        """When the node is created. """
        print("Node.init:", self.name, self.original_cls.__dict__)
        for name, socket_wrapper in self.original_cls.__dict__.items():
            if isinstance(socket_wrapper, NodeSocketWrapper):
                socket_wrapper_instance = socket_wrapper.create_instance(self)
                setattr(self, name, socket_wrapper_instance)
                # print(f"Node.init: new socket: {name}, {getattr(self, name)}, {socket_wrapper_instance.socket}")

    def get_dependent_nodes(self) -> List['Node']:
        """Get all nodes that depend on this node's outputs"""
        dependent_nodes = []
        for output in self.outputs:
            for link in output.links:
                if link.to_node not in dependent_nodes:
                    dependent_nodes.append(link.to_node)
        return dependent_nodes

    def get_input_values(self) -> InputValues:
        """Get all input values, either from linked nodes or default values"""
        names = [socket.name for socket in self.inputs]
        values = []
        
        for input_socket in self.inputs:
            if input_socket.links:
                from_socket = input_socket.links[0].from_socket
                values.append(from_socket.default_value)
            else:
                values.append(input_socket.default_value)
                
        return InputValues(names, values)

    def evaluate(self, inputs: InputValues) -> None:
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
        # Get input values
        inputs = self.get_input_values()

        # Evaluate this node
        self.evaluate(inputs)
        
        # Trigger updates for dependent nodes
        for dependent in self.get_dependent_nodes():
            dependent.process()
