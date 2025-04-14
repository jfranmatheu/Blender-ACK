from bl_ui.space_node import NODE_PT_active_node_generic

from .. import ACK
from .btypes.node_tree import NodeTree


@ACK.UI.override_layout(NODE_PT_active_node_generic, poll=lambda ctx: NodeTree.poll_space(ctx))
class ActiveNodePanel:
    def draw(self, context, layout):
        if context.active_node is None:
            return
        layout.prop(context.active_node, "label", icon='NODE')
