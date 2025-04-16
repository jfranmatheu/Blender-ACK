from bpy.types import Context, UILayout
from ...ackit import ACK

from .node_tree import UILayoutNodeTree


@ACK.UI.Panel.FromFunction.NODE_EDITOR(tab="Preview", flags=set(), order=0)
def draw_ne_uilayout_preview(context: Context, layout: UILayout):
    node_tree: UILayoutNodeTree = context.space_data.node_tree
    if not node_tree:
        layout.label(text="No node tree selected")
        return
    if not UILayoutNodeTree.poll_space(context):
        layout.label(text="Not a node tree")
        return

    node_tree.execute(context, layout)
