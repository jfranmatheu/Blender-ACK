from typing import Set, Dict, Any, Union, List, ItemsView, Type
from uuid import uuid4

from bpy import types as bpy_types

from ...core.base_type import BaseType
from ..annotations_internal import NodeSocketWrapper, NodeSocket
from .node_tree import NodeTree
from ...data.props_typed import WrappedPropertyDescriptor

__all__ = ['Node']



class Node(BaseType, bpy_types.Node):
    _node_tree_type: Type[NodeTree]
    _node_category: str
    _color_tag: str = 'NONE'

    @property
    def uid(self) -> str:
        return self.name

    @classmethod
    def poll(cls, node_tree: NodeTree) -> bool:
        if hasattr(cls, '_node_tree_type') and cls._node_tree_type is not None:
            return node_tree.bl_idname == cls._node_tree_type.bl_idname
        return False

    @property
    def node_tree(self) -> NodeTree:
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
        
        import bpy
        bpy.ops.node.translate_attach('INVOKE_DEFAULT', TRANSFORM_OT_translate={"value": (0.0, 0.0, 0.0)})

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

    def verify_link(self, link: bpy_types.NodeLink) -> bool:
        """Verify if the link is valid"""
        from_socket: NodeSocket = link.from_socket  # cast to ACK NodeSocket
        to_socket: NodeSocket = link.to_socket  # cast to ACK NodeSocket
        if from_socket.__class__ == to_socket.__class__:
            # Same socket type.
            return True
        from_socket_type: Type[Any] | None = from_socket.value_type
        to_socket_type: Type[Any] | None = to_socket.value_type
        assert from_socket_type is not None and to_socket_type is not None, f"Link {link} has invalid socket types: {from_socket_type} -> {to_socket_type}"
        '''if from_socket_type == to_socket_type:
            # Strictly equal types. (tho they could be vector/matrix with different lengths that should be casted)
            return True'''
        if to_socket.can_cast_from_socket(from_socket):
            return True
        if to_socket.can_cast_from_type(from_socket_type):  # NOTE: I have doubts about this one.
            return True
        if to_socket.can_cast_from_value(from_socket.value):
            return True
        return False

    def insert_link(self, link: bpy_types.NodeLink):
        """Handle creation of a link to or from the node

        :param link: Link, Node link that will be inserted
        :type link: 'bpy.types.NodeLink'
        """
        # This will be called for both nodes this link connects.
        # So we need to check only one of the nodes.
        if link.from_node == self:
            return
        if not self.verify_link(link):
            self.node_tree.tag_remove_link(link)
            return

    def get_dependent_nodes(self) -> List['Node']:
        """Get all nodes that depend on this node's outputs"""
        dependent_nodes = []
        for output in self.outputs:
            for link in output.links:
                if isinstance(link.to_node, Node) and link.to_node not in dependent_nodes:
                    dependent_nodes.append(link.to_node)
        return dependent_nodes

    def evaluate(self) -> None:
        """[NodeTree ONLY]
        Evaluate the node with the given input values.
        This method should be overridden by node subclasses.
        """
        pass

    def process(self) -> None:
        """[NodeTree ONLY]
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

    def draw_buttons(self, context: bpy_types.Context, layout: bpy_types.UILayout):
        """Draw the properties in the node layout"""
        props_to_draw: list[tuple[WrappedPropertyDescriptor, int]] = []
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, WrappedPropertyDescriptor):
                if value.is_node_drawable():
                    props_to_draw.append((value, value._draw_node_order))

        # print("Node.draw_buttons:", self.name, props_to_draw)

        for prop_wrapper, order in sorted(props_to_draw, key=lambda x: x[1]):
            prop_wrapper.draw_in_node_layout(layout, self, context)

    def draw_buttons_ext(self, context: bpy_types.Context, layout: bpy_types.UILayout):
        """Draw the properties in the sidebar layout"""
        props_to_draw: list[tuple[WrappedPropertyDescriptor, int]] = []
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, WrappedPropertyDescriptor):
                if value.is_drawable():
                    props_to_draw.append((value, value._draw_order))

        # print("Node.draw_buttons_ext:", self.name, props_to_draw)

        for prop_wrapper, order in sorted(props_to_draw, key=lambda x: x[1]):
            prop_wrapper.draw_in_layout(layout, self, context)
