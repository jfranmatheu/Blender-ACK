from ....ackit import ACK
from ..sockets import LayoutSocket, ElementSocket

from bpy import types as bpy_types
from typing import Dict, Any


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Row", tooltip="Row layout node")
class RowLayoutNode(ACK.NE.NodeExec):
    # --- Inputs ---
    # Receives the parent layout context
    InParentLayout = ACK.NE.InputSocket(LayoutSocket, label="Parent")
    # Receives connections from child UI elements (MultiInput allows multiple)
    InElements = ACK.NE.InputSocket(ElementSocket, label="Elements", multi=True)

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False)

    # --- Outputs ---
    # Passes the created row layout context downstream
    OutLayout = ACK.NE.OutputSocket(LayoutSocket, label="Row Layout")


    def execute(self, context, layout, **kwargs):
        # 1. Get the parent layout context to draw into
        # Use the value from InParentLayout if connected, otherwise use the layout passed to the tree execution
        parent_layout = self.InParentLayout.value or layout
        if not parent_layout:
            print(f"Warning: RowLayoutNode '{self.name}' has no parent layout context.")
            self.OutLayout.set_value(None) # Pass None downstream
            return # Cannot proceed without a layout to draw into

        # 2. Create the specific layout (the row)
        row_layout = parent_layout.row(align=self.align)

        # 3. Execute child elements connected to InElements
        # The MultiInputSocket's value property conveniently returns a list of connected source nodes
        child_element_nodes = self.InElements.get_connected_nodes()
        if child_element_nodes:
            for child_node in child_element_nodes:
                if child_node and hasattr(child_node, 'execute'):
                    try:
                        print(f"RowLayoutNode '{self.name}' executing child: {child_node.name}")
                        # *** Directly call execute on the child node ***
                        # Pass the newly created row_layout as the context for the child
                        child_node.execute(context, layout=row_layout, _called_by_layout=True, **kwargs)
                    except Exception as e:
                        import traceback
                        print(f"Error executing child node '{child_node.name}' from '{self.name}': {e}")
                        traceback.print_exc()
                elif child_node:
                     print(f"Warning: Connected node '{child_node.name}' to '{self.name}.InElements' has no execute method.")


        # 4. Set the output value to the created row layout
        # This allows chaining: Row -> Column (Column.InParentLayout <- Row.OutLayout)
        self.OutLayout.set_value(row_layout)

@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Column", tooltip="Column layout node")
class ColumnLayoutNode(ACK.NE.NodeExec):
    InParentLayout = ACK.NE.InputSocket(LayoutSocket, label="Parent")
    InElements = ACK.NE.InputSocket(ElementSocket, label="Elements", multi=True)
    align = ACK.PropTyped.Bool(name="Align", default=False)
    OutLayout = ACK.NE.OutputSocket(LayoutSocket, label="Column Layout")

    def execute(self, context, layout, **kwargs):
        parent_layout = self.InParentLayout.value or layout
        if not parent_layout:
            print(f"Warning: ColumnLayoutNode '{self.name}' has no parent layout context.")
            self.OutLayout.set_value(None)
            return
        col_layout = parent_layout.column(align=self.align)
        child_element_nodes = self.InElements.get_connected_nodes()
        if child_element_nodes:
            for child_node in child_element_nodes:
                if child_node and hasattr(child_node, 'execute'):
                    try:
                        print(f"ColumnLayoutNode '{self.name}' executing child: {child_node.name}")
                        child_node.execute(context, layout=col_layout, _called_by_layout=True, **kwargs)
                    except Exception as e:
                        import traceback
                        print(f"Error executing child node '{child_node.name}' from '{self.name}': {e}")
                        traceback.print_exc()
                elif child_node:
                     print(f"Warning: Connected node '{child_node.name}' to '{self.name}.InElements' has no execute method.")
        self.OutLayout.set_value(col_layout)


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Box", tooltip="Box layout node")
class BoxLayoutNode(ACK.NE.NodeExec):
    InParentLayout = ACK.NE.InputSocket(LayoutSocket, label="Parent")
    InElements = ACK.NE.InputSocket(ElementSocket, label="Elements", multi=True)
    OutLayout = ACK.NE.OutputSocket(LayoutSocket, label="Box Layout")

    def execute(self, context, layout, **kwargs):
        parent_layout = self.InParentLayout.value or layout
        if not parent_layout:
            print(f"Warning: BoxLayoutNode '{self.name}' has no parent layout context.")
            self.OutLayout.set_value(None)
            return
        box_layout = parent_layout.box()
        child_element_nodes = self.InElements.get_connected_nodes()
        if child_element_nodes:
            for child_node in child_element_nodes:
                if child_node and hasattr(child_node, 'execute'):
                    try:
                        print(f"BoxLayoutNode '{self.name}' executing child: {child_node.name}")
                        child_node.execute(context, layout=box_layout, _called_by_layout=True, **kwargs)
                    except Exception as e:
                        import traceback
                        print(f"Error executing child node '{child_node.name}' from '{self.name}': {e}")
                        traceback.print_exc()
                elif child_node:
                     print(f"Warning: Connected node '{child_node.name}' to '{self.name}.InElements' has no execute method.")
        self.OutLayout.set_value(box_layout)


# Refined SplitLayoutNode
@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Split", tooltip="Split layout into two areas (typically left/right)")
class SplitLayoutNode(ACK.NE.NodeExec):
    # --- Inputs ---
    # Receives the parent layout context
    InParentLayout = ACK.NE.InputSocket(LayoutSocket, label="Parent")

    # --- Properties ---
    align = ACK.PropTyped.Bool(
        name="Align",
        default=False,
        description="Align elements within the split areas"
    )
    factor = ACK.PropTyped.Float(
        name="Factor",
        default=0.5,
        min=0.0,
        max=1.0,
        description="Split point (0.0 to 1.0)"
    )

    # --- Outputs ---
    # Output separate layout contexts for the two areas created by the split
    OutLeft = ACK.NE.OutputSocket(LayoutSocket, label="Left Layout")
    OutRight = ACK.NE.OutputSocket(LayoutSocket, label="Right Layout")
    # Note: Depending on context, 'Left'/'Right' might behave as 'Top'/'Bottom'

    def execute(self, context, layout, **kwargs):
        parent_layout = self.InParentLayout.value or layout
        if not parent_layout:
            print(f"Warning: SplitLayoutNode '{self.name}' has no parent layout context.")
            # Set both outputs to None if parent is invalid
            self.OutLeft.set_value(None)
            self.OutRight.set_value(None)
            return

        # 1. Create the split layout object
        # The 'split' object itself is a UILayout that manages the split areas
        split = parent_layout.split(factor=self.factor, align=self.align)

        # 2. Create distinct layout areas within the split
        # Typically, you'd create a column or row in each part of the split.
        # Let's default to creating columns, as that's common.
        # These are the layout contexts we will pass downstream.
        left_layout_area = split.column()
        right_layout_area = split.column()

        # 3. Set the output socket values
        self.OutLeft.set_value(left_layout_area)
        self.OutRight.set_value(right_layout_area)

        # Note: This node itself doesn't execute child elements directly.
        # Users connect other Layout nodes (Row, Column, Box) to OutLeft/OutRight,
        # and those nodes will handle executing their connected elements.
