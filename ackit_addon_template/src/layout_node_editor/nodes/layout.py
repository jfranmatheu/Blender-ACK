from typing import Dict, Any, Set, Optional
import bpy
from bpy import types as bpy_types

from ....ackit import ACK
from ..sockets import ElementSocket

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
class LayoutNodeBase:
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

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Self")

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

    # Default execute - subclasses should override to create specific layout type
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        print(f"Warning: LayoutNodeBase execute called directly for {self.name}. Subclass should override.")
        parent_layout = kwargs.get('parent_layout')
        return {'parent_layout': parent_layout} # Pass through

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
    InContents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False, description="Align elements within the row").tag_node_drawable() # Keep specific align for row()

    # Inherits common properties and Element output from LayoutNodeBase

    # Execute is called by _internal_execute
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')
        if not parent_layout:
            print(f"Warning: RowLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None
        my_layout = parent_layout.row(align=self.align)
        self.apply_layout_properties(my_layout) # Apply common props
        return {'parent_layout': my_layout}


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Column", tooltip="Column layout node")
class ColumnLayoutNode(LayoutNodeBase, ACK.NE.NodeExec): # Inherit from base
    # --- Inputs ---
    InContents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False, description="Align elements within the column").tag_node_drawable()

    # Inherits common properties and Element output from LayoutNodeBase

    # Execute is called by _internal_execute
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')
        if not parent_layout:
            print(f"Warning: ColumnLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None
        my_layout = parent_layout.column(align=self.align)
        self.apply_layout_properties(my_layout) # Apply common props
        return {'parent_layout': my_layout}


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Box", tooltip="Box layout node")
class BoxLayoutNode(LayoutNodeBase, ACK.NE.NodeExec): # Inherit from base
    # --- Inputs ---
    InContents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)

    # Inherits common properties and Element output from LayoutNodeBase

    # Execute is called by _internal_execute
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')
        if not parent_layout:
            print(f"Warning: BoxLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None
        my_layout = parent_layout.box()
        self.apply_layout_properties(my_layout) # Apply common props
        return {'parent_layout': my_layout}


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Split", tooltip="Split layout node")
class SplitLayoutNode(LayoutNodeBase, ACK.NE.NodeExec): # Inherit from base
    # --- Inputs ---
    InLeft = ACK.NE.InputSocket(ElementSocket, label="Left")
    InRight = ACK.NE.InputSocket(ElementSocket, label="Right")

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False, description="Align the split layout within its parent").tag_node_drawable(order=0)
    factor = ACK.PropTyped.Float(name="Factor", default=0.5, min=0.0, max=1.0, description="Split factor (percentage for the left side)").tag_node_drawable(order=1)

    # Inherits common properties and Element output from LayoutNodeBase

    # Execute is called by _internal_execute
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')
        if not parent_layout:
            print(f"Warning: SplitLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None
        # Create the specific split layout
        split_layout = parent_layout.split(factor=self.factor, align=self.align)
        # Apply common properties from base class helper
        self.apply_layout_properties(split_layout)
        # Return the created layout for children to use
        return {'parent_layout': split_layout}



@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Separator", tooltip="Adds a separator line to the layout")
class SeparatorLayoutNode(ACK.NE.NodeExec):

    # --- Inputs ---
    # Needs an input to receive the execution flow and parent_layout
    #InElement = ACK.NE.InputSocket(ElementSocket, label="Element")

    # --- Properties ---
    factor = ACK.PropTyped.Float(name="Factor", default=0.5, min=0.0, max=10.0, description="Split factor (percentage for the left side)").tag_node_drawable(order=0)

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout: bpy_types.UILayout = kwargs.get('parent_layout')
        if not parent_layout:
            print(f"Warning: SeparatorLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None
        # Use factor property correctly
        parent_layout.separator(factor=self.factor)
        # Return None as it doesn't provide a new layout context
        return None
