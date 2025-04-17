from typing import Type
import bpy

from ...ackit import ACK

__all__ = [
    'ElementSocket',
]

# Socket for signaling connection between Elements/Layouts (Child -> Parent)
# Does not pass data via the 'value' property.
class ElementSocket(ACK.NE.SocketExec[None]): # Explicitly None type
    label = "Element/Layout"
    color: tuple[float, float, float, float] = (0.8, 0.2, 0.2, 1.0) # Distinct color

    # Override value properties as they are meaningless here
    @property
    def value(self) -> None:
        return None

    def set_value(self, value: None):
        pass # Setting a value does nothing

    # Override draw to be simple
    def draw(self, context: bpy.types.Context, layout: bpy.types.UILayout, node: bpy.types.Node, text: str):
        layout.label(text=self.label or self.name)

    # Ensure value_type returns None
    @property
    def value_type(self) -> Type[None]:
        return type(None)
