from typing import Callable
from types import new_class

import bpy
from bpy.types import Menu as BlMenu

from .base import BaseUI, UILayout
from ....globals import GLOBALS


class Menu(BaseUI):

    @classmethod
    def tag_register(deco_cls) -> 'Menu':
        return super().tag_register(BlMenu, 'MT')
    
    @classmethod
    def new_from_func(cls, func: Callable, **kwargs) -> 'Menu':
        cls = new_class(
            func.__name__,
            (Menu, ),
            {
                **kwargs,
                'draw_ui': func,
            }
        )
        cls.tag_register()
        return cls

    @classmethod
    def popup(cls) -> None:
        bpy.ops.wm.call_menu('INVOKE_DEFAULT', name=cls.bl_idname)

    @classmethod
    def draw_in_layout(cls, layout: UILayout, label: str = None, icon: str = 'NONE'):
        layout.menu(cls.bl_idname, text=label if label is not None else cls.bl_label, icon=icon)
