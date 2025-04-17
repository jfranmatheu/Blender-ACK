from ...ackit import ACK
from bpy import types as bpy_types

# Import the output node to reference its bl_idname
from .nodes.output import RootLayoutOutputNode

class UILayoutNodeTree(ACK.NE.TreeExec):
    bl_label = "UI Layout Node Tree"
    # Define the ID name of the node that acts as the execution root
    output_node_type = RootLayoutOutputNode

    # The execute method now relies on the base class finding and starting from the output node
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout, **additional_kwargs) -> None:
        # Pass context and layout as keyword arguments for the base execute method
        super().execute(context, layout, **additional_kwargs)
