import bpy # Add bpy import
from collections import defaultdict

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem, _node_categories # Add _node_categories import

# Updated relative imports
from ..core.btypes import BTypes # Assuming BTypes comes from core/btypes.py
from ..globals import GLOBALS # Check globals path


# Store the dynamically created category class
node_category_class = None
# Store registered node categories for unregistration
node_categories_list = []


# Function to create the base NodeCategory class dynamically
def get_node_category_class():
    global node_category_class
    if node_category_class is None:
        tree_type_name = f"{GLOBALS.ADDON_MODULE_SHORT.upper()}_TREETYPE"
        # Define the poll method using the addon's tree type
        def poll(cls, context):
            return context.space_data.tree_type == tree_type_name
        
        # Create the dynamic class
        node_category_class = type(
            f"{GLOBALS.ADDON_MODULE_SHORT.upper()}NodeCategory",
            (NodeCategory,),
            {
                'poll': classmethod(poll)
            }
        )
    return node_category_class


# Copied and adapted function to register multi-level categories
def register_node_categories_multi(identifier, cat_list, subcat_list):
    if identifier in _node_categories:
        print(f"Warning: Node categories list '{identifier}' already registered. Skipping.")
        # raise KeyError("Node categories list '%s' already registered" % identifier)
        return

    # works as draw function for menus
    def draw_node_item(self, context):
        layout = self.layout
        col = layout.column(align=True)
        for item in self.category.items(context):
            # Check if item is a subcategory (has identifier) or a node item
            if hasattr(item, 'identifier') and isinstance(item, NodeCategory):
                layout.menu(f"NODE_MT_category_{item.identifier}")
            elif isinstance(item, NodeItem):
                # Use node_item.draw method if available, otherwise default draw
                draw_func = getattr(item, "draw", None)
                if draw_func:
                    draw_func(item, col, context)
                else:
                    col.operator("node.add_node", text=item.label).type = item.nodetype
            else:
                # Handle potential separators or other custom items if needed
                pass


    menu_types = []
    all_cats = subcat_list + cat_list
    for cat in all_cats:
        # Only register menus for categories that actually have items or subcategories
        if cat.items(None): # Pass None context as items should be static list
            menu_type = type(f"NODE_MT_category_{cat.identifier}", (bpy.types.Menu,), {
                "bl_space_type": 'NODE_EDITOR',
                "bl_label": cat.name,
                "category": cat,
                "poll": cat.poll,
                "draw": draw_node_item,
            })

            menu_types.append(menu_type)
            bpy.utils.register_class(menu_type)

    def draw_add_menu(self, context):
        layout = self.layout
        for cat in cat_list: # Only draw top-level categories in the main add menu
            if cat.poll(context):
                layout.menu(f"NODE_MT_category_{cat.identifier}")

    # stores: (categories list, menu draw function, submenu types)
    _node_categories[identifier] = (all_cats, draw_add_menu, menu_types)
    # Store the identifier and menu types for unregistration
    GLOBALS.NODE_EDITOR_MENUS[identifier] = menu_types


def register():
    global node_categories_list
    node_categories_list.clear() # Clear previous list if re-registering

    # Initialize the global dictionary for menus if it doesn't exist
    if not hasattr(GLOBALS, 'NODE_EDITOR_MENUS'):
        GLOBALS.NODE_EDITOR_MENUS = {}

    node_cat_class = get_node_category_class()
    if not node_cat_class:
        print("Error: Could not create node category class.")
        return
        
    cat_node_relationship: dict[str, list] = defaultdict(list)
    subcat_node_relationship: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    node_classes = BTypes.Node.get_classes()
    
    # Organize nodes based on their category path
    for node in node_classes:
        category_path = getattr(node, '_node_category', None)
        if category_path:
            parts = category_path.strip('/').split('/')
            cat_name = parts[0].strip()
            
            if len(parts) > 1:
                subcat_name = parts[1].strip()
                subcat_node_relationship[cat_name][subcat_name].append(node)
            else:
                cat_node_relationship[cat_name].append(node)

    # Build NodeCategory objects
    all_subcategories = []
    top_level_categories = []

    # Process categories that might have subcategories
    processed_cats = set()
    for cat_name, subcats in subcat_node_relationship.items():
        processed_cats.add(cat_name)
        category_items = []
        subcat_objects = []

        # Create subcategory objects
        for subcat_name, nodes_in_subcat in subcats.items():
            subcat_id = f"{cat_name.upper()}_{subcat_name.upper()}".replace(' ', '_')
            subcat_label = subcat_name.title()
            subcat_node_items = [NodeItem(n.get_idname(), label=n.bl_label) for n in nodes_in_subcat]
            
            new_subcat = node_cat_class(subcat_id, subcat_label, items=subcat_node_items)
            all_subcategories.append(new_subcat)
            subcat_objects.append(new_subcat) # Add to parent category's items

        # Add direct nodes for this category (if any)
        direct_nodes = cat_node_relationship.get(cat_name, [])
        category_items.extend([NodeItem(n.get_idname(), label=n.bl_label) for n in direct_nodes])
        
        # Add subcategory objects to the items list
        category_items.extend(subcat_objects)

        # Create the top-level category object
        cat_id = cat_name.upper().replace(' ', '_')
        cat_label = cat_name.title()
        top_level_categories.append(node_cat_class(cat_id, cat_label, items=category_items))

    # Process remaining categories (those without subcategories)
    for cat_name, nodes in cat_node_relationship.items():
        if cat_name not in processed_cats:
            cat_id = cat_name.upper().replace(' ', '_')
            cat_label = cat_name.title()
            node_items = [NodeItem(n.get_idname(), label=n.bl_label) for n in nodes]
            top_level_categories.append(node_cat_class(cat_id, cat_label, items=node_items))

    # Register using the multi-level function
    identifier = f'{GLOBALS.ADDON_MODULE_SHORT.upper()}_NODES'
    
    if top_level_categories or all_subcategories:
        register_node_categories_multi(identifier, top_level_categories, all_subcategories)
        node_categories_list = top_level_categories + all_subcategories # Store for unregister

    # Initialize the global dictionary for menus if it doesn't exist
    # if not hasattr(GLOBALS, 'NODE_EDITOR_MENUS'):
    #     GLOBALS.NODE_EDITOR_MENUS = {}


def unregister():
    identifier = f'{GLOBALS.ADDON_MODULE_SHORT.upper()}_NODES'
    
    # Unregister menus first
    if hasattr(GLOBALS, 'NODE_EDITOR_MENUS') and identifier in GLOBALS.NODE_EDITOR_MENUS:
        menu_types = GLOBALS.NODE_EDITOR_MENUS.pop(identifier, [])
        for menu_type in reversed(menu_types): # Unregister in reverse order
            try:
                bpy.utils.unregister_class(menu_type)
            except RuntimeError as e:
                 print(f"Error unregistering menu {menu_type.__name__}: {e}")


    # Unregister node categories using the identifier
    try:
        # Check if the identifier exists before trying to unregister
        if identifier in _node_categories:
             nodeitems_utils.unregister_node_categories(identifier)
        else:
            print(f"Node categories list '{identifier}' not found for unregistration.")
    except KeyError:
         print(f"Error: Node categories list '{identifier}' was not found during unregistration.")
    except Exception as e:
         print(f"An unexpected error occurred during node category unregistration: {e}")

    global node_categories_list
    node_categories_list.clear()
    # We don't unregister node_category_class itself, as it's just a type definition
