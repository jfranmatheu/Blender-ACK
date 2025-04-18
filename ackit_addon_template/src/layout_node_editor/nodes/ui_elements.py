from typing import Dict, Any, Set, Optional
import bpy
from bpy import types as bpy_types

# Import ACK from the root ackit library
from ....ackit import ACK
# Import ElementSocket from the sockets file in the same editor definition
from ..sockets import ElementSocket
from .enums import search_icon_items, icons_ids_set

__all__ = [
    'LabelNode',
    'OperatorNode',
]


@ACK.NE.add_node_to_category("Elements")
@ACK.NE.add_node_metadata(label="Label", tooltip="Display a text label in a layout", icon='FONT_DATA')
class LabelNode(ACK.NE.NodeExec):
    """Node that draws a label into a layout."""
    # --- Inputs --- (None)

    # --- Properties ---
    text = ACK.PropTyped.String(name="Text", default="Label").tag_node_drawable(order=0)
    icon = ACK.PropTyped.String(name="Icon", default="NONE", search=search_icon_items).tag_node_drawable(order=1)

    # --- Outputs ---
    # Used to connect to LayoutNode.InContents (Child -> Parent)
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Element")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, root_layout: bpy_types.UILayout, **kwargs) -> Optional[Dict[str, Any]]: # Return type is dict or None
        parent_layout = kwargs.get('parent_layout')

        if parent_layout:
            parent_layout.label(text=self.text, icon=self.icon if self.icon and self.icon in icons_ids_set else 'NONE')
        else:
            print(f"Warning: LabelNode '{self.name}' executed without 'parent_layout' in kwargs.")
        # Return None or {} as this node doesn't change the context for subsequent children
        return None


@ACK.NE.add_node_to_category("Elements")
@ACK.NE.add_node_metadata(label="Operator Button", tooltip="Display a button that runs an operator", icon='PLAY')
class OperatorNode(ACK.NE.NodeExec):
    """Node that draws an operator button into a layout."""
    # --- Inputs --- (None)

    # --- Properties ---
    operator_id = ACK.PropTyped.String(name="Operator ID", default="wm.operator_defaults", description="The bl_idname of the operator to run").tag_node_drawable(order=0)
    text_override = ACK.PropTyped.String(name="Text", default="", description="Optional text override for the button (uses operator label if empty)").tag_node_drawable(order=1)
    icon = ACK.PropTyped.String(name="Icon", default="NONE", search=search_icon_items).tag_node_drawable(order=2)

    # --- Outputs ---
    # Used to connect to LayoutNode.InContents (Child -> Parent)
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Element")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, root_layout: bpy_types.UILayout, **kwargs) -> Optional[Dict[str, Any]]: # Return type is dict or None
        parent_layout = kwargs.get('parent_layout')

        if parent_layout:
            icon = self.icon if self.icon and self.icon in icons_ids_set else 'NONE'
            parent_layout.operator(self.operator_id, text=self.text_override or None, icon=icon)
        else:
            print(f"Warning: OperatorNode '{self.name}' executed without 'parent_layout' in kwargs.")
        # Return None or {}
        return None
