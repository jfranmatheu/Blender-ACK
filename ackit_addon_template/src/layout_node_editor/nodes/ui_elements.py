from typing import Dict, Any
import bpy

# Import ACK from the root ackit library
from ....ackit import ACK
# Import LayoutSocket from the sockets file in the same editor definition
from ..sockets import ElementSocket

__all__ = [
    'LabelNode',
    'OperatorNode',
]


@ACK.NE.add_node_to_category("Elements")
@ACK.NE.add_node_metadata(label="Label", tooltip="Display a text label in a layout", icon='FONT_DATA')
class LabelNode(ACK.NE.NodeExec):
    """Node that draws a label into a layout using a node property."""
    # --- Inputs ---

    # --- Properties ---
    # The text to display. Configured directly on the node UI.
    text = ACK.PropTyped.String(name="Text", default="Label")
    icon = ACK.PropTyped.String(name="Icon", default="NONE")

    # --- Outputs ---
    # Passes the input layout through.
    Element = ACK.NE.OutputSocket(ElementSocket)

    def execute(self, context, layout, _called_by_layout=False, **kwargs):
        # Only draw if called by a layout node AND a valid layout is provided
        if not _called_by_layout:
            # print(f"LabelNode '{self.name}' skipped (called by main loop).")
            return # Do nothing if called by the main NodeTreeExec loop

        if layout:
            # print(f"LabelNode '{self.name}' drawing.")
            layout.label(text=self.text, icon=self.icon)
        else:
            # This case should ideally not happen if called by a layout node
            print(f"Warning: LabelNode '{self.name}' called by layout parent but received no layout.")


@ACK.NE.add_node_to_category("Elements")
@ACK.NE.add_node_metadata(label="Operator Button", tooltip="Display a button that runs an operator", icon='PLAY')
class OperatorNode(ACK.NE.NodeExec):
    """Node that draws an operator button into a layout using node properties."""
    # --- Inputs ---

    # --- Properties ---
    # Configured directly on the node UI.
    operator_id = ACK.PropTyped.String(name="Operator ID", default="wm.operator_defaults", description="The bl_idname of the operator to run")
    text_override = ACK.PropTyped.String(name="Button Text", default="", description="Optional text override for the button (uses operator label if empty)")
    icon_override = ACK.PropTyped.String(name="Button Icon", default="", description="Optional icon override (e.g., 'CANCEL', uses operator icon if empty)")

    # --- Outputs ---
    Element = ACK.NE.OutputSocket(ElementSocket)

    def execute(self, context, layout, _called_by_layout=False, **kwargs):
        # Only draw if called by a layout node AND a valid layout is provided
        if not _called_by_layout:
            # print(f"OperatorNode '{self.name}' skipped (called by main loop).")
            return # Do nothing if called by the main NodeTreeExec loop

        if layout:
            # print(f"OperatorNode '{self.name}' drawing.")
            # Ensure text/icon are None if empty string, as layout.operator prefers None
            text = self.text_override or None
            icon = self.icon_override or 'NONE' # Operator default icon is 'NONE'
            layout.operator(self.operator_id, text=text, icon=icon)
        else:
            print(f"Warning: OperatorNode '{self.name}' called by layout parent but received no layout.")
