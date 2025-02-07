from enum import Enum, auto
from typing import Callable, Type

from ....types.btypes.ui.panel import Panel
from ....globals import GLOBALS


__all__ = [
    'PanelFromFunction'
]


def panel_from_function(space_type: str,
                       region_type: str,
                       tab: str | None = GLOBALS.ADDON_MODULE_UPPER,
                       context: str = '') -> Type:
    def decorator(func: Callable) -> Type:
        new_cls = Panel.new_from_func(
            func,
            bl_space_type=space_type,
            bl_region_type=region_type,
            bl_category=tab if tab is not None else GLOBALS.ADDON_MODULE_UPPER,
            bl_context=context,
        )
        return new_cls

    return decorator



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
    VIEW3D = auto()
    NODE_EDITOR = auto()
    IMAGE_EDITOR = auto()
    SEQUENCE_EDITOR = auto()
    DOPESHEET_EDITOR = auto()
    GRAPH_EDITOR = auto()
    NLA_EDITOR = auto()
    TEXT_EDITOR = auto()
    OUTLINER = auto()
    FILE_BROWSER = auto()

    def __call__(self, tab: str = None) -> Callable[[Type], Type]:
        """Returns decorator that sets space type and optional tab"""
        return panel_from_function(self.name, 'UI', tab=tab)
        

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

        def __call__(self, tab: str = None) -> Callable[[Type], Type]:
            """Returns decorator that sets properties context and optional tab"""
            return panel_from_function('PROPERTIES', 'WINDOW', tab=tab, context=self.name.lower())
