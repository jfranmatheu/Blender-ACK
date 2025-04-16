from typing import Dict, Any
import bpy

# Import ACK from the root ackit library
from ....ackit import ACK
# Import LayoutSocket from the sockets file in the same editor definition
from ..sockets import LayoutSocket

__all__ = [
    'LabelNode',
    'OperatorNode',
]


@ACK.NE.add_node_to_category("Elements")
@ACK.NE.add_node_metadata(label="Label", tooltip="Display a text label in a layout", icon='FONT_DATA')
class LabelNode(ACK.NE.NodeExec):
    """Node that draws a label into a layout using a node property."""
    # --- Inputs ---
    # Expects a layout object to draw into.
    InLayout = ACK.NE.InputSocket(LayoutSocket)

    # --- Properties ---
    # The text to display. Configured directly on the node UI.
    text: ACK.PropTyped.String(name="Text", default="Label")
    icon: ACK.PropTyped.String(name="Icon", default="NONE")

    # --- Outputs ---
    # Passes the input layout through.
    OutLayout = ACK.NE.OutputSocket(LayoutSocket)

    def execute(self, *args, **kwargs):
        layout = self.InLayout.value
        if layout is not None:
            layout = layout.label(text=self.text, icon=self.icon)
        self.OutLayout.set_value(layout)


@ACK.NE.add_node_to_category("Elements")
@ACK.NE.add_node_metadata(label="Operator Button", tooltip="Display a button that runs an operator", icon='PLAY')
class OperatorNode(ACK.NE.NodeExec):
    """Node that draws an operator button into a layout using node properties."""
    # --- Inputs ---
    # Expects a layout object to draw into.
    InLayout = ACK.NE.InputSocket(LayoutSocket)

    # --- Properties ---
    # Configured directly on the node UI.
    operator_id: ACK.PropTyped.String(name="Operator ID", default="wm.operator_defaults", description="The bl_idname of the operator to run")
    text_override: ACK.PropTyped.String(name="Button Text", default="", description="Optional text override for the button (uses operator label if empty)")
    icon_override: ACK.PropTyped.String(name="Button Icon", default="", description="Optional icon override (e.g., 'CANCEL', uses operator icon if empty)")

    # --- Outputs ---
    # Passes the input layout through.
    OutLayout = ACK.NE.OutputSocket(LayoutSocket)

    def execute(self, *args, **kwargs):
        layout = self.InLayout.value
        if layout is not None:
            layout = layout.operator(self.operator_id, text=self.text_override, icon=self.icon_override)
        self.OutLayout.set_value(layout)
