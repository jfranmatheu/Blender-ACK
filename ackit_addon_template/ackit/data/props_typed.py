from enum import Enum
from math import pi
from typing import Any, Callable, Type, TypeVar, Union, Generic, Optional

from bpy.props import *
from bpy import types as btypes
from mathutils import Color, Vector, Matrix

from ..utils.callback import CallbackList # Check if utils/callback.py exists


__all__ = [
    'WrappedPropertyDescriptor',
    'WrappedTypedPropertyTypes'
]


T = TypeVar('T')

class WrappedPropertyDescriptor(Generic[T]):
    """
    A property descriptor that combines typing support with wrapped property functionality.
    Can be used both as a descriptor and for registration through annotations.
    """
    def __init__(self, property_type: Callable, **kwargs):
        self.property_type = property_type
        self.kwargs = kwargs
        self._update_callback_set = CallbackList()
        self._prop_name = None
        self._owner_cls = None
        self._flags: set[str] = set()
        self._draw_order = -1
        self._draw_poll = None
        self._draw_kwargs = {}
        self._draw_node_order = -1
        self._draw_node_poll = None
        self._draw_node_kwargs = {}

    def __set_name__(self, owner, name):
        """Called when the descriptor is assigned to the owner class"""
        self._prop_name = name
        self._owner_cls = owner
        if not hasattr(owner, '__annotations__'):
            owner.__annotations__ = {}

    def __get__(self, instance, owner) -> T:
        if instance is None:
            return self
        # Access the underlying Blender property directly using the name
        try:
            return getattr(instance, self._prop_name)
        except AttributeError:
            # Fallback or raise error if property doesn't exist on instance yet
            # This might happen before registration or if used incorrectly
            # For now, returning self might be suitable for inspection purposes
            # Consider raising a more specific error if needed.
            # raise AttributeError(f"Property '{self._prop_name}' not found on instance {instance}")
            return self # Or None, or raise error

    def add_update_callback(self, callback: Callable) -> 'WrappedPropertyDescriptor[T]':
        """Add an update callback"""
        if not callable(callback):
            raise TypeError("callback: expected a callable")
        self._update_callback_set.add_callback(callback)
        return self

    def create_property(self, idname: str | None = None, owner_cls: Type = None) -> Any:
        """Create the actual bpy property during registration"""
        owner_cls = owner_cls or self._owner_cls
        prop_name = idname or self._prop_name
        if not prop_name:
             raise ValueError("Property name must be set either via __set_name__ or provided to create_property")

        kwargs = self.kwargs.copy()
        
        # Combine descriptor's update callbacks with any provided in kwargs
        explicit_update = kwargs.pop('update', None)
        if explicit_update and not callable(explicit_update):
            raise TypeError("update keyword: expected a callable")

        # Add node/socket specific callbacks automatically if applicable
        # Make sure Node and NodeSocket are imported correctly
        try:
            from ..ne.btypes import Node, NodeSocket
            if owner_cls is not None:
                if issubclass(owner_cls, NodeSocket):
                    self.add_update_callback(lambda socket, context: socket.on_property_update(context))
                elif issubclass(owner_cls, Node):
                     # Pass prop_name to node's update handler
                    self.add_update_callback(lambda node, context: node.on_property_update(context, prop_name))
        except ImportError:
            # Handle cases where Node/NodeSocket might not be relevant or importable
            pass 

        # Add explicitly passed update function last
        if explicit_update:
            self.add_update_callback(explicit_update)

        # Set the final update function if callbacks exist
        if self._update_callback_set:
            # Create a unique update function name based on the property name
            update_func_name = f"_ack_{prop_name}_update"
            # Define the actual update function
            def generated_update_func(instance, context):
                self._update_callback_set.call_callbacks(instance, context)
            # Assign it to the owner class if possible (for introspection)
            if owner_cls and owner_cls.__module__ != 'bpy_types':
                 setattr(owner_cls, update_func_name, generated_update_func)
            # Set the update kwarg
            kwargs['update'] = generated_update_func # Use the function directly

        prop = self.property_type(**kwargs)

        # Assign the property to the owner class
        if owner_cls is not None:
            if owner_cls.__module__ == 'bpy_types':
                # Registering directly to a Blender type
                setattr(owner_cls, prop_name, prop)
            else:
                # Registering via annotation on a custom class (PropertyGroup, Operator, etc.)
                owner_cls.__annotations__[prop_name] = prop
        return prop

    # Property attribute setters with proper return typing
    def min(self, value: Union[int, float]) -> 'WrappedPropertyDescriptor[T]':
        self.kwargs['min'] = value
        return self

    def max(self, value: Union[int, float]) -> 'WrappedPropertyDescriptor[T]':
        self.kwargs['max'] = value
        return self

    def default(self, value: T) -> 'WrappedPropertyDescriptor[T]':
        self.kwargs['default'] = value
        return self

    def description(self, text: str) -> 'WrappedPropertyDescriptor[T]':
        self.kwargs['description'] = text
        return self

    def draw_in_layout(self, layout: 'btypes.UILayout', prop_owner: Any, poll_context: bpy.types.Context | None = None):
        """Draw the property in a layout"""
        # Use the internal name derived from __set_name__
        if poll_context is not None and self._draw_poll is not None and callable(self._draw_poll):
            if not self._draw_poll(prop_owner, poll_context):
                return
        layout.prop(prop_owner, self._prop_name, **self._draw_kwargs)

    def draw_in_node_layout(self, layout: 'btypes.UILayout', prop_owner: Any, poll_context: bpy.types.Context | None = None):
        """Draw the property in a node layout"""
        # Use the internal name derived from __set_name__
        if poll_context is not None and self._draw_node_poll is not None and callable(self._draw_node_poll):
            if not self._draw_node_poll(prop_owner, poll_context):
                return
        layout.prop(prop_owner, self._prop_name, **self._draw_node_kwargs)

    def has_flag(self, flag: str) -> bool:
        """Check if the property has a flag"""
        return flag in self._flags

    def is_drawable(self) -> bool:
        """Check if the property is drawable"""
        return 'DRAW_IN_LAYOUT' in self._flags
    
    def is_node_drawable(self) -> bool:
        """Check if the property is drawable in a node layout"""
        return 'DRAW_IN_NODE_LAYOUT' in self._flags

    def tag_drawable(self, order: int = -1, poll: Optional[Callable] = None, **draw_kwargs) -> 'WrappedPropertyDescriptor[T]':
        """Tag the property to be drawn in a layout (wether it is a node, a socket, a panel, an operator, etc.)"""
        self._flags.add('DRAW_IN_LAYOUT')
        self._draw_order = order
        self._draw_kwargs = draw_kwargs
        self._draw_poll = poll
        return self

    def tag_node_drawable(self, order: int = -1, poll: Optional[Callable] = None, **draw_kwargs) -> 'WrappedPropertyDescriptor[T]':
        """Tag the property to be drawn in a node layout"""
        self._flags.add('DRAW_IN_NODE_LAYOUT')
        self._draw_node_order = order
        self._draw_node_kwargs = draw_kwargs
        self._draw_node_poll = poll
        return self


