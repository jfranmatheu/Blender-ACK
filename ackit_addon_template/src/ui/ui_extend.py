from bl_ui.space_view3d import VIEW3D_HT_header
from bpy import types as bpy_types

from ...ackit import ACK


# Without ACKit helper
# It does not handle unregistering.
# So same function is appended when updating/refreshing the addon.

'''
@VIEW3D_HT_header.append
def draw_header(self, context):
    self.layout.operator("wm.open_mainfile")
'''

# With ACKit helper
# While it can be less intuitive syntax, it handles unregistering, which makes it more robust.

@ACK.UI.extend_layout(VIEW3D_HT_header)
def draw_header(context: bpy_types.Context, layout: bpy_types.UILayout):
    layout.operator("wm.open_mainfile")
