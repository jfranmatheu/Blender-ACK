from bpy.types import UILayout

from .panel import Panel
from ...flags import PANEL as PanelOptions


class Popover(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {PanelOptions.INSTANCED.name}
    bl_category = ''

    @classmethod
    def from_function(cls):
        return super().from_function(
            space_type='VIEW_3D',
            region_type='WINDOW',
            tab='',
            flags={PanelOptions.INSTANCED}
        )

    @classmethod
    def draw_in_layout(cls, layout: UILayout, label: str | None = None):
        return super().draw_in_layout(layout, label if label is not None else cls.bl_label, as_popover=True)
