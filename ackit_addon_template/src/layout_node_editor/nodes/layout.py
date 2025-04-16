from ....ackit import ACK
from ..sockets import LayoutSocket

from bpy import types as bpy_types
from typing import Dict, Any


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Row", tooltip="Row layout node")
class RowLayoutNode(ACK.NE.NodeExec):
    # --- Inputs ---
    InLayout = ACK.NE.InputSocket(LayoutSocket)

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False)

    # --- Outputs ---
    OutLayout = ACK.NE.OutputSocket(LayoutSocket)


    def execute(self, *args, **kwargs):
        layout = self.InLayout.value
        if layout is not None:
            layout = layout.row(align=self.align)
        self.OutLayout.set_value(layout)

@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Column", tooltip="Column layout node")
class ColumnLayoutNode(ACK.NE.NodeExec):
    # --- Inputs ---
    InLayout = ACK.NE.InputSocket(LayoutSocket)

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False)

    # --- Outputs ---
    OutLayout = ACK.NE.OutputSocket(LayoutSocket)


    def execute(self, *args, **kwargs):
        layout = self.InLayout.value
        if layout is not None:
            layout = layout.column(align=self.align)
        self.OutLayout.set_value(layout)


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Box", tooltip="Box layout node")
class BoxLayoutNode(ACK.NE.NodeExec):
    # --- Inputs ---
    InLayout = ACK.NE.InputSocket(LayoutSocket)

    # --- Outputs ---
    OutLayout = ACK.NE.OutputSocket(LayoutSocket)

    def execute(self, *args, **kwargs):
        layout = self.InLayout.value
        if layout is not None:
            layout = layout.box()
        self.OutLayout.set_value(layout)


@ACK.NE.add_node_to_category("Layout")
@ACK.NE.add_node_metadata(label="Split", tooltip="Split layout node")
class SplitLayoutNode(ACK.NE.NodeExec):
    # --- In    puts ---
    InLayout = ACK.NE.InputSocket(LayoutSocket)

    # --- Properties ---
    align = ACK.PropTyped.Bool(name="Align", default=False)
    factor = ACK.PropTyped.Float(name="Factor", default=0.5)

    # --- Outputs ---
    OutLayout = ACK.NE.OutputSocket(LayoutSocket)

    def execute(self, *args, **kwargs):
        layout = self.InLayout.value
        if layout is not None:
            split = layout.split(align=self.align, factor=self.factor)
            self.OutLayout.set_value(split)
