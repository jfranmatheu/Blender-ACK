import bpy
from typing import Dict, Any
import mathutils

from ...data.props_typed import WrappedPropertyDescriptor


class BaseNode:
    bl_idname: str
    name: str
    location: mathutils.Vector

    # Change type hint to bpy.types.Node, rely on runtime isinstance check inside
    def _get_serializable_properties(self) -> Dict[str, Any]:
        """
        Extracts serializable properties and their values from an ACK node instance.
        """
        props = {}

        # Iterate through the actual class dictionary
        for prop_name, descriptor in self.__class__.__dict__.items():
            # Runtime check using the potentially imported actual class
            if isinstance(descriptor, WrappedPropertyDescriptor):
                try:
                    # Get the value from the node instance
                    value = getattr(self, prop_name)
                    # Handle specific types
                    if isinstance(value, bpy.types.ID):
                        props[prop_name] = value.name if value else None
                    elif isinstance(value, mathutils.Matrix):
                        # Convert Matrix to tuple of tuples (rows)
                        props[prop_name] = tuple(tuple(row) for row in value)
                    elif isinstance(value, (mathutils.Vector, mathutils.Color, bpy.types.bpy_prop_array)):
                        # These are directly iterable into tuples
                        props[prop_name] = tuple(value)
                    else:
                        # Attempt to serialize other types directly
                        props[prop_name] = value
                except Exception as e: # Catch broader exceptions during getattr/processing
                    print(f"Warning: Could not get or process attribute '{prop_name}' from node '{self.name}': {e}")
        return props

    def serialize(self) -> Dict[str, Any]:
        """Serializes basic node info and properties."""
        if not hasattr(self, 'name') or not hasattr(self, 'bl_idname'):
                raise ValueError(f"Node {self} cannot be serialized: missing name or bl_idname")
        return {
            "id": self.name,
            "type": self.bl_idname,
            "location": tuple(self.location),
            "properties": self._get_serializable_properties(),
        }
