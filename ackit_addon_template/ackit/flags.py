from enum import Enum, auto
from typing import Type, Callable, TypeVar

import bpy

# Assuming T might represent different base types (Operator, Modal, Node, Panel) depending on context.
# A more robust solution might involve TypeVars or Protocol, but for now, using 'Any' or specific types where clear.
from typing import Any
# We will need imports for base types later, potentially like:
# from .ops.btypes.generic import Operator
# from .ops.btypes.modal import ModalOperator # If Modal base class exists
# from .ne.btypes.node import Node
# from .ui.btypes.panel import Panel
# Import base types for TypeVar bounds
from .ne.btypes import Node as _NodeType # Use alias to avoid name clash if needed
from .ui.btypes import Panel as _PanelType # Use alias

__all__ = [
    'OPERATOR',
    'MODAL',
    'PANEL',
    'NODE_CATEGORY',
]


# --- Operator Flags ---

class _OperatorTypeFlags(Enum):
    # https://docs.blender.org/api/current/bpy_types_enum_items/operator_type_flag_items.html#rna-enum-operator-type-flag-items
    REGISTER = auto()
    UNDO = auto()
    UNDO_GROUPED = auto()
    BLOCKING = auto()
    MACRO = auto()
    GRAB_CURSOR = auto()
    GRAB_CURSOR_X = auto()
    GRAB_CURSOR_Y = auto()
    DEPENDS_ON_CURSOR = auto()
    PRESET = auto()
    INTERNAL = auto()
    MODAL_PRIORITY = auto()