class WrappedTypedPropertyTypes:
    """Factory for creating wrapped properties with proper typing.
        Use them in Operators and Nodes. """

    @classmethod
    def Float(cls, name: str = '', **kwargs) -> WrappedPropertyDescriptor[float]:
        return WrappedPropertyDescriptor[float](FloatProperty, name=name, **kwargs)

    @staticmethod
    def Int(name: str = '', **kwargs) -> WrappedPropertyDescriptor[int]:
        return WrappedPropertyDescriptor[int](IntProperty, name=name, **kwargs)

    @staticmethod
    def Bool(name: str = '', **kwargs) -> WrappedPropertyDescriptor[bool]:
        return WrappedPropertyDescriptor[bool](BoolProperty, name=name, **kwargs)

    @staticmethod
    def String(name: str = '', **kwargs) -> WrappedPropertyDescriptor[str]:
        return WrappedPropertyDescriptor[str](StringProperty, name=name, **kwargs)

    @staticmethod
    def DirPath(name: str = '', **kwargs) -> WrappedPropertyDescriptor[str]:
        return WrappedPropertyDescriptor[str](StringProperty, name=name, subtype='DIR_PATH', **kwargs)

    @staticmethod
    def FilePath(name: str = '', **kwargs) -> WrappedPropertyDescriptor[str]:
        return WrappedPropertyDescriptor[str](StringProperty, name=name, subtype='FILE_PATH', **kwargs)

    @staticmethod
    def FileName(name: str = '', **kwargs) -> WrappedPropertyDescriptor[str]:
        return WrappedPropertyDescriptor[str](StringProperty, name=name, subtype='FILE_NAME', **kwargs)

    @staticmethod
    def Enum(name: str = '', items=[], multiple_selection: bool = False, **kwargs) -> WrappedPropertyDescriptor[Union[str, set[str]]]:
        prop_type = EnumProperty
        return_type = str
        if multiple_selection:
            if 'options' not in kwargs:
                kwargs['options'] = {'ENUM_FLAG'}
            else:
                kwargs['options'].add('ENUM_FLAG')
            return_type = set[str]
        return WrappedPropertyDescriptor[return_type](prop_type, name=name, items=items, **kwargs)

    @classmethod
    def Vector(cls, name: str = '', size: int = 3, type: Union[Type[float], Type[int], Type[bool]] = float, **kwargs) -> WrappedPropertyDescriptor[Vector]: # Use Vector for type hint
        if 'default' not in kwargs:
            kwargs['default'] = tuple([0] * size) # Use tuple for default
        if type == float:
            property_type = FloatVectorProperty
        elif type == int:
            property_type = IntVectorProperty
        elif type == bool:
            property_type = BoolVectorProperty
        else:
            raise ValueError(f"Unsupported vector type: {type}")
        return WrappedPropertyDescriptor[Vector](property_type, name=name, size=size, **kwargs)

    @classmethod
    def Color(cls, name: str = '', use_alpha: bool = False, **kwargs) -> WrappedPropertyDescriptor[Color]: # Use Color for type hint
        size = 4 if use_alpha else 3
        if 'default' not in kwargs:
            kwargs['default'] = tuple([0.0] * size) # Use tuple for default
        return WrappedPropertyDescriptor[Color](FloatVectorProperty, name=name, size=size, min=0.0, max=1.0, subtype='COLOR', **kwargs)

    @classmethod
    def Matrix3x3(cls, name: str = '', **kwargs) -> WrappedPropertyDescriptor[Matrix]:
        """Create a 3x3 Matrix property."""
        if 'default' not in kwargs:
            kwargs['default'] = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        return WrappedPropertyDescriptor[Matrix](FloatVectorProperty, name=name, size=(3, 3), subtype='MATRIX', **kwargs)

    @classmethod
    def Matrix4x4(cls, name: str = '', **kwargs) -> WrappedPropertyDescriptor[Matrix]:
        """Create a 4x4 Matrix property."""
        if 'default' not in kwargs:
            kwargs['default'] = ((1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 0.0), (0.0, 0.0, 1.0, 0.0), (0.0, 0.0, 0.0, 1.0))
        return WrappedPropertyDescriptor[Matrix](FloatVectorProperty, name=name, size=(4, 4), subtype='MATRIX', **kwargs)

    # Preset types
    @classmethod
    def Angle(cls, name: str = '', default: float = 0, **kwargs) -> WrappedPropertyDescriptor[float]:
        return cls.Float(name=name, default=default, subtype='ANGLE', unit='ROTATION', **kwargs)

    @classmethod
    def Factor(cls, name: str = '', default: float = 0.0, **kwargs) -> WrappedPropertyDescriptor[float]:
        return cls.Float(name=name, default=default, **kwargs).min(0.0).max(1.0)

    # Pointer types nested under Data for organization
    class Data:
        @staticmethod
        def Pointer(name: str = '', type: Type[btypes.ID] = btypes.Object, **kwargs) -> WrappedPropertyDescriptor[btypes.ID]:
            return WrappedPropertyDescriptor[type](PointerProperty, name=name, type=type, **kwargs)
        
        @staticmethod
        def Object(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Object]:
            return WrappedPropertyDescriptor[btypes.Object](PointerProperty, name=name, type=btypes.Object, **kwargs)

        @staticmethod
        def Material(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Material]:
            return WrappedPropertyDescriptor[btypes.Material](PointerProperty, name=name, type=btypes.Material, **kwargs)

        @staticmethod
        def Mesh(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Mesh]:
            return WrappedPropertyDescriptor[btypes.Mesh](PointerProperty, name=name, type=btypes.Mesh, **kwargs)

        @staticmethod
        def Texture(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Texture]:
            return WrappedPropertyDescriptor[btypes.Texture](PointerProperty, name=name, type=btypes.Texture, **kwargs)

        @staticmethod
        def Collection(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Collection]:
            if type is None:
                raise ValueError("CollectionProperty requires a 'type' argument (a PropertyGroup subclass).")
            return WrappedPropertyDescriptor[btypes.Collection](PointerProperty, name=name, type=btypes.Collection, **kwargs)

        @staticmethod
        def Scene(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Scene]:
            return WrappedPropertyDescriptor[btypes.Scene](PointerProperty, name=name, type=btypes.Scene, **kwargs)

        @staticmethod
        def World(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.World]:
            return WrappedPropertyDescriptor[btypes.World](PointerProperty, name=name, type=btypes.World, **kwargs)

        @staticmethod
        def Image(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Image]:
            return WrappedPropertyDescriptor[btypes.Image](PointerProperty, name=name, type=btypes.Image, **kwargs)

        @staticmethod
        def Armature(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Armature]:
            return WrappedPropertyDescriptor[btypes.Armature](PointerProperty, name=name, type=btypes.Armature, **kwargs)

        @staticmethod
        def Action(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Action]:
            return WrappedPropertyDescriptor[btypes.Action](PointerProperty, name=name, type=btypes.Action, **kwargs)

        @staticmethod
        def Text(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Text]:
            return WrappedPropertyDescriptor[btypes.Text](PointerProperty, name=name, type=btypes.Text, **kwargs)

        @staticmethod
        def Light(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Light]:
            return WrappedPropertyDescriptor[btypes.Light](PointerProperty, name=name, type=btypes.Light, **kwargs)

        @staticmethod
        def Curve(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Curve]:
            return WrappedPropertyDescriptor[btypes.Curve](PointerProperty, name=name, type=btypes.Curve, **kwargs)

        @staticmethod
        def Camera(name: str = '', **kwargs) -> WrappedPropertyDescriptor[btypes.Camera]:
            return WrappedPropertyDescriptor[btypes.Camera](PointerProperty, name=name, type=btypes.Camera, **kwargs)
