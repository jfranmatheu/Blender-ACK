from collections import defaultdict

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# Updated relative imports
from ..core.btypes import BTypes # Assuming BTypes comes from core/btypes.py
from ..globals import GLOBALS # Check globals path


class DefaultNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == f"{GLOBALS.ADDON_MODULE_SHORT.upper()}_TREETYPE"


def create_category_hierarchy(categories_dict, category_path, node_item):
    """Helper function to create nested category structure"""
    if not category_path:
        return node_item
    
    current = category_path[0]
    remaining = category_path[1:]
    
    # If this is the last category in the path, add the node
    if not remaining:
        if current not in categories_dict:
            categories_dict[current] = []
        categories_dict[current].append(node_item)
        return
    
    # Create subcategory if it doesn't exist
    if current not in categories_dict:
        categories_dict[current] = {}
    
    # Recursively handle remaining path
    create_category_hierarchy(categories_dict[current], remaining, node_item)


def build_category_list(categories_dict, identifier_prefix=''):
    """Convert nested dictionary into list of NodeCategory objects"""
    result = []
    
    for category_name, contents in categories_dict.items():
        identifier = f"{identifier_prefix}{category_name}".replace(' ', '_').upper()
        label = category_name.replace('_', ' ').title()
        
        # If contents is a list, these are the category's direct nodes
        if isinstance(contents, list):
            result.append(DefaultNodeCategory(identifier, label, items=contents))
        # If contents is a dict, these are subcategories
        else:
            items = []
            # First add any direct nodes (stored in special key if exists)
            if isinstance(contents.get('', []), list):
                items.extend(contents[''])
            
            # Then recursively process subcategories
            subcats = build_category_list(
                {k: v for k, v in contents.items() if k != ''}, 
                f"{identifier}_"
            )
            items.extend(subcats)
            
            result.append(DefaultNodeCategory(identifier, label, items=items))
    
    return result


def register():
    # Create hierarchical structure
    category_hierarchy = {}
    node_classes = BTypes.Node.get_classes()
    
    # First pass: organize nodes into category hierarchy
    for node_class in node_classes:
        if hasattr(node_class, '_node_category') and node_class._node_category:
            # Split category path and create node item
            cat_path = node_class._node_category.split('/')
            node_item = NodeItem(node_class.get_idname())
            
            # Add to hierarchy
            create_category_hierarchy(category_hierarchy, cat_path, node_item)
    
    # Second pass: convert hierarchy to flat list of categories
    node_categories = build_category_list(category_hierarchy)
    
    # Register with Blender
    if node_categories:
        nodeitems_utils.register_node_categories(
            f'{GLOBALS.ADDON_MODULE_SHORT.upper()}_NODES', 
            node_categories
        )


def unregister():
    try:
        nodeitems_utils.unregister_node_categories(f'{GLOBALS.ADDON_MODULE_SHORT.upper()}_NODES')
    except:
        pass
