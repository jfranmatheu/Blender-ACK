from typing import TypeVar, Generic, Type, Any
import bpy

from ...ackit import ACK

__all__ = [
    'LayoutSocket',
    'ElementSocket',
]


# Socket for passing UILayout objects
class LayoutSocket(ACK.NE.SocketExec[bpy.types.UILayout]):
    label = "Layout"
    color: tuple[float, float, float, float] = (0.2, 0.2, 0.8, 1.0)


# Socket for signaling UI Element children (does not pass data)
class ElementSocket(ACK.NE.SocketExec[None]): # Explicitly None type
    label = "Element"
    color: tuple[float, float, float, float] = (0.8, 0.2, 0.2, 1.0) # Distinct color

    # Override value properties as they are meaningless here
    @property
    def value(self) -> None:
        # This socket type doesn't transfer values via the standard mechanism.
        # Use get_connected_nodes() on the input socket instead.
        return None

    def set_value(self, value: None):
        # Setting a value on an Element output socket does nothing.
        pass

    # Override draw to maybe be simpler or indicate its purpose
    def draw(self, context: bpy.types.Context, layout: bpy.types.UILayout, node: bpy.types.Node, text: str):
        # Just draw the label, no property field needed
        layout.label(text=self.label or self.name)

    # Ensure value_type returns None
    @property
    def value_type(self) -> Type[None]:
        return type(None)
