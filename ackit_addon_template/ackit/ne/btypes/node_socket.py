import typing
import uuid
from typing import Any, TypeVar, Generic, Optional, cast, Union, Type, Dict, Set, ClassVar, Tuple, Callable

from bpy import types as bpy_types

from ...core.base_type import BaseType
from ...data.props import PropertyTypes as Prop
from ..socket_casting import SocketCast


__all__ = ['NodeSocket']


T = TypeVar('T')

cached_node_cls_type: Dict[Type['NodeSocket'], Type] = {}

# Helper functions (consider moving to a utils module later)
def _get_generic_type(instance: 'NodeSocket') -> Type[Any] | None:
    """Attempts to get the generic type T from a NodeSocket subclass instance."""
    if instance.__class__ in cached_node_cls_type:
        return cached_node_cls_type[instance.__class__]
    # Check __orig_bases__ first (standard for generic subclasses)
    for base in getattr(instance.__class__, '__orig_bases__', []):
        origin = typing.get_origin(base)
        if origin is NodeSocket:
            args = typing.get_args(base)
            if args:
                cached_node_cls_type[instance.__class__] = args[0]
                return args[0]
    # Fallback: Check direct annotations if it's not a direct subclass maybe?
    # This part is less reliable for complex hierarchies
    # For now, rely on explicit generic subclassing like NodeSocket[dict]
    return None

def _get_default_value(typ):
    """Returns a default value for basic Python types supported by custom properties."""
    if typ is dict:
        return {}
    elif typ is list:
        # Note: Blender custom props don't directly support lists, often stored as IDPropertyArray or serialized.
        # Returning [] might be okay for transient use, but saving might fail.
        print("Warning: List type used for custom property socket. Behavior might be limited.")
        return []
    elif typ is str:
        return ""
    elif typ is int:
        return 0
    elif typ is float:
        return 0.0
    elif typ is bool:
        return False
    elif typ is bytes:
        return b''
    elif typ is type(None):
        return None # Allow None type
    # Add more basic types if needed
    else:
        # Allow ID property types like Object, Material etc.? For now, restrict.
        # Check if typ corresponds to a bpy.types.ID subclass?
        origin = typing.get_origin(typ)
        args = typing.get_args(typ)
        # Handle basic generic aliases like tuple[float, float]
        if origin is tuple and args:
            try:
                # Return tuple of defaults for each type in the tuple args
                return tuple(_get_default_value(arg) for arg in args)
            except TypeError:
                raise TypeError(f"Unsupported type within tuple for custom property initialization: {typ}")
        elif origin is None and isinstance(typ, type):
            # Maybe it's a simple class? Try instantiating? Risky.
            # For now, only support explicitly listed types and basic generics.
            pass # Fall through to the error
            return None
        raise TypeError(f"Unsupported type for custom property initialization: {typ}")


