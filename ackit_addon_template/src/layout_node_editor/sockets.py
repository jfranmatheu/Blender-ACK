from typing import TypeVar, Generic, Type, Any
import bpy

from ...ackit import ACK

__all__ = [
    'LayoutSocket',
]


# Socket for passing UILayout objects
class LayoutSocket(ACK.NE.SocketExec[bpy.types.UILayout]):
    label = "Layout"
    color: tuple[float, float, float, float] = (0.2, 0.2, 0.8, 1.0)
