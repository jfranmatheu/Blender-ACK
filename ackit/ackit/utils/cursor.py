from enum import Enum

import bpy
from bpy.types import Context


class Cursor(Enum):
    DEFAULT       =      'DEFAULT'
    NONE          =         'NONE'
    WAIT          =         'WAIT'
    CROSSHAIR     =    'CROSSHAIR'
    MOVE_X        =       'MOVE_X'
    MOVE_Y        =       'MOVE_Y'
    KNIFE         =        'KNIFE'
    TEXT          =         'TEXT'
    PAINT_BRUSH   =  'PAINT_BRUSH'
    PAINT_CROSS   =  'PAINT_CROSS'
    HAND          =         'HAND'
    SCROLL_X      =     'SCROLL_X'
    SCROLL_Y      =     'SCROLL_Y'
    SCROLL_XY     =    'SCROLL_XY'
    EYEDROPPER    =   'EYEDROPPER'
    DOT           =          'DOT'
    ERASER        =       'ERASER'

    def set_icon(self, context: Context | None = None) -> None:
        context = context if context is not None else bpy.context
        context.window.cursor_modal_set(self.value)

    @staticmethod
    def wrap(x: int, y: int, context: Context | None = None) -> None:
        context = context if context is not None else bpy.context
        context.window.cursor_warp(x, y)

    @staticmethod
    def restore(context: Context | None = None) -> None:
        context = context if context is not None else bpy.context
        context.window.cursor_modal_restore()


class OperatorCursorUtils:
    _current_cursor: Cursor | None = None
    _previous_cursor: Cursor | None = None

    def set_cursor(self, cursor_type: Cursor, context: Context | None = None) -> None:
        """Set the cursor type for the modal operator.
        
        Args:
            cursor_type: The Cursor enum value to set
            context: Optional context override
        """
        # Store the current cursor type if we haven't stored one yet
        if self._previous_cursor is None and self._current_cursor is not None:
            # We can't actually get the current cursor type from Blender,
            # so we'll just use DEFAULT as a fallback
            self._previous_cursor = self._current_cursor

        self._current_cursor = cursor_type
        cursor_type.set_icon(context)

    def restore_cursor(self, context: Context | None = None) -> None:
        """Restore the cursor to its previous state."""
        if self._previous_cursor is not None:
            Cursor.restore(context)

    def wrap_cursor(self, x: int, y: int, context: Context | None = None) -> None:
        """Wrap the cursor to specified coordinates."""
        Cursor.wrap(x, y, context)