class OPERATOR:
    """ Decorators for adding Blender operator options. """

    @staticmethod
    def _decorator(*flags: _OperatorTypeFlags, **kwargs) -> Callable[[Type[Any]], Type[Any]]:
        """ Base decorator to add Blender operator type flags. """
        def wrapper(cls: Type[Any]) -> Type[Any]:
            if not hasattr(cls, 'bl_options'):
                cls.bl_options = set()
            for flag in flags:
                cls.bl_options.add(flag.name)
            for key, value in kwargs.items():
                setattr(cls, key, value)
            return cls
        return wrapper

    @classmethod
    def REGISTER(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Integrates operator into Blender's UI. """
        return cls._decorator(_OperatorTypeFlags.REGISTER)(_deco_cls)

    @classmethod
    def UNDO(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Creates an undo event for data-modifying operators. """
        return cls._decorator(_OperatorTypeFlags.UNDO)(_deco_cls)

    @classmethod
    def REGISTER_UNDO(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Combines REGISTER and UNDO flags. """
        # Original REGISTER_UNDO combined REGISTER and UNDO, let's keep that logic
        return cls._decorator(_OperatorTypeFlags.REGISTER, _OperatorTypeFlags.UNDO)(_deco_cls)

    @classmethod
    def UNDO_GROUPED(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Consolidates multiple similar operator executions in undo stack. """
        return cls._decorator(_OperatorTypeFlags.UNDO_GROUPED)(_deco_cls)

    @classmethod
    def BLOCKING(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Exclusively controls cursor during operator execution. """
        return cls._decorator(_OperatorTypeFlags.BLOCKING)(_deco_cls)

    @classmethod
    def MACRO(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Marks operator as a composite of multiple sub-operations. """
        return cls._decorator(_OperatorTypeFlags.MACRO)(_deco_cls)

    @classmethod
    def GRAB_CURSOR(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Captures mouse focus for continuous interactions. """
        return cls._decorator(_OperatorTypeFlags.GRAB_CURSOR)(_deco_cls)

    @classmethod
    def GRAB_CURSOR_X(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Constrains cursor movement to horizontal axis. """
        return cls._decorator(_OperatorTypeFlags.GRAB_CURSOR_X)(_deco_cls)

    @classmethod
    def GRAB_CURSOR_Y(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Constrains cursor movement to vertical axis. """
        return cls._decorator(_OperatorTypeFlags.GRAB_CURSOR_Y)(_deco_cls)

    @classmethod
    def PRESET(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Adds preset button to operator settings. """
        return cls._decorator(_OperatorTypeFlags.PRESET)(_deco_cls)

    @classmethod
    def INTERNAL(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Removes operator from public search results. """
        return cls._decorator(_OperatorTypeFlags.INTERNAL)(_deco_cls)

    @classmethod
    def MODAL_PRIORITY(cls, _deco_cls: Type[Any]) -> Type[Any]:
        """ Gives operator higher event handling priority. """
        return cls._decorator(_OperatorTypeFlags.MODAL_PRIORITY)(_deco_cls)

    class DEPENDS_ON_CURSOR(Enum):
        """ Requires specific initial cursor placement. """
        DEFAULT = "Default"
        NONE = "None"
        WAIT = "Wait"
        CROSSHAIR = "Crosshair"
        MOVE_X = "Move-X"
        MOVE_Y = "Move-Y"
        KNIFE = "Knife"
        TEXT = "Text"
        PAINT_BRUSH = "Paint Brush"
        PAINT_CROSS = "Paint Cross"
        DOT = "Dot Cursor"
        ERASER = "Eraser"
        HAND = "Open Hand"
        HAND_POINT = "Pointing Hand"
        HAND_CLOSED = "Closed Hand"
        SCROLL_X = "Scroll-X"
        SCROLL_Y = "Scroll-Y"
        SCROLL_XY = "Scroll-XY"
        EYEDROPPER = "Eyedropper"
        PICK_AREA = "Pick Area"
        STOP = "Stop"
        COPY = "Copy"
        CROSS = "Cross"
        MUTE = "Mute"
        ZOOM_IN = "Zoom In"
        ZOOM_OUT = "Zoom Out"

        def __call__(self, _deco_cls: Type[Any]) -> Type[Any]:
            """ Decorator method for DEPENDS_ON_CURSOR flag. """
            return OPERATOR._decorator(
                _OperatorTypeFlags.DEPENDS_ON_CURSOR,
                bl_cursor_pending=self.name
            )(_deco_cls)


# --- Modal Flags ---

class _ModalInternalFlags(Enum):
    DRAW_POST_PIXEL = auto()
    DRAW_POST_VIEW = auto()
    DRAW_PRE_VIEW = auto()
    DRAW_BACKDROP = auto()

class MODAL:
    """ Decorators for adding modal operator flags. """

    @staticmethod
    def _decorator(flag: _ModalInternalFlags, **kwargs) -> Callable[[Type[Any]], Type[Any]]:
        """ Base decorator to enable custom modal functionalities. """
        def wrapper(cls: Type[Any]) -> Type[Any]:
            if not hasattr(cls, '_modal_flags') or cls._modal_flags is None:
                cls._modal_flags = set()
            cls._modal_flags.add(flag)
            for key, value in kwargs.items():
                setattr(cls, key, value)
            return cls
        return wrapper

    class DRAW_POST_PIXEL(Enum):
        """ Enables draw_2d() function in the modal for the selected space. """
        VIEW_3D = bpy.types.SpaceView3D
        IMAGE_EDITOR = bpy.types.SpaceImageEditor
        # ... (add other space types as needed from original file) ...
        NODE_EDITOR = bpy.types.SpaceNodeEditor

        def __call__(self, _deco_cls: Type[Any]) -> Type[Any]:
            return MODAL._decorator(_ModalInternalFlags.DRAW_POST_PIXEL, _draw_postpixel_space=self.value)(_deco_cls)

    class DRAW_POST_VIEW(Enum):
        """ Enables draw_3d() function in the modal for the selected space. """
        VIEW_3D = bpy.types.SpaceView3D
        # ... (add other space types as needed) ...

        def __call__(self, _deco_cls: Type[Any]) -> Type[Any]:
            return MODAL._decorator(_ModalInternalFlags.DRAW_POST_VIEW, _draw_postview_space=self.value)(_deco_cls)

    class DRAW_PRE_VIEW(Enum):
        """ Enables draw_3d() function (before standard drawing) in the modal for the selected space. """
        VIEW_3D = bpy.types.SpaceView3D
        # ... (add other space types as needed) ...

        def __call__(self, _deco_cls: Type[Any]) -> Type[Any]:
            return MODAL._decorator(_ModalInternalFlags.DRAW_PRE_VIEW, _draw_preview_space=self.value)(_deco_cls)

    class DRAW_BACKDROP(Enum):
        """ Enables draw_backdrop() function in the modal for the selected node editor type. """
        SHADER_NODE_TREE = 'ShaderNodeTree'
        GEOMETRY_NODE_TREE = 'GeometryNodeTree'
        TEXTURE_NODE_TREE = 'TextureNodeTree'

        def __call__(self, _deco_cls: Type[Any]) -> Type[Any]:
            return MODAL._decorator(_ModalInternalFlags.DRAW_BACKDROP, _draw_backdrop_treetype=self.value)(_deco_cls)


# --- Panel Flags ---

PanelT = TypeVar('PanelT', bound=_PanelType) # Bound to Panel base type

class PANEL(Enum):
    """ Decorator flags for Panels. Use as @flags.PANEL.HIDE_HEADER etc. """
    HIDE_HEADER = auto()
    DEFAULT_CLOSED = auto()
    INSTANCED = auto()

    def __call__(self, panel_cls: Type[PanelT]) -> Type[PanelT]:
        if not hasattr(panel_cls, 'bl_options') or panel_cls.bl_options is None:
            panel_cls.bl_options = set()
        panel_cls.bl_options.add(self.name)
        return panel_cls


# --- Node Category Flag ---

NodeT = TypeVar('NodeT', bound=_NodeType) # Bound to Node base type

def NODE_CATEGORY(category: str) -> Callable[[Type[NodeT]], Type[NodeT]]:
    """
    Decorator to add a node category to a node class.

    Args:
        category (str): The node category. Use '/' for subcategories.

    Returns:
        Callable: Decorator function.
    """
    def wrapper(cls: Type[NodeT]) -> Type[NodeT]:
        # Now Pylance knows cls is a subclass of Node and has _node_category
        cls._node_category = category
        return cls
    return wrapper 


class NodeColorTag(Enum):
    """
    Decorator utility to set the color tag of a node.
    """
    NONE = auto()
    ATTRIBUTE = auto()
    COLOR = auto()
    CONVERTER = auto()
    DISTORT = auto()
    FILTER = auto()
    GEOMETRY = auto()
    INPUT = auto()
    MATTE = auto()
    OUTPUT = auto()
    SCRIPT = auto()
    SHADER = auto()
    TEXTURE = auto()
    VECTOR = auto()
    PATTERN = auto()
    INTERFACE = auto()
    GROUP = auto()
    
    def __call__(self, _deco_cls: Type[NodeT]) -> Type[NodeT]:
        _deco_cls._color_tag = self.name
        return _deco_cls


class NodeFlags:
    ColorTag = NodeColorTag
