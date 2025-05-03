from bpy.types import Context, UILayout, SpaceView3D, Region
from ...ackit import ACK
import bpy
import ctypes

from ...ackit.gpu.imm import rect_rounded_2d
from ...ackit.bcy.ui_layout import uiLayout, uiLayoutRoot
from ...ackit.bcy.DNA_screen_type import ARegion, Panel, PanelFlags, ARegionDoDrawFlags, ARegionRuntime


my_panel_1_cylayout: uiLayout | None = None
my_panel_1_layout: UILayout | None = None
my_panel_1_layout_id : int | None = None
my_panel_1_cyregion: ARegion | None = None
my_panel_1_region : Region | None = None
my_panel_1_region_id : int | None = None

@ACK.UI.Popover.from_function()
def my_popover(_context: Context, layout: UILayout):
    layout.label(text="My Nice Popover")


@ACK.UI.Panel.FromFunction.VIEW_3D(tab="My Tab", order=1) # flags={ACK.UI.PanelFlags.HIDE_HEADER}
def my_panel_1(context: Context, layout: UILayout):
    global my_panel_1_cyregion, my_panel_1_region, my_panel_1_region_id
    global my_panel_1_layout, my_panel_1_cylayout, my_panel_1_layout_id
    cyregion = ARegion.from_address(context.region.as_pointer())
    my_panel_1_cyregion = cyregion
    my_panel_1_region = context.region
    my_panel_1_region_id = id(context.region)

    layout.label(text="My Panel 1")
    obj = context.object
    if obj:
        layout.prop(obj, "name")
    layout.operator('render.render', text="Render")
    my_popover.draw_in_layout(layout, as_popover=True)

    '''if cyregion.runtime.contents.check_do_draw_flag(ARegionDoDrawFlags.DRAW):
        print("do_draw flag is set")
    else:
        print("do_draw flag is not set")

    if cyregion.runtime.contents.check_do_draw_paintcursor_flag(ARegionDoDrawFlags.DRAW):
        print("do_draw_paintcursor flag is set")
    else:
        print("do_draw_paintcursor flag is not set")'''

    box = layout.box()
    box.label(text="My Box")
    '''box.ui_units_x = 10
    box.ui_units_y = 20
    box.scale_x = 1.1
    box.scale_y = 1.1'''
    # box.operator('render.render', text="Render")
    cy_layout = uiLayout.from_address(box.as_pointer())  # id(box))
    # cy_layout.type = 8  # 28 << 9  # 1 item, 2 row, 4, text, 8 box, 10 row, 
    print(box, cy_layout)
    global my_panel_1_layout, my_panel_1_cylayout, my_panel_1_layout_id
    my_panel_1_cylayout = cy_layout
    my_panel_1_layout = box
    my_panel_1_layout_id = id(box)
    # root = uiLayoutRoot.from_address(cy_layout.root)
    # cy_layout = uiLayout.from_address(root.layout)
    print("pos:", cy_layout.x, cy_layout.y)
    print("size:", cy_layout.w, cy_layout.h)
    print("scale:", cy_layout.scale[0], cy_layout.scale[1])
    print("ui units:", cy_layout.units[0], cy_layout.units[1])
    print("space:", cy_layout.space)
    # print("states:", cy_layout.active, cy_layout.enabled, cy_layout.activate_init, cy_layout.active_default, cy_layout.redalert, cy_layout.keepaspect, cy_layout.variable_size, cy_layout.alignment, cy_layout.emboss)
    # print("roundbox rect:", cy_layout.roundbox.rect.xmin, cy_layout.roundbox.rect.xmax, cy_layout.roundbox.rect.ymin, cy_layout.roundbox.rect.ymax)
    # print("rounbox strwidth:", cy_layout.roundbox.strwidth)
    # print("rounbox alignnr:", cy_layout.roundbox.alignnr)
    # print("rounbox ofs:", cy_layout.roundbox.ofs)
    # print("rounbox pos:", cy_layout.roundbox.pos)
    # print("rounbox selsta:", cy_layout.roundbox.selsta)
    # print("rounbox selend:", cy_layout.roundbox.selend)
    # get the root, we need to cast it to uiLayoutRoot
    
    box.label(text=str(cy_layout.w))


