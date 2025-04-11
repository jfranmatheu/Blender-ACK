from ...ackit import ACK


@ACK.UI.create_popover_from_func()
def my_popover(context, layout):
    layout.label(text="My Popover")


@ACK.UI.create_panel_from_func.VIEW_3D(tab="My Tab", flags=(ACK.UI.add_panel_flag.HIDE_HEADER,), order=1)
def my_panel_1(context, layout):
    layout.label(text="My Panel 1")
    layout.operator('render.render', text="Render")
    my_popover.draw_in_layout(layout)

@ACK.UI.create_panel_from_func.VIEW_3D(tab="My Tab", flags=(ACK.UI.add_panel_flag.DEFAULT_CLOSED,), order=2)
def my_panel_2(context, layout):
    layout.label(text="My Panel 200")

@ACK.UI.create_panel_from_func.VIEW_3D(tab="My Tab", order=3)
def my_panel_3(context, layout):
    layout.label(text="My Panel 300")
