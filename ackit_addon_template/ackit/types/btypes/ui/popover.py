from .panel import Panel
from ....decorators.options import PanelOptions


class Popover(Panel):
    bl_options: set[str] = {PanelOptions.INSTANCED.name}
