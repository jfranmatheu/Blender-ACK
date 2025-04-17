from typing import Set
import bpy

from ....ackit import ACK
from ..sockets import ElementSocket

__all__ = ['RootLayoutOutputNode']

@ACK.NE.add_node_to_category("Output") # Or maybe just "Layout"?
@ACK.NE.add_node_metadata(label="Root Layout Output", tooltip="Defines the root of the UI layout execution")
class RootLayoutOutputNode(ACK.NE.NodeExec):

    # --- Inputs ---
    # Receives the final element/layout to be drawn directly into the initial layout
    InElement = ACK.NE.InputSocket(ElementSocket, label="Root Element")

    # --- Outputs --- (None)

    # This node's execute is called by _internal_execute
    # It receives the initial layout from the NodeTreeExec call
    def execute(self, context: bpy.types.Context, parent_layout: bpy.types.UILayout | None, **kwargs):
        # The 'parent_layout' received here IS the initial layout for the whole tree.
        # We just need to pass it down to the connected child node.
        # The base _internal_execute will handle calling the child connected to InElement.

        if not parent_layout:
            print(f"Error: RootLayoutOutputNode '{self.name}' did not receive an initial layout context.")
            return None # Cannot proceed

        if not self.InElement.is_linked:
            print(f"Warning: RootLayoutOutputNode '{self.name}' has nothing connected to InElement.")
            # Return the parent_layout anyway? Or None? Let's return None to stop drawing.
            return None

        # print(f"RootLayoutOutputNode '{self.name}' execute returning initial layout: {parent_layout}")
        # Return the layout that the connected child should draw into.
        return {'parent_layout': parent_layout}
