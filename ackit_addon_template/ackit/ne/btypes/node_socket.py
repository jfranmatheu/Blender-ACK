import typing
from typing import Any, TypeVar, Generic, Optional, cast

from bpy import types as bpy_types
from bpy import props as bpy_props # Import bpy.props

from ...core.base_type import BaseType


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

    # Define block_property_update directly as a class attribute without type hint
    block_property_update = bpy_props.BoolProperty(
        default=False, 
        options={'HIDDEN', 'SKIP_SAVE'},
        description="Internal flag to prevent recursive updates"
    )

    @property
    def is_input(self):
        return not self.is_output

    @property
    def value(self) -> Optional[T]:
        return self.get_value()

    @value.setter
    def value(self, value: Optional[T]):
        self.set_value(value)

    def get_value(self) -> Optional[T]:
        if self.is_input:
            if self.is_linked:
                from_socket: 'NodeSocket' = self.links[0].from_socket
                return from_socket.get_value()
        
        if self.use_custom_property:
            if self.property_name in self:
                stored_value = self[self.property_name]
                # Optional: Add stricter type check here if needed
                return stored_value
            else:
                # Initialize custom property
                expected_type = _get_generic_type(self)
                if expected_type is None:
                    print(f"Error: Could not determine generic type T for socket {self.name}. Cannot initialize custom property.")
                    return None
                try:
                    default_value = _get_default_value(expected_type)
                    print(f"Initializing custom property '{self.property_name}' on {self.name} with default: {default_value}")
                    self[self.property_name] = default_value
                    # Use cast to tell the linter we believe the type is correct
                    return cast(Optional[T], default_value)
                except TypeError as e:
                    print(f"Error initializing custom property '{self.property_name}' on socket {self.name}: {e}")
                    return None
        
        # Fallback for standard bpy.props based sockets
        if hasattr(self, self.property_name):
            # getattr might return something not matching T, but that's inherent
            return getattr(self, self.property_name)
        else:
            print(f"Warning: Property '{self.property_name}' not found on socket {self.name}")
            return None

    def set_value(self, value: Optional[T]):
        if self.use_custom_property:
            expected_type = _get_generic_type(self)
            is_any_type = expected_type is Any
            allow_none = expected_type is type(None) or is_any_type
            type_mismatch = False
            
            if expected_type and not is_any_type and not (allow_none and value is None):
                # Get the origin type (e.g., list for list[str], tuple for tuple[int, int])
                origin_type = typing.get_origin(expected_type) or expected_type
                # Check if origin_type is suitable for isinstance (must be a class)
                if isinstance(origin_type, type):
                    if not isinstance(value, origin_type):
                        # Allow int to float implicit conversion
                        if not (origin_type is float and isinstance(value, int)):
                            type_mismatch = True
                else:
                    # Origin is not a simple type (e.g., Union, Callable), skip isinstance check
                    # More complex validation could be added here if needed.
                    print(f"Skipping isinstance check for complex type: {expected_type}")
                    return
            
            if type_mismatch:
                print(f"Warning: Type mismatch setting custom property '{self.property_name}' on {self.name}. Expected {expected_type} (origin: {origin_type}), got {type(value)}.)")
                return # Prevent setting value of wrong type
            
            # Set the value if checks pass
            self[self.property_name] = value
        elif hasattr(self, self.property_name):
            # Standard property handling
            try:
                setattr(self, self.property_name, value)
            except TypeError as e:
                print(f"Error setting property '{self.property_name}' on socket {self.name}: {e}")
                # Potentially handle specific type errors (e.g., assigning string to float prop)
        else:
             print(f"Warning: Property '{self.property_name}' not found on socket {self.name} during set_value")

    def set_value_with_block_update(self, value):
        # Temporarily set the flag to prevent update loops
        self.block_property_update = True 
        try:
            self.set_value(value)
        finally:
            # Ensure the flag is reset even if set_value fails
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
        return self.links if self.is_linked else []
        # return (*self.links, *self.portal_links) if self.use_portal_links and self.is_linked else self.links if not self.use_portal_links and self.is_linked else self.portal_links if self.use_portal_links else []

    def draw_color(self, context: bpy_types.Context, node: bpy_types.Node) -> tuple[float, float, float, float]: # Fix hint
        # print(node, self, self.name, self.property_name, self.property, node.tree_prop_idname)
        return self.color
    
    def draw(self, context: bpy_types.Context, layout: bpy_types.UILayout, node: bpy_types.Node, text: str):
        if self.use_custom_property or (self.is_output and self.is_linked):
            layout.label(text=self.name)
        else:
            layout.prop(self, self.property_name, text=self.name)
