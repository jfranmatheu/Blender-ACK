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
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')
        context = kwargs.get('context') # Keep context if needed

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

    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')
        context = kwargs.get('context') # Keep context if needed

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

    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        parent_layout = kwargs.get('parent_layout')
        context = kwargs.get('context') # Keep context if needed

        if not parent_layout:
            print(f"Warning: BoxLayoutNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None
        my_layout = parent_layout.box()
        return {'parent_layout': my_layout}

# --- SplitLayoutNode removed ---
