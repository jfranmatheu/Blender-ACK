from typing import Set, Dict, Any, Union, List
from collections.abc import Sequence

from mathutils import Color, Vector
from bpy import types as bpy_types

from ..base_type import BaseType
from ....globals import GLOBALS
from .node_socket import NodeSocket

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


class Node(BaseType):
    bl_idname: str
    bl_label: str
    bl_description: str
    bl_options: Set[str]
    bl_icon: str
    
    # Attributes.
    color: Color
    width: int
    height: int
    location: Vector
    label: str
    name: str
    mute: bool
    select: bool
    parent: bpy_types.Node
    type: str
    use_custom_color: bool
    
    inputs: bpy_types.NodeInputs
    outputs: bpy_types.NodeOutputs
    
    # Runtime.
    # Use default tree type value.
    _node_tree_type: str = f"{GLOBALS.ADDON_MODULE_SHORT.upper()}_TREETYPE"
    _node_category: str

    @classmethod
    def tag_register(cls):
        return super().tag_register(bpy_types.Node, 'NODE')

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
        self.init_inputs()
        self.init_outputs()

    def init_inputs(self) -> None:
        add_input = self.inputs.new
        add_output = self.outputs.new
        for socket_name, socket in self.__annotations__.items():
            if isinstance(socket, NodeSocketWrapper):
                if socket.is_input:
                    add_input(socket.bl_idname, socket_name)
                else:
                    add_output(socket.bl_idname, socket_name)

    def init_outputs(self) -> None:
        pass

    def copy(self, original_node: bpy_types.Node) -> None:
        pass

    def free(self) -> None:
        pass

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

    '''def update(self) -> None:
        """Called when node or its inputs change"""
        print("node update", self.name)
        self.process()'''

    '''def draw_buttons(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> None:
        pass
    
    def draw_buttons_ext(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> None:
        pass
    
    def draw_label(self) -> str:
        pass

    def debug_zone_body_lazy_function_graph(self) -> None:
        pass
    
    def debug_zone_lazy_function_graph(self) -> None:
        pass'''
