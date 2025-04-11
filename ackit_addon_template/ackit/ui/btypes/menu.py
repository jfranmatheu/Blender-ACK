from typing import Callable

import bpy
from bpy.types import Menu as BlMenu

from .base import BaseUI, UILayout


__all__ = [
    'Menu',
]


class Menu(BaseUI, BlMenu):
    '''
    A class for creating a menu.
    '''

    @classmethod
    def from_function(cls, label: str, **kwargs) -> 'Menu':
        def decorator(func: Callable) -> 'Menu':
            new_cls = type(
                func.__name__,
                (Menu, ),
                {
                    **kwargs,
                    'label': label,
                    'draw_ui': lambda self, ctx, layout: func(ctx, layout),
                }
            )
            new_cls.__module__ = func.__module__
            new_cls.tag_register()
            return new_cls
        return decorator

    @classmethod
    def popup(cls) -> None:
        bpy.ops.wm.call_menu('INVOKE_DEFAULT', name=cls.bl_idname)

    @classmethod
    def draw_in_layout(cls, layout: UILayout, label: str = None, icon: str = 'NONE'):
        layout.menu(cls.bl_idname, text=label if label is not None else cls.bl_label, icon=icon)
