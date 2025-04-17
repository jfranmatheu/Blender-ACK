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
    # 'SplitLayoutNode', # Removed for now
]


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Row", tooltip="Row layout node")
class RowLayoutNode(ACK.NE.NodeExec):
    # --- Inputs ---
    # Unified input for child elements and nested layouts (Child -> Parent)
    InContents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False)

    # --- Outputs ---
    # Allows this node to be connected as a child to another layout's InContents
    Element = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, root_layout: bpy_types.UILayout, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')

        if not parent_layout:
            print(f"Warning: RowLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None # Cannot create layout

        # Create the specific layout
        my_layout = parent_layout.row(align=self.align)

        # Return the arguments for children, providing the new layout context
        return {'parent_layout': my_layout}
        # Child execution is handled by base _internal_execute after this returns


# --- Update ColumnLayoutNode similarly ---
@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Column", tooltip="Column layout node")
class ColumnLayoutNode(ACK.NE.NodeExec):
    InContents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)
    align = ACK.PropTyped.Bool(name="Align", default=False)
    Element = ACK.NE.OutputSocket(ElementSocket, label="Self")

    def execute(self, context: bpy_types.Context, root_layout: bpy_types.UILayout, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')

        if not parent_layout:
            print(f"Warning: ColumnLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None
        my_layout = parent_layout.column(align=self.align)
        return {'parent_layout': my_layout}


# --- Update BoxLayoutNode similarly ---
@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Box", tooltip="Box layout node")
class BoxLayoutNode(ACK.NE.NodeExec):
    InContents = ACK.NE.InputSocket(ElementSocket, label="Contents", multi=True)
    Element = ACK.NE.OutputSocket(ElementSocket, label="Self")

    def execute(self, context: bpy_types.Context, root_layout: bpy_types.UILayout, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')

        if not parent_layout:
            print(f"Warning: BoxLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None
        my_layout = parent_layout.box()
        return {'parent_layout': my_layout}


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Split", tooltip="Split layout node (divides into two columns)")
class SplitLayoutNode(ACK.NE.NodeExec):
    # --- Inputs ---
    # Two distinct inputs for the left and right side of the split
    InLeft = ACK.NE.InputSocket(ElementSocket, label="Left")
    InRight = ACK.NE.InputSocket(ElementSocket, label="Right")

    # --- Properties ---
    factor = ACK.PropTyped.Float(name="Factor", default=0.5, min=0.0, max=1.0, description="Split factor (percentage for the left side)")
    align = ACK.PropTyped.Bool(name="Align", default=False, description="Align the split layout within its parent")

    # --- Outputs ---
    # Allows this node to be connected as a child to another layout's InContents/Input
    Element = ACK.NE.OutputSocket(ElementSocket, label="Self")

    # Execute is called by _internal_execute
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')
        # context = kwargs.get('context') # Extract context if needed later

        if not parent_layout:
            print(f"Warning: SplitLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None # Cannot create layout

        # Create the specific split layout
        # Note: The children connected to InLeft/InRight will draw within this split layout.
        # Blender's split layout automatically handles placing subsequent elements
        # added to it into the left or right column based on internal state.
        # However, our node system executes children explicitly. The base class will
        # execute InLeft's child first, then InRight's child. Both will receive
        # the *same* split_layout object as their 'parent_layout'.
        # This works because adding elements to a split layout alternates columns.
        split_layout = parent_layout.split(factor=self.factor, align=self.align)

        # Return the created layout for children to use
        # The base _internal_execute will pass this to children connected to InLeft and InRight
        return {'parent_layout': split_layout}
