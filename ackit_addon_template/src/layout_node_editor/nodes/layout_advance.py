from typing import Dict, Any, Set, Optional, Tuple
import bpy
from bpy import types as bpy_types

from ....ackit import ACK
from ..sockets import ElementSocket

from .enums import search_icon_items, icons_ids_set
from .base import BaseNode

# Make sure output node is imported if needed elsewhere, but not directly used here
# from .output import RootLayoutOutputNode

__all__ = [
    'SectionLayoutNode',
    'PanelLayoutNode',
]


class AdvancedLayoutNode(BaseNode):
    pass


@ACK.NE.add_node_to_category("Layout/Advanced")
@ACK.NE.add_node_metadata(label="Section", tooltip="Section layout node")
class SectionLayoutNode(AdvancedLayoutNode, ACK.NE.NodeExec):
    # --- Inputs ---
    InHeader = ACK.NE.InputSocket(ElementSocket, label="Header", multi=True)
    InContent = ACK.NE.InputSocket(ElementSocket, label="Content", multi=True)

    # --- Properties ---
    align_content = ACK.PropTyped.Bool(name="Align Content", default=False, description="Align the split layout within its parent").tag_node_drawable(order=0)

    header_text = ACK.PropTyped.String(name="Text", default="Header Title").tag_node_drawable(order=1, poll=lambda node, _ctx: not node.InHeader.is_linked)
    header_icon = ACK.PropTyped.String(name="Icon", default="NONE", search=search_icon_items).tag_node_drawable(order=2, poll=lambda node, _ctx: not node.InHeader.is_linked)

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Self")

    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> Tuple[bpy_types.UILayout, bpy_types.UILayout]:
        draw_default_header = not self.InHeader.is_linked

        # Create the layouts
        section_layout = layout.column(align=True) # Main container for the section
        header_layout = section_layout.box().row(align=True) # Layout for the header elements
        content_layout = section_layout.box().column(align=self.align_content) # Layout for the content elements

        # Draw the default header label if nothing is connected to InHeader
        if draw_default_header:
             # Ensure header_icon property exists if used here
             icon = getattr(self, 'header_icon', 'NONE') # Safely get icon property
             header_layout.label(text=self.header_text, icon=icon if icon in icons_ids_set else 'NONE')

        return header_layout, content_layout


@ACK.NE.add_node_to_category("Layout/Advanced")
@ACK.NE.add_node_metadata(label="Panel", tooltip="Panel layout node")
class PanelLayoutNode(AdvancedLayoutNode, ACK.NE.NodeExec):
    # --- Inputs ---
    InHeader = ACK.NE.InputSocket(ElementSocket, label="Header", multi=True)
    InContent = ACK.NE.InputSocket(ElementSocket, label="Content", multi=True)

    # --- Properties ---
    align_content = ACK.PropTyped.Bool(name="Align Content", default=False, description="Align the split layout within its parent").tag_node_drawable(order=0)

    header_text = ACK.PropTyped.String(name="Text", default="Header Title").tag_node_drawable(order=1, poll=lambda node, _ctx: not node.InHeader.is_linked)
    header_icon = ACK.PropTyped.String(name="Icon", default="NONE", search=search_icon_items).tag_node_drawable(order=2, poll=lambda node, _ctx: not node.InHeader.is_linked)

    # --- Outputs ---
    # Output socket remains an assignment as it's a descriptor itself
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Self")


    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> Tuple[bpy_types.UILayout, bpy_types.UILayout]:
        # Check if header should be drawn by connected nodes or default label
        # Note: The original code had 'use_def_header = self.InHeader.is_linked'
        # which seems reversed. If InHeader IS linked, we should execute the
        # connected nodes, not draw the default label. Let's assume the default
        # label is drawn only if InHeader is NOT linked.
        draw_default_header = not self.InHeader.is_linked

        # Create the layouts
        header, panel = layout.panel(self.uid, default_closed=False)
        if self.align_content and panel:
            panel = panel.column(align=True)

        # Draw the default header label if nothing is connected to InHeader
        if draw_default_header:
            # Ensure header_icon property exists if used here
            icon = getattr(self, 'header_icon', 'NONE') # Safely get icon property
            header.label(text=self.header_text, icon=icon if icon in icons_ids_set else 'NONE')

        return header, panel
