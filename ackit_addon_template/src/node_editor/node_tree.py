from ...ackit import ACK


class NodeTree(ACK.NE.Tree):
    bl_label = "ACK Example Node Tree"
    
    def get_input_nodes(self):
        """Get all nodes that have no inputs or unconnected inputs"""
        input_nodes = []
        for node in self.nodes:
            is_input = True
            for input in node.inputs:
                if input.links:
                    is_input = False
                    break
            if is_input:
                input_nodes.append(node)
        return input_nodes

    def update(self) -> None:
        """Called when the node tree is modified"""
        if not self.nodes:
            return
            
        # Only evaluate from input nodes
        for input_node in self.get_input_nodes():
            input_node.process()

    def evaluate(self) -> None:
        """Manual evaluation of the entire node tree"""
        self.update()
