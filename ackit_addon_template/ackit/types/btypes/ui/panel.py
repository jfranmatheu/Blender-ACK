from typing import Callable
from types import new_class

from .base import BaseUI, DrawExtension, UILayout, Context
from ....globals import GLOBALS
from ....decorators.options import PanelOptions

from bpy.types import Panel as BlPanel


class Panel(BaseUI, DrawExtension):
    bl_category: str = GLOBALS.ADDON_MODULE_UPPER
    bl_context: str = ''
    bl_space_type: str = 'VIEW_3D'
    bl_region_type: str = 'UI'
    bl_options: set[str]

    @classmethod
    def tag_register(deco_cls) -> 'Panel':
        return super().tag_register(
            BlPanel, 'PT'
        )

    @classmethod
    def new_from_func(cls, func: Callable, **kwargs) -> 'Panel':
        cls = new_class(
            func.__name__,
            (Panel, ),
            {
                **kwargs,
                'draw_ui': func,
            }
        )
        cls.tag_register()
        return cls

    def draw_header(self, context: Context):
        super().draw_header(context)

    @classmethod
    def draw_in_layout(cls, layout: UILayout, label: str = 'Panel', as_popover: bool = False):
        if as_popover:
            layout.popover(cls.bl_idname, text=label)
        else:
            return layout.panel(cls.bl_idname, default_closed=False)


