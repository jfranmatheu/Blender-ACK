from typing import Dict, Any, Set, Optional
import bpy
from bpy import types as bpy_types

# Import ACK from the root ackit library
from ....ackit import ACK
# Import ElementSocket from the sockets file in the same editor definition
from ..sockets import ElementSocket

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
    text = ACK.PropTyped.String(name="Text", default="Label")
    icon = ACK.PropTyped.String(name="Icon", default="NONE")

    # --- Outputs ---
    # Used to connect to LayoutNode.InContents (Child -> Parent)
    Element = ACK.NE.OutputSocket(ElementSocket)

    # Execute is called by _internal_execute
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]: # Return type is dict or None
        parent_layout = kwargs.get('parent_layout')
        context = kwargs.get('context') # Keep context if needed

        if parent_layout:
            parent_layout.label(text=self.text, icon=self.icon)
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
    operator_id = ACK.PropTyped.String(name="Operator ID", default="wm.operator_defaults")
    text_override = ACK.PropTyped.String(name="Button Text", default="")
    icon_override = ACK.PropTyped.String(name="Button Icon", default="")

    # --- Outputs ---
    # Used to connect to LayoutNode.InContents (Child -> Parent)
    Element = ACK.NE.OutputSocket(ElementSocket)

    # Execute is called by _internal_execute
    def execute(self, *args, **kwargs) -> Optional[Dict[str, Any]]: # Return type is dict or None
        parent_layout = kwargs.get('parent_layout')
        context = kwargs.get('context') # Keep context if needed

        if parent_layout:
            text = self.text_override or None
            icon = self.icon_override or 'NONE'
            parent_layout.operator(self.operator_id, text=text, icon=icon)
        else:
            print(f"Warning: OperatorNode '{self.name}' executed without 'parent_layout' in kwargs.")
        # Return None or {}
        return None
