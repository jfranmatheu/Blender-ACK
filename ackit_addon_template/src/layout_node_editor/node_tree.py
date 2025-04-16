from ...ackit import ACK

from bpy import types as bpy_types


class UILayoutNodeTree(ACK.NE.TreeExec):
    bl_label = "UI Layout Node Tree"

    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> None:
        super().execute(context, layout)
