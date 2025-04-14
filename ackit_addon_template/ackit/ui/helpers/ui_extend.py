from typing import Callable, List, Tuple, Type, Union

from bpy.types import Menu, Panel, Context, UILayout

from ...debug import get_logger # Corrected import: Use get_logger factory


_log = get_logger("UI Extend") # Corrected instantiation

# --- Type Aliases ---
# The signature of a function used for drawing in Panels/Menus
UIDrawFunc = Callable[[Context, UILayout], None]
UIExtension = Tuple[Type, UIDrawFunc, str] # (target_cls, func, mode)
UI_TYPES = (Panel, Menu)

# Registry to store functions to be appended/prepended
_ui_extensions: List[UIExtension] = []


# --- Decorators ---

def ui_extend(target_cls: Type, prepend: bool = False) -> Callable[[UIDrawFunc], UIDrawFunc]:
    """
    Decorator to register a function to be appended or prepended to a Blender UI class's draw method.
    
    Usage:
        @ui_extend(bpy.types.SOME_PT_panel, prepend=True)
        def my_draw_func(context, layout):
            layout.label(text="Hello")

    Args:
        target_cls: The Blender Panel or Menu class (e.g., bpy.types.OBJECT_MT_context_menu).
        prepend: Whether to prepend the function instead of appending.
        
    Returns:
        Callable: The decorated function with (bpy.types.Context, bpy.types.UILayout) arguments.
    """
    if prepend:
        return prepend_to(target_cls)
    else:
        return append_to(target_cls)

def append_to(target_cls: Type) -> Callable[[UIDrawFunc], UIDrawFunc]:
    """
    Decorator to register a function to be appended to a Blender UI class's draw method.

    Usage:
        @append_to(bpy.types.SOME_PT_panel)
        def my_draw_func(context, layout):
            layout.label(text="Hello")

    Args:
        target_cls: The Blender Panel or Menu class (e.g., bpy.types.OBJECT_MT_context_menu).
        
    Returns:
        Callable: The decorated function with (bpy.types.Context, bpy.types.UILayout) signature.
    """
    if not isinstance(target_cls, UI_TYPES) or not hasattr(target_cls, 'bl_rna'):
         _log.warning(f"Target class '{target_cls}' might not be a valid Blender UI type for appending.")
         # Allow proceeding but log warning

    def decorator(func: UIDrawFunc) -> UIDrawFunc:
        _log.debug(f"Queueing '{func.__name__}' for appending to '{target_cls.__name__}'")
        _ui_extensions.append((target_cls, func, 'append'))
        # Return the original function unmodified. Registration happens later.
        return func
    return decorator

def prepend_to(target_cls: Type) -> Callable[[UIDrawFunc], UIDrawFunc]:
    """
    Decorator to register a function to be prepended to a Blender UI class's draw method.

     Usage:
        @prepend_to(bpy.types.SOME_MT_menu)
        def my_draw_func(context, layout):
            layout.operator("wm.open_mainfile")

    Args:
        target_cls: The Blender Panel or Menu class (e.g., bpy.types.OBJECT_MT_context_menu).
        
    Returns:
        Callable: The decorated function with (bpy.types.Context, bpy.types.UILayout) signature.
    """
    if not isinstance(target_cls, UI_TYPES) or not hasattr(target_cls, 'bl_rna'):
         _log.warning(f"Target class '{target_cls}' might not be a valid Blender UI type for prepending.")
         # Allow proceeding but log warning

    def decorator(func: UIDrawFunc) -> UIDrawFunc:
        _log.debug(f"Queueing '{func.__name__}' for prepending to '{target_cls.__name__}'")
        _ui_extensions.append((target_cls, func, 'prepend'))
        # Return the original function unmodified. Registration happens later.
        return func
    return decorator


# --- UI Extension Registration ---

def register_ui_extensions():
    """Applies all queued UI extensions using the appropriate .append or .prepend."""
    if not _ui_extensions:
        return

    _log.info(f"Applying {len(_ui_extensions)} UI draw extensions...")
    for target_cls, func, mode in _ui_extensions:
        try:
            op = getattr(target_cls, mode, None)
            if callable(op):
                op(func)
                _log.debug(f"{mode.capitalize()}ed '{func.__name__}' to '{target_cls.__name__}'")
            else:
                # This might happen if the target_cls is not a Panel or Menu type
                _log.warning(f"Target class '{target_cls.__name__}' does not support .{mode}()")
        except Exception as e:
            # Catch potential errors during the actual append/prepend call
            _log.error(f"Failed to {mode} '{func.__name__}' to '{target_cls.__name__}': {e}", exc_info=True)

def unregister_ui_extensions():
    """Removes all applied UI extensions using .remove()."""
    if not _ui_extensions:
        return

    _log.info(f"Removing {len(_ui_extensions)} UI draw extensions...")
    # Iterate in reverse order of registration for potentially safer unregistration
    for target_cls, func, mode in reversed(_ui_extensions):
         try:
             # Both append and prepend use .remove for unregistration
             op = getattr(target_cls, 'remove', None)
             if callable(op):
                 # Blender's remove handles non-existent functions gracefully (no error).
                 op(func)
                 _log.debug(f"Removed '{func.__name__}' from '{target_cls.__name__}' (was {mode}ed)")
             else:
                  _log.warning(f"Target class '{target_cls.__name__}' does not support .remove() for '{func.__name__}'")
         except Exception as e:
             # Capture potential errors during removal, though Blender's remove is usually safe.
             _log.warning(f"Could not remove '{func.__name__}' from '{target_cls.__name__}': {e}", exc_info=True)

    # Clear the list after attempting unregistration. This prevents accidental re-registration
    # if the module is somehow not fully cleared on script reload without full addon disable/enable.
    _ui_extensions.clear()

# Example Usage (within an addon using ackit):
# from ackit.ui.helpers.ui_append import append_to, prepend_to
# from bl_ui.space_properties import PROPERTIES_PT_options
#
# @append_to(PROPERTIES_PT_options)
# def _my_props_draw_append(self, context):
#     self.layout.label(text="Appended from My Addon!")
#
# @prepend_to(bpy.types.OBJECT_MT_context_menu)
# def _my_object_menu_prepend(self, context):
#     self.layout.operator("object.select_all", text="Prepended Select")
#


# --- Register/Unregister ---

def register():
    register_ui_extensions()

def unregister():
    unregister_ui_extensions()
