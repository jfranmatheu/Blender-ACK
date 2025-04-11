from .base import BaseUI, UILayout
from ...globals import GLOBALS

import bpy
from bpy.types import UIList as BlUIList, Context, UILayout


class UIList(BaseUI, BlUIList):
    label: str

    @classmethod
    def draw_in_layout(cls, layout: UILayout, data, attr_coll: str, attr_index: str, rows: int = 5, list_id: str = ''):
        layout.template_list(
            cls.bl_idname, list_id,
            data, attr_coll,
            data, attr_index,
            rows=rows
        )