class NodeSocket(BaseType, bpy_types.NodeSocket, Generic[T]):
    label: str
    color: tuple[float, float, float, float] = (.5, .5, .5, 1.0)
    property_name: str = 'property'
    use_custom_property: bool = False
    # Casting.
    property_cast: Callable[[Any], Any] | None = None
    cast_from_socket: ClassVar[Dict[str, Callable[[Any], Any]]] = {}  # Cast from socket type.
    cast_from_types: ClassVar[Dict[Type, Callable[[Any], Any]]] = {}  # Cast from defined property value type.
    # Extended properties
    uid: Prop.STRING(default='', options={'HIDDEN'})
    block_property_update: Prop.BOOL(default=False, options={'HIDDEN', 'SKIP_SAVE'})

    @property
    def is_input(self) -> bool:
        """ Gets whether the socket is an input socket. """
        return not self.is_output

    @property
    def value(self) -> T:
        """ Gets the value of the socket. """
        return self.get_value()

    @value.setter
    def value(self, value: T):
        """ Sets the value of the socket. """
        self.set_value(value)

    @property
    def value_type(self) -> Union[Type[T], None]:
        """ Gets the type of the socket value. """
        return _get_generic_type(self)

    def get_value(self) -> Union[T, None]:
        """ Gets the value of the socket. """
        if self.is_input:
            if self.is_linked:
                # TODO: support multi-input sockets (value retrieval from multiple links).
                from_socket: NodeSocket = self.links[0].from_socket
                from_value = from_socket.get_value()
                if from_value is None:
                    return None
                if from_socket.__class__.__name__ == self.__class__.__name__:
                    return from_value
                # NOTE: I have doubts about 'value_type' comparison.
                if self.value_type == from_socket.value_type or self.value_type == type(from_value): # type(from_value):
                    return from_value
                if socket_cast := self.cast_from_socket.get(from_socket.__class__.__name__, None):
                    return socket_cast(from_value)
                if socket_cast := self.cast_from_types.get(type(from_value), None):
                    return socket_cast(from_value)
                raise ValueError(f"Sockets are incompatible: {from_socket.__class__.__name__} -> {self.__class__.__name__}")
            if self.is_multi_input:
                # Multi-input sockets have no value.
                # They take its values from the links.
                return None
        if self.use_custom_property:
            if self.property_name not in self:
                return None
            val = self[self.property_name]
        else:
            val = getattr(self, self.property_name)
        if self.property_cast is not None:
            # NOTE: Some properties needs to be casted to the correct type, for example:
            # - Python lists are stored as IDPropertyArray, we need to cast it to a tuple or list, same for Python dictionaries.
            # - Vector properties (and RGBA color) are interpreted as 'bpy_prop_array', so we need to cast it to a tuple.
            val = self.property_cast(val)
        return val

    def set_value(self, value: T):
        """ Sets the value of the socket, if possible (based on the `cast` class variable). """
        if self.use_custom_property:
            self[self.property_name] = value
        else:
            setattr(self, self.property_name, value)

    def set_value_with_block_update(self, value):
        """ Sets the value of the socket, blocking property updates. """
        self.block_property_update = True
        self.set_value(value)
        self.block_property_update = False

    def can_cast_from_socket(self, socket: 'NodeSocket') -> bool:
        """ Checks if a socket can be cast to the type of the socket. """
        return self.cast_from_socket.get(socket.__class__.__name__, None) is not None

    def can_cast_from_type(self, value_type: Type[Any]) -> bool:
        """ Checks if a type can be cast to the type of the socket. """
        return self.cast_from_types.get(value_type, None) is not None

    def can_cast_from_value(self, value: Any) -> bool:
        """ Checks if a value can be cast to the type of the socket. """
        return self.cast_from_types.get(type(value), None) is not None

    def on_property_update(self, context: bpy_types.Context):
        """ Called when the property of the socket is updated. """
        if not self.is_input:
            return
        print(f"NodeSocket.on_property_update: {self.property_name}")
        if self.block_property_update:
            return
        self.block_property_update = True
        self.node.process()
        self.block_property_update = False

    def init(self, node: bpy_types.Node):
        """ Called when the socket is created for the first time. """
        self.uid = str(uuid.uuid4())
        if self.use_custom_property:
            try:
                typ = _get_generic_type(self)
                if typ is None:
                    raise ValueError(f"No generic type found for socket {self.name}")
                default_value = _get_default_value(typ)
                if default_value is None:
                    raise ValueError(f"No default value found for socket {self.name}")
                self.set_value(default_value)
            except Exception as e:
                print(f"Error setting default value for custom property {self.property_name}: {e}")

    def get_links(self):
        """ Gets the links of the socket. """
        return self.links  # if self.is_linked else []
        # return (*self.links, *self.portal_links) if self.use_portal_links and self.is_linked else self.links if not self.use_portal_links and self.is_linked else self.portal_links if self.use_portal_links else []

    def draw_color(self, context: bpy_types.Context, node: bpy_types.Node) -> tuple[float, float, float, float]:
        """ Draws the color of the socket. """
        # print(node, self, self.name, self.property_name, self.property, node.tree_prop_idname)
        return self.color

    def draw(self, context: bpy_types.Context, layout: bpy_types.UILayout, node: bpy_types.Node, text: str):
        """ Draws the socket layout. """
        if not self.use_custom_property and ((self.is_input and not self.is_linked) or (self.is_output and len(self.node.inputs) == 0)):
            show_label = not (self.is_output and len(self.node.outputs) == 1 and len(self.node.inputs) == 0)
            layout.prop(self, self.property_name, text=self.name if show_label else '')
        else:
            layout.label(text=self.name)
