from typing import Protocol, TypeVar, Set, Dict, Any, cast, Type
from types import new_class
import bpy
from bpy.types import Context, Event, Operator

# Protocol defining the required Blender operator interface
class OperatorProtocol(Protocol):
    bl_idname: str
    bl_label: str
    bl_options: Set[str]
    
    def execute(self, context: Context) -> Set[str]: ...
    def invoke(self, context: Context, event: Event) -> Set[str]: ...
    def modal(self, context: Context, event: Event) -> Set[str]: ...
    def draw(self, context: Context) -> None: ...
    def poll(cls, context: Context) -> bool: ...
    def cancel(self, context: Context) -> None: ...

# Type variable constrained to classes that implement OperatorProtocol
T = TypeVar('T', bound=Type[OperatorProtocol])

class BlenderPropertyDescriptor:
    """Base class for Blender property descriptors"""
    def copy(self) -> 'BlenderPropertyDescriptor':
        return self.__class__()
    
    def initialize(self, cls: Any, name: str) -> None:
        pass

def RegisterOperator(cls: T) -> T:
    """
    Decorator that registers a class as a Blender operator.
    Returns the newly created operator class with proper type hints.
    
    Args:
        cls: The class to be registered as an operator
        
    Returns:
        The registered operator class with proper type hints
    
    Example:
        @RegisterOperator
        class MyOperator:
            bl_idname = "object.my_operator"
            bl_label = "My Operator"
            bl_options = {'REGISTER', 'UNDO'}
            
            def execute(self, context: Context) -> Set[str]:
                return {'FINISHED'}
    """
    # Create the bases tuple
    bases = (cls, bpy.types.Operator)
    
    # Get namespace from the original class
    namespace = dict(cls.__dict__)
    
    # Create new class with proper metaclass
    new_cls = new_class(
        cls.__name__,
        bases,
        {},
        lambda ns: ns.update(namespace)
    )
    
    # Ensure annotations exist
    if not hasattr(new_cls, '__annotations__'):
        new_cls.__annotations__ = {}
    
    # Initialize property descriptors
    for name, value in cls.__dict__.items():
        if isinstance(value, BlenderPropertyDescriptor):
            new_descriptor = value.copy()
            new_descriptor.initialize(new_cls, name)
            setattr(new_cls, name, new_descriptor)
    
    # Register with Blender
    bpy.utils.register_class(new_cls)
    
    # Cast to preserve type information
    return cast(T, new_cls)

# Example usage with full type hinting
@RegisterOperator
class ExampleOperator:
    bl_idname: str = "object.example_operator"
    bl_label: str = "Example Operator"
    bl_options: Set[str] = {'REGISTER', 'UNDO'}
    
    def execute
    
    def invoke(self, context: Context, event: Event) -> Set[str]:
        return {'RUNNING_MODAL'}
    
    def modal(self, context: Context, event: Event) -> Set[str]:
        if event.type == 'LEFTMOUSE':
            return {'FINISHED'}
        return {'RUNNING_MODAL'}
    
    def draw(self, context: Context) -> None:
        pass
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        return context.active_object is not None
    
    def cancel(self, context: Context) -> None:
        pass