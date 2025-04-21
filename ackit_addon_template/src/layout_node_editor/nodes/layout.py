from typing import Dict, Any, Set, Optional
import bpy
from bpy import types as bpy_types

from ....ackit import ACK
from ..sockets import ElementSocket
from .base import BaseNode

# Make sure output node is imported if needed elsewhere, but not directly used here
# from .output import RootLayoutOutputNode

__all__ = [
    'RowLayoutNode',
    'ColumnLayoutNode',
    'BoxLayoutNode',
    'SplitLayoutNode',
    'SeparatorLayoutNode',
]

# --- Helper for Enum Properties ---
# Define items based on bpy.types.UILayout properties
alignment_items = [
    ('LEFT', "Left", "Align buttons towards the left", 'ALIGN_LEFT', 0),
    ('CENTER', "Center", "Align buttons towards the center", 'ALIGN_CENTER', 1),
    ('RIGHT', "Right", "Align buttons towards the right", 'ALIGN_RIGHT', 2),
    ('EXPAND', "Expand", "Expand buttons to fill the layout width", 'ALIGN_JUSTIFY', 3), # Icon approx
]

direction_items = [
    ('HORIZONTAL', "Horizontal", "Lay out items horizontally", 'TRACKING_FORWARDS', 0),
    ('VERTICAL', "Vertical", "Lay out items vertically", 'TRACKING_DOWNWARDS', 1),
]

emboss_items = [
    ('NORMAL', "Normal", "Draw UI elements normally (default)", 'HIDE_OFF', 0),
    ('BORDER', "Border", "Draw UI elements with a border", 'SNAP_VERTEX', 1), # Icon approx
    ('NONE', "None", "Draw UI elements flat, without emboss", 'SNAP_OFF', 2),
]


# --- Base Class for Layout Properties ---
class LayoutNodeBase(BaseNode):
    """ Base class to hold common layout properties """

    # --- Properties (Common UILayout settings) using Annotations ---
    alert: ACK.Prop.BOOL(name="Alert", default=False, description="Draw the layout with alert status")
    alignment: ACK.Prop.ENUM(name="Alignment", items=alignment_items, default='EXPAND', description="Alignment of elements within the layout")
    emboss: ACK.Prop.ENUM(name="Emboss", items=emboss_items, default='NORMAL', description="Emboss style for elements in the layout")
    enabled: ACK.Prop.BOOL(name="Enabled", default=True, description="Is the layout enabled (interactive)?")
    scale_x: ACK.Prop.FLOAT(name="Scale X", default=1.0, min=0.0, description="Scale factor for the layout width")
    scale_y: ACK.Prop.FLOAT(name="Scale Y", default=1.0, min=0.0, description="Scale factor for the layout height")
    ui_units_x: ACK.Prop.INT(name="UI Units X", default=0, min=0, description="Explicit width in UI units (0 uses automatic width)")
    ui_units_y: ACK.Prop.INT(name="UI Units Y", default=0, min=0, description="Explicit height in UI units (0 uses automatic height)")
    use_property_decorate: ACK.Prop.BOOL(name="Decorate Props", default=True, description="Draw decoration around properties")
    use_property_split: ACK.Prop.BOOL(name="Split Props", default=False, description="Split properties layout")

    # --- Helper Method ---
    def apply_layout_properties(self, layout: bpy.types.UILayout):
        """ Helper to apply common properties to a created layout """
        if not layout: return
        # Access properties directly using self.prop_name
        layout.alert = self.alert
        # Avoid setting default 'EXPAND' as it might override row/column behavior
        if self.alignment != 'EXPAND': layout.alignment = self.alignment
        # layout.direction = self.direction # Usually set by row/column/split itself
        if self.emboss != 'NORMAL': layout.emboss = self.emboss
        layout.enabled = self.enabled
        if self.scale_x != 1.0: layout.scale_x = self.scale_x
        if self.scale_y != 1.0: layout.scale_y = self.scale_y
        if self.ui_units_x > 0: layout.ui_units_x = self.ui_units_x
        if self.ui_units_y > 0: layout.ui_units_y = self.ui_units_y
        layout.use_property_decorate = self.use_property_decorate
        layout.use_property_split = self.use_property_split

    def draw_buttons_ext(self, context: bpy_types.Context, layout: bpy_types.UILayout):
        """ Draw the properties in the sidebar layout """
        layout.prop(self, 'alert')
        layout.prop(self, 'alignment')
        layout.prop(self, 'emboss')
        layout.prop(self, 'enabled')
        col = layout.column()
        col.prop(self, 'scale_x')
        col.prop(self, 'scale_y')
        col.separator()
        col.prop(self, 'ui_units_x')
        col.prop(self, 'ui_units_y')
        layout.prop(self, 'use_property_decorate')
        layout.prop(self, 'use_property_split')

