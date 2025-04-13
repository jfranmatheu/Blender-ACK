from typing import Callable, Type, Set, ClassVar, List, Optional, Any, Union, TYPE_CHECKING
from enum import Enum, auto

from .base import BaseUI, DrawExtension, UILayout, Context
from ...globals import GLOBALS
# from ...flags import PANEL as PanelOptions  # circular import!

# Import PanelOptionsEnum only for type checking
if TYPE_CHECKING:
    from ...flags import PANEL as PanelOptionsEnum

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

    def __call__(self, tab: Optional[str] = None, flags: Optional[Set[Union[str, 'PanelOptionsEnum']]] = None, order: int = 0) -> Callable[[Callable[[Context, UILayout], None]], Type['Panel']]:
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

        def __call__(self, tab: Optional[str] = None, flags: Optional[Set[Union[str, 'PanelOptionsEnum']]] = None, order: int = 0) -> Callable[[Callable[[Context, UILayout], None]], Type['Panel']]:
            """Returns decorator that sets properties context and optional tab"""
            return Panel.from_function('PROPERTIES', 'WINDOW', tab=tab, context=self.name.lower(), flags=flags, order=order)


class Panel(BaseUI, DrawExtension, BlPanel):
    bl_category: str = GLOBALS.ADDON_MODULE_UPPER
    bl_context: str = ''
    bl_space_type: str = 'VIEW_3D'
    bl_region_type: str = 'UI'
    bl_options: set[str]

    _polling_functions: ClassVar[Set[Callable[[Context], bool]]] = set()

    @classmethod
    def poll(cls, context: Context) -> bool:
        """Default poll method. Iterates through registered polling functions."""
        if cls._polling_functions:
            for func in cls._polling_functions:
                if not func(context):
                    return False
        return True

    FromFunction = PanelFromFunction  # utility to access the PanelFromFunction enum that helps with the creation of panels from functions with ease.

    @classmethod
    def from_function(cls,
                      space_type: str = 'VIEW_3D',
                      region_type: str = 'UI',
                      tab: Optional[str] = None,
                      context: Optional[str] = None,
                      flags: Optional[Set[Union[str, 'PanelOptionsEnum']]] = None,
                      order: int = 0) -> Callable[[Callable[[Context, UILayout], None]], Type['Panel']]:
        """
        Decorator factory to create a Panel class from a draw function.

        This allows defining simple panels without explicitly creating a new class.
        It's the underlying mechanism used by the `PanelFromFunction` enum decorators.

        Args:
            space_type (str): The space type where the panel appears.
                              Common values: 'VIEW_3D', 'PROPERTIES', 'NODE_EDITOR',
                              'IMAGE_EDITOR', 'SEQUENCE_EDITOR', etc.
            region_type (str): The region within the space type.
                               Common values: 'UI' (Side Panel), 'WINDOW', 'HEADER',
                               'TOOLS', 'TOOL_PROPS'.
            tab (Optional[str]): The category tab name under which the panel appears 
                                 (e.g., in the VIEW_3D UI region).
                                 Defaults to the Addon's name from GLOBALS.
            context (Optional[str]): The specific context within certain space types, 
                                     primarily 'PROPERTIES'. Common values: 'OBJECT', 
                                     'MATERIAL', 'SCENE', 'WORLD', 'RENDER', 
                                     'OUTPUT', 'VIEW_LAYER', 'DATA' (for Mesh, Curve, etc.),
                                     'MODIFIER', 'CONSTRAINT', 'BONE', etc.
                                     Leave as None or '' for spaces without specific contexts.
            flags (Optional[Set[Union[str, ackit.flags.PANEL]]]): 
                A set of flags. Can contain strings (like 'DEFAULT_CLOSED') or 
                members from the `ackit.flags.PANEL` enum.
                (Type hinted as `Optional[Set[Union[str, 'PanelOptionsEnum']]]` 
                 using a forward reference for type checking).
                Example: `flags={'DEFAULT_CLOSED', PanelFlags.INSTANCED}`
            order (int): The panel's drawing order within its category/context.
                         Lower numbers appear first.

        Returns:
            Callable[[Callable[[Context, UILayout], None]], Type[Panel]]: 
                A decorator. When applied to a function `func(context, layout)`, 
                it generates and registers a new Panel subclass whose `draw` 
                method calls `func`.

        Usage Example:
            ```python
            from ackit import ACK
            from ackit.flags import PANEL as PanelFlags # Import for flags

            @ACK.UI.create_panel_from_func(space_type='PROPERTIES', region_type='WINDOW', 
                                       context='OBJECT', tab="Custom Props", 
                                       flags={PanelFlags.DEFAULT_CLOSED, 'INSTANCED'})
            def my_object_props_panel(context, layout):
                layout.label(text="My Properties")
            ```
        """
        DrawFuncType = Callable[[Context, UILayout], None]

        def decorator(func: DrawFuncType) -> Type[Panel]: # type: ignore[valid-type]
            panel_flags = {flag if isinstance(flag, str) else flag.name 
                           for flag in flags} if flags is not None else set()
            panel_category = tab if tab is not None else GLOBALS.ADDON_MODULE_UPPER
            panel_context = context if context is not None else ''

            cls_dict = {
                'bl_space_type': space_type,
                'bl_region_type': region_type,
                'bl_category': panel_category,
                'bl_context': panel_context,
                'bl_options': panel_flags,
                'bl_order': order,
                'draw_ui': lambda self, ctx, layout: func(ctx, layout),
                '_polling_functions': set()
            }

            if cls_dict['poll'] is None:
                del cls_dict['poll']

            new_cls = type(
                func.__name__,
                (Panel, ),
                cls_dict
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
