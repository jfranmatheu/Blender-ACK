from ...ackit import ACK


@ACK.Register.FromFunction.POPOVER()
def my_popover(context, layout):
    layout.label(text="My Popover")


@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="My Tab", flags=(ACK.Flags.PANEL.HIDE_HEADER,), order=1)
def my_panel_1(context, layout):
    layout.label(text="My Panel 1")
    layout.operator('render.render', text="Render")
    my_popover.draw_in_layout(layout)

@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="My Tab", flags=(ACK.Flags.PANEL.DEFAULT_CLOSED,), order=2)
def my_panel_2(context, layout):
    layout.label(text="My Panel 200")

@ACK.Register.FromFunction.PANEL.VIEW_3D(tab="My Tab", order=3)
def my_panel_3(context, layout):
    layout.label(text="My Panel 300")
