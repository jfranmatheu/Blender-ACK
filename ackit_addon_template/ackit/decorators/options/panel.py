from enum import Enum, auto

from bpy.types import Panel


class PanelOptions(Enum):
    ''' Use as decorator over a Panel subclass. '''
    HIDE_HEADER = auto()
    DEFAULT_CLOSED = auto()
    INSTANCED = auto()

    def __call__(self, deco_cls: Panel):
        if not hasattr(deco_cls, 'bl_options') or deco_cls.bl_options is None:
            deco_cls.bl_options = set()
        deco_cls.bl_options.add(self.name)
        return deco_cls
