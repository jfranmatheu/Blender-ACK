from typing import Any, Callable, Optional, Type, TypeVar, Union, Generic
from enum import Enum
from functools import partial

from bpy.props import *
from mathutils import Matrix

from ..property import PropertyTypes
from ...reg_types.nodes import Node, NodeSocket
from ....utils.callback import CallbackList


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

    def __set_name__(self, owner, name):
        """Called when the descriptor is assigned to the owner class"""
        self._prop_name = name
        if not hasattr(owner, '__annotations__'):
            owner.__annotations__ = {}
        self.create_property(name, owner)

    def __get__(self, instance, owner) -> T:
        if instance is None:
            return self
        return getattr(instance, self._prop_name)

    def add_update_callback(self, callback: Callable) -> 'WrappedPropertyDescriptor[T]':
        """Add an update callback"""
        if not callable(callback):
            raise TypeError("callback: expected a callable")
        self._update_callback_set.add_callback(callback)
        return self

    def create_property(self, idname: str | None = None, owner_cls: Type = None) -> Any:
        """Create the actual bpy property during registration"""
        kwargs = self.kwargs.copy()

        # Handle update callback differently
        if 'update' in kwargs:
            update_func = kwargs.pop('update')
            if not callable(update_func):
                raise TypeError("update keyword: expected a callable")
            self.add_update_callback(update_func)

        # Add node/socket specific callbacks
        if owner_cls is not None:
            if issubclass(owner_cls, NodeSocket):
                self.add_update_callback(lambda socket, context: socket.on_property_update(context))
            elif issubclass(owner_cls, Node):
                self.add_update_callback(lambda node, context: node.on_property_update(context, idname))

        # Handle update callback
        if self._update_callback_set:
            kwargs['update'] = lambda instance, context: self._update_callback_set.call_callbacks(instance, context)

        prop = self.property_type(**kwargs)
        if owner_cls is not None:
            if owner_cls.__module__ == 'bpy_types':
                # BPY type.
                setattr(owner_cls, idname, prop)
            else:
                # ACK type.
                owner_cls.__annotations__[idname] = prop
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

    def draw_in_layout(self, layout: 'bpy.types.UILayout', prop_owner: Any):
        """Draw the property in a layout"""
        layout.prop(prop_owner, self._prop_name)

class WrappedTypedPropertyTypes:
    """Factory for creating wrapped properties with proper typing"""
    
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
    def Enum(name: str = '', items=[], multiple_selection: bool = False, **kwargs) -> WrappedPropertyDescriptor[str]:
        if multiple_selection:
            if 'options' not in kwargs:
                kwargs['options'] = {'ENUM_FLAG'}
            else:
                kwargs['options'].add('ENUM_FLAG')
        return WrappedPropertyDescriptor[str](EnumProperty, name=name, items=items, **kwargs)

    @classmethod
    def Vector(cls, name: str = '', size: int = 3, type: Union[Type[float], Type[int], Type[bool]] = float, **kwargs) -> WrappedPropertyDescriptor[tuple[float, ...]]:
        if 'default' not in kwargs:
            kwargs['default'] = [0] * size
        if type == float:
            property_type = FloatVectorProperty
        elif type == int:
            property_type = IntVectorProperty
        elif type == bool:
            property_type = BoolVectorProperty
        else:
            raise ValueError(f"Unsupported vector type: {type}")
        return WrappedPropertyDescriptor[tuple[float, ...]](property_type, name=name, size=size, **kwargs)

    # Preset types
    @classmethod
    def Angle(cls, name: str = '', default: float = 0, **kwargs) -> WrappedPropertyDescriptor[float]:
        return cls.Float(name=name, default=default, subtype='ANGLE', unit='ROTATION', **kwargs)

    @classmethod
    def Factor(cls, name: str = '', default: float = 0.0, **kwargs) -> WrappedPropertyDescriptor[float]:
        return cls.Float(name=name, default=default, **kwargs).min(0.0).max(1.0)
