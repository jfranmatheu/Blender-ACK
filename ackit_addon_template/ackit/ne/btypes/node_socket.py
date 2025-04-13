import typing
from typing import Any, TypeVar, Generic, Optional, cast

from bpy import types as bpy_types

from ...core.base_type import BaseType
from ...data.props import PropertyTypes as Prop


__all__ = ['NodeSocket']


T = TypeVar('T')



# Helper functions (consider moving to a utils module later)
def _get_generic_type(instance):
    """Attempts to get the generic type T from a NodeSocket subclass instance."""
    # Check __orig_bases__ first (standard for generic subclasses)
    for base in getattr(instance.__class__, '__orig_bases__', []):
        origin = typing.get_origin(base)
        if origin is NodeSocket:
            args = typing.get_args(base)
            if args:
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

    # Extended properties
    block_property_update: Prop.BOOL(default=False, options={'HIDDEN', 'SKIP_SAVE'})

    @property
    def is_input(self):
        return not self.is_output

    @property
    def value(self) -> T:
        return self.get_value()

    @value.setter
    def value(self, value: T):
        self.set_value(value)

    def get_value(self) -> T:
        if self.is_input:
            if self.is_linked:
                # TODO: support multi-input sockets.
                from_socket: NodeSocket = self.links[0].from_socket
                return from_socket.get_value()
        if self.use_custom_property:
            if self.property_name in self:
                return self[self.property_name]
            return None
        return getattr(self, self.property_name)

    def set_value(self, value: T):
        if self.use_custom_property:
            self[self.property_name] = value
        else:
            setattr(self, self.property_name, value)

    def set_value_with_block_update(self, value):
        self.block_property_update = True
        self.set_value(value)
        self.block_property_update = False

    def on_property_update(self, context: bpy_types.Context):
        if not self.is_input:
            return
        print(f"NodeSocket.on_property_update: {self.property_name}")
        if self.block_property_update:
            return
        self.block_property_update = True
        self.node.process()
        self.block_property_update = False

    def get_links(self):
        return self.links  # if self.is_linked else []
        # return (*self.links, *self.portal_links) if self.use_portal_links and self.is_linked else self.links if not self.use_portal_links and self.is_linked else self.portal_links if self.use_portal_links else []

    def draw_color(self, context: bpy_types.Context, node: bpy_types.Node) -> tuple[float, float, float, float]:
        # print(node, self, self.name, self.property_name, self.property, node.tree_prop_idname)
        return self.color

    def draw(self, context: bpy_types.Context, layout: bpy_types.UILayout, node: bpy_types.Node, text: str):
        if not self.use_custom_property and ((self.is_input and not self.is_linked) or (self.is_output and len(self.node.inputs) == 0)):
            layout.prop(self, self.property_name, text=self.name)
        else:
            layout.label(text=self.name)