@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Row", tooltip="Row layout node")
class RowLayoutNode(LayoutNodeBase, ACK.NE.NodeExec): # Inherit from base
    # --- Inputs ---
    Contents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False, description="Align elements within the row").tag_node_drawable() # Keep specific align for row()

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    Element = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> bpy_types.UILayout:
        return layout.row(align=self.align)


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Column", tooltip="Column layout node")
class ColumnLayoutNode(LayoutNodeBase, ACK.NE.NodeExec): # Inherit from base
    # --- Inputs ---
    Contents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False, description="Align elements within the column").tag_node_drawable()

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    Element = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> bpy_types.UILayout:
        return layout.column(align=self.align)


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Box", tooltip="Box layout node")
class BoxLayoutNode(LayoutNodeBase, ACK.NE.NodeExec): # Inherit from base
    # --- Inputs ---
    InContents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> bpy_types.UILayout:
        return layout.box()


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Split", tooltip="Split layout node")
class SplitLayoutNode(LayoutNodeBase, ACK.NE.NodeExec): # Inherit from base
    # --- Inputs ---
    InLeft = ACK.NE.InputSocket(ElementSocket, label="Left")
    InRight = ACK.NE.InputSocket(ElementSocket, label="Right")

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False, description="Align the split layout within its parent").tag_node_drawable(order=0)
    factor = ACK.PropTyped.Float(name="Factor", default=0.5, min=0.0, max=1.0, description="Split factor (percentage for the left side)").tag_node_drawable(order=1)

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> bpy_types.UILayout:
        return layout.split(factor=self.factor, align=self.align)


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Separator", tooltip="Adds a separator line to the layout")
class SeparatorLayoutNode(ACK.NE.NodeExec):
    # --- Properties ---
    factor = ACK.PropTyped.Float(name="Factor", default=0.5, min=0.0, max=10.0, description="Split factor (percentage for the left side)").tag_node_drawable(order=0)

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> None:
        layout.separator(factor=self.factor)


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Column Flow", tooltip="Column Flow layout node")
class ColumnFlowLayoutNode(LayoutNodeBase, ACK.NE.NodeExec): # Inherit from base
    # --- Inputs ---
    InContents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)

    # --- Properties ---
    columns = ACK.PropTyped.Int(name="Columns", default=0, min=0, soft_max=10, description="Number of columns, 0 is automatic").tag_node_drawable(order=0)
    align = ACK.PropTyped.Bool(name="Align", default=False, description="Align columns within the layout").tag_node_drawable(order=1) # Keep specific align for row()

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> bpy_types.UILayout:
        return layout.column_flow(columns=self.columns, align=self.align)


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Grid Flow", tooltip="Grid Flow layout node")
class GridFlowLayoutNode(LayoutNodeBase, ACK.NE.NodeExec): # Inherit from base
    # --- Inputs ---
    InContents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)

    # --- Properties ---
    row_major = ACK.PropTyped.Bool(name="Row Major", default=True, description="If true, the grid will be laid out row by row, otherwise column by column").tag_node_drawable(order=0)
    columns = ACK.PropTyped.Int(name="Columns", default=0, soft_min=-10, soft_max=10, description="Number of columns, 0 is automatic, negative are automatic multiple numbers along major axis (eg. -2 will only produce 2, 4, 6 etc.)").tag_node_drawable(order=1)
    even_columns = ACK.PropTyped.Bool(name="Even Columns", default=True, description="If true, the columns will be evened out to the nearest whole number").tag_node_drawable(order=2)
    even_rows = ACK.PropTyped.Bool(name="Even Rows", default=True, description="If true, the rows will be evened out to the nearest whole number").tag_node_drawable(order=3)
    align = ACK.PropTyped.Bool(name="Align", default=False, description="Align grid slots within the layout").tag_node_drawable(order=4) # Keep specific align for row()

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> bpy_types.UILayout:
        return layout.grid_flow(row_major=self.row_major, columns=self.columns, even_columns=self.even_columns, even_rows=self.even_rows, align=self.align)