@ACK.UI.Panel.FromFunction.VIEW_3D(tab="My Tab", flags={ACK.UI.PanelFlags.DEFAULT_CLOSED}, order=2)
def my_panel_2(_context: Context, layout: UILayout):
    layout.label(text="My Panel 200")

@ACK.UI.Panel.FromFunction.VIEW_3D(tab="My Tab", order=3)
def my_panel_3(_context: Context, layout: UILayout):
    layout.label(text="My Panel 300")


def draw_handler(context):
    global my_panel_1_cyregion, my_panel_1_region, my_panel_1_region_id
    global my_panel_1_layout, my_panel_1_cylayout, my_panel_1_layout_id
    # if my_panel_1_region_id is None or my_panel_1_region_id != id(bpy.context.region):
    #     return
    print("dh: region globals:", my_panel_1_cyregion, my_panel_1_region, my_panel_1_region_id)
    cy_region = my_panel_1_cyregion
    if cy_region is None:
        return
    last_panel_address = cy_region.panels.last
    last_panel = Panel.from_address(last_panel_address)
    if last_panel is None:
        return
    first_panel_address = cy_region.panels.first
    first_panel = Panel.from_address(first_panel_address)
    if first_panel is None:
        return
    cy_panel = None
    ok = False
    while 1:
        first_panel_address = cy_region.panels.first
        # Need to check against the actual memory address for the loop condition
        if cy_panel is None:
            cy_panel = first_panel
        else:
            current_address = ctypes.addressof(cy_panel)
            if current_address == last_panel_address:
                break
            cy_panel = cy_panel.next
            if cy_panel is None:
                break
            if isinstance(cy_panel, int):
                cy_panel = Panel.from_address(cy_panel)
            else:
                cy_panel = cy_panel.contents

        if cy_panel is None:
            break

        # Now safely access attributes
        panel_name = cy_panel.panelname
        # Check the actual panel name (adjust if needed based on Blender's internal naming)
        if panel_name != b"my_panel_1":
            continue
        
        # Check the runtime flag
        if cy_panel.is_closed:
                # Panel found but closed, stop searching in this region for this panel
            break
        
        # If we reach here, the panel is found and open
        ok = True
        break # Exit the loop once the correct panel is found


    if not my_panel_1_cyregion or not my_panel_1_region or not my_panel_1_region_id:
        # Reset the globals.
        '''my_panel_1_cyregion = None
        my_panel_1_region = None
        my_panel_1_region_id = None
        my_panel_1_cylayout = None
        my_panel_1_layout = None
        my_panel_1_layout_id = None'''
        print("dh: reset globals")
        return

    print("Nice panel found and it's open")

    
    print("dh: my_panel_1_layout_id:", my_panel_1_layout_id)
    print("dh: my_panel_1_layout:", my_panel_1_layout)
    print("dh: my_panel_1_cylayout:", my_panel_1_cylayout)
    if my_panel_1_layout is None:
        return
    cy_layout = my_panel_1_cylayout
    # Add check for cy_layout being None before accessing attributes
    if cy_layout is None:
        return
    print("dh: pos:", cy_layout.x, cy_layout.y)
    print("dh: size:", cy_layout.w, cy_layout.h)
    print("dh: scale:", cy_layout.scale[0], cy_layout.scale[1])
    print("dh: ui units:", cy_layout.units[0], cy_layout.units[1])
    print("dh: space:", cy_layout.space)
    # print("states:", cy_layout.active, cy_layout.enabled, cy_layout.activate_init, cy_layout.active_default, cy_layout.redalert, cy_layout.keepaspect, cy_layout.variable_size, cy_layout.alignment, cy_layout.emboss)
    # print("dh: roundbox rect:", cy_layout.roundbox.rect.xmin, cy_layout.roundbox.rect.xmax, cy_layout.roundbox.rect.ymin, cy_layout.roundbox.rect.ymax)
    # print("rounbox strwidth:", cy_layout.roundbox.strwidth)
    # print("rounbox alignnr:", cy_layout.roundbox.alignnr)
    # print("dh: roundbox ofs:", cy_layout.roundbox.ofs)
    # print("dh: roundbox pos:", cy_layout.roundbox.pos)
    
    print("dh: cy_panel:", cy_panel)
    print(f"\t- {cy_panel.panelname=}")
    print(f"\t- {cy_panel.ofsx=}")
    print(f"\t- {cy_panel.ofsy=}")
    print(f"\t- {cy_panel.sizex=}")
    print(f"\t- {cy_panel.sizey=}")
    print(f"\t- {cy_panel.blocksizex=}")
    print(f"\t- {cy_panel.blocksizey=}")
    print(f"\t- {cy_panel.labelofs=}")
    print(f"\t- {cy_panel.flag=}")
    print(f"\t- {cy_panel.type_flag=}")
    print(f"\t- {cy_panel.runtime_flag=}")
    print(f"\t- real size y: {cy_panel.get_panel_real_size_y()}")
    print(f"\t- real ofsy: {cy_panel.get_panel_real_ofsy()}")
    '''print(f"\t- {cy_panel.is_closed=}")
    print(f"\t- {cy_panel.is_dragging=}")
    print(f"\t- {cy_panel.is_pinned=}")
    print(f"\t- {cy_panel.is_selected=}")
    print(f"\t- {cy_panel.is_active=}")
    print(f"\t- {cy_panel.is_active_border=}")
    print(f"\t- {cy_panel.has_header=}")'''
    

    pos = (
        cy_layout.x + cy_layout.space,
        context.region.height + cy_layout.y - cy_layout.h * 0.5 - cy_layout.space * 0.5,
    )
    size = (
        cy_layout.w,
        cy_layout.h,
    )
    print("dh: rect pos:", pos[0], pos[1], "size:", size[0], size[1])
    rect_rounded_2d(pos[0], pos[1], size[0], size[1], 6, (.25, .8, .54, 0.25), segments_per_corner=4)

    print("dh: cy_region win/size:", cy_region.winx, cy_region.winy, cy_region.sizex, cy_region.sizey)
    
    return

    cy_region_runtime = cy_region.runtime.contents
    if cy_region_runtime is None:
        return
    draw_rct = cy_region_runtime.drawrct
    print("dh: cy_region runtime data:")
    print("\t- draw_rct:", draw_rct.xmin, draw_rct.xmax, draw_rct.ymin, draw_rct.ymax)
    print(f"\t- {cy_region_runtime.offset_x=}")
    print(f"\t- {cy_region_runtime.offset_y=}")
    print(f"\t- {cy_region_runtime.visible=}")
    print(f"\t- {cy_region_runtime.do_draw=}")
    print(f"\t- {cy_region_runtime.do_draw_paintcursor=}")

    '''draw_buffer = cy_region_runtime.draw_buffer
    if draw_buffer is None:
        return
    draw_buffer = draw_buffer.contents
    if draw_buffer is None:
        return
    # offscreen = draw_buffer.offscreen
    viewport = draw_buffer.viewport
    if viewport is None:
        return
    viewport = viewport.contents
    if viewport is None:
        return
    print("dh: draw buffer viewport:")
    print(f"\t- {viewport.size=}")
    print(f"\t- {viewport.flag=}")
    print(f"\t- {viewport.active_view=}")
    print(f"\t- {viewport.do_color_management=}")'''


to_unregister_draw_handler = []


def register():
    global to_unregister_draw_handler
    if to_unregister_draw_handler:
        unregister()
    # register draw handler in view3d UI.
    draw_callback = lambda : draw_handler(bpy.context)
    SpaceView3D.draw_handler_add(draw_callback, (), 'UI', 'POST_PIXEL')
    to_unregister_draw_handler.append((SpaceView3D, draw_callback, 'UI'))


def unregister():
    global to_unregister_draw_handler
    if not to_unregister_draw_handler:
        return
    for (space, handler, draw_type) in to_unregister_draw_handler:
        try:
            space.draw_handler_remove(handler, draw_type)
        except Exception as e:
            print(f"Error removing draw handler: {e}")
        
    to_unregister_draw_handler.clear()
