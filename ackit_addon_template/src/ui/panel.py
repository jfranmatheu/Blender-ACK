from bpy.types import Context, UILayout
from ...ackit import ACK


@ACK.UI.Popover.from_function()
def my_popover(_context: Context, layout: UILayout):
    layout.label(text="My Nice Popover")


@ACK.UI.Panel.FromFunction.VIEW_3D(tab="My Tab", flags={ACK.UI.PanelFlags.HIDE_HEADER}, order=1)
def my_panel_1(context: Context, layout: UILayout):
    layout.label(text="My Panel 1")
    obj = context.object
    if obj:
        layout.prop(obj, "name")
    layout.operator('render.render', text="Render")
    my_popover.draw_in_layout(layout, as_popover=True)

@ACK.UI.Panel.FromFunction.VIEW_3D(tab="My Tab", flags={ACK.UI.PanelFlags.DEFAULT_CLOSED}, order=2)
def my_panel_2(_context: Context, layout: UILayout):
    layout.label(text="My Panel 200")

@ACK.UI.Panel.FromFunction.VIEW_3D(tab="My Tab", order=3)
def my_panel_3(_context: Context, layout: UILayout):
    layout.label(text="My Panel 300")
