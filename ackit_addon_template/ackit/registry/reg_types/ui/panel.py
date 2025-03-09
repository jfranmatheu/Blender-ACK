from typing import Callable, Type
from enum import Enum, auto

from .base import BaseUI, DrawExtension, UILayout, Context
from ....globals import GLOBALS
from ...flags import PanelOptions

from bpy.types import Panel as BlPanel

__all__ = [
    'PanelFromFunction',
    'Panel',
]

class PanelFromFunction(Enum):
    """Decorator to create panels of the specified space type from a decorated function.
        ## Usage Example:
        ```py
        @Panel.VIEW3D(tab="My Tab")
        def my_panel_1(context, layout):
            layout.label(text="My Panel 1")
        ```
        ```py
        @Panel.Properties.OBJECT(tab="My Tab")
        def my_panel_2(context, layout):
            layout.label(text="My Panel 2")
        ```
    """
    VIEW_3D = auto()
    NODE_EDITOR = auto()
    IMAGE_EDITOR = auto()
    SEQUENCE_EDITOR = auto()
    DOPESHEET_EDITOR = auto()
    GRAPH_EDITOR = auto()
    NLA_EDITOR = auto()
    TEXT_EDITOR = auto()
    OUTLINER = auto()
    FILE_BROWSER = auto()

    def __call__(self, tab: str = None, flags: PanelOptions = None, order: int = 0) -> Callable[[Type], Type]:
        """Returns decorator that sets space type and optional tab"""
        return Panel.from_function(self.name, 'UI', tab=tab, flags=flags, order=order)


    class Properties(Enum):
        """Properties editor context decorators"""
        OBJECT = auto()
        MATERIAL = auto()
        TEXTURE = auto()
        PARTICLE = auto()
        PHYSICS = auto()
        MODIFIER = auto()
        BONE = auto()
        CONSTRAINT = auto()
        RENDER = auto()
        SCENE = auto()
        WORLD = auto()

        def __call__(self, tab: str = None, flags: PanelOptions = None, order: int = 0) -> Callable[[Type], Type]:
            """Returns decorator that sets properties context and optional tab"""
            return Panel.from_function('PROPERTIES', 'WINDOW', tab=tab, context=self.name.lower(), flags=flags, order=order)


class Panel(BaseUI, DrawExtension, BlPanel):
    bl_category: str = GLOBALS.ADDON_MODULE_UPPER
    bl_context: str = ''
    bl_space_type: str = 'VIEW_3D'
    bl_region_type: str = 'UI'
    bl_options: set[str]

    @classmethod
    def from_function(cls,
                      space_type: str = 'TOPBAR',
                      region_type: str = 'HEADER',
                      tab: str | None = GLOBALS.ADDON_MODULE_UPPER,
                      context: str = '',
                      flags: PanelOptions = None,
                      order: int = 0) -> 'Panel':
        """ Decorator to create a panel from a function. """
        def decorator(func: Callable) -> Panel:
            new_cls = type(
                func.__name__,
                (Panel, ),
                {
                    'bl_space_type': space_type,
                    'bl_region_type': region_type,
                    'bl_category': tab if tab is not None else GLOBALS.ADDON_MODULE_UPPER,
                    'bl_context': context,
                    'bl_options': {flag.name for flag in flags} if flags else set(),
                    'bl_order': order,
                    'draw_ui': lambda self, ctx, layout: func(ctx, layout),
                }
            )
            new_cls.__module__ = func.__module__
            new_cls.tag_register()
            return new_cls
        return decorator

    # def draw_header(self, context: Context):
    #     super().draw_header(context)

    @classmethod
    def draw_in_layout(cls, layout: UILayout, label: str = 'Panel', as_popover: bool = False):
        if as_popover:
            layout.popover(cls.bl_idname, text=label)
        else:
            return layout.panel(cls.bl_idname, default_closed=False)
