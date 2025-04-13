import bpy
from collections import defaultdict
import re # For parsing menu ID back to path

from ..core.btypes import BTypes
from ..globals import GLOBALS

# --- Global storage ---
# Stores the generated hierarchy, e.g., {'Inputs': {'Data': {'__nodes__': [NodeA]}, '__nodes__': [NodeB]}, ...}
_category_hierarchy = {} 
# Stores dynamically created menu classes, mapping bl_idname to the class
_registered_menu_classes = {} 

# Special key for storing direct node classes within a category level
_NODE_LIST_KEY = '__nodes__'

# --- Hierarchy Building ---

def add_to_hierarchy(hierarchy, path_parts, node_class):
    """Recursively adds a node class to the nested dictionary hierarchy."""
    if not path_parts:
        return # Should not happen

    current_part = path_parts[0]
    remaining_parts = path_parts[1:]

    if current_part not in hierarchy:
        hierarchy[current_part] = {} 

    if not remaining_parts:
        # Leaf level: Add node class to the list under the special key
        if _NODE_LIST_KEY not in hierarchy[current_part]:
            hierarchy[current_part][_NODE_LIST_KEY] = []
        hierarchy[current_part][_NODE_LIST_KEY].append(node_class)
    else:
        # Go deeper
        add_to_hierarchy(hierarchy[current_part], remaining_parts, node_class)

def build_hierarchy():
    """Builds the nested category hierarchy from registered node classes."""
    global _category_hierarchy
    _category_hierarchy.clear()
    node_classes = BTypes.Node.get_classes()

    for node_class in node_classes:
        category_path = getattr(node_class, '_node_category', None)
        if category_path:
            path_parts = [p.strip() for p in category_path.strip('/').split('/') if p.strip()]
            if path_parts:
                add_to_hierarchy(_category_hierarchy, path_parts, node_class)
            else:
                print(f"Warning: Node class {node_class.__name__} has invalid category path: '{category_path}'")
        else:
            # Optionally add nodes without a category to a default one, e.g., 'Uncategorized'
            # add_to_hierarchy(_category_hierarchy, ['Uncategorized'], node_class)
            pass 

# --- Dynamic Menu Drawing ---

def draw_submenu(self, context):
    """Generic draw function for all dynamically created submenus."""
    layout = self.layout
    
    # Determine the path this menu represents from its bl_idname
    # Example: ACKIT_MT_category_INPUTS_DATA -> ['Inputs', 'Data']
    prefix = "ACKIT_MT_category_"
    if not self.bl_idname.startswith(prefix):
        return # Should not happen
        
    path_str = self.bl_idname[len(prefix):]
    path_parts = [p.replace('_', ' ').title() for p in path_str.split('_') if p] # Reconstruct path parts

    # Find the corresponding level in the hierarchy
    current_level = _category_hierarchy
    try:
        for part in path_parts:
            current_level = current_level[part]
    except KeyError:
        print(f"Error: Could not find hierarchy path for menu {self.bl_idname}")
        return

    # Get sorted subcategories and nodes at this level
    # Filter out the special node list key when getting subcategory keys
    subcat_keys = sorted([k for k, v in current_level.items() if k != _NODE_LIST_KEY and isinstance(v, dict)])
    # Get direct nodes using the special key
    direct_nodes = sorted(current_level.get(_NODE_LIST_KEY, []), key=lambda nc: nc.bl_label)

    # 1. Draw Submenus
    for subcat_key in subcat_keys:
        sub_path_parts = path_parts + [subcat_key]
        # Construct the bl_idname for the submenu
        sub_menu_idname = prefix + "_".join(p.upper().replace(' ', '_') for p in sub_path_parts)
        if sub_menu_idname in _registered_menu_classes:
            layout.menu(sub_menu_idname)
        else:
             print(f"Warning: Submenu class {sub_menu_idname} not found during drawing.")

    # Add separator if there are both submenus and direct items
    if subcat_keys and direct_nodes:
        layout.separator()

    # 2. Draw Node Operators
    for node_class in direct_nodes:
        op = layout.operator("node.add_node", text=node_class.bl_label)
        op.type = node_class.get_idname()
        # Optionally set use_transform for placement: op.use_transform = True


# --- Dynamic Menu Creation ---

def create_menus_recursive(hierarchy_dict, identifier_prefix="ACKIT_MT_category", parent_parts=[]):
    """Recursively creates bpy.types.Menu classes for the hierarchy."""
    global _registered_menu_classes
    
    # Iterate over actual category keys, excluding the special node list key
    sorted_keys = sorted([k for k in hierarchy_dict.keys() if k != _NODE_LIST_KEY])

    for key in sorted_keys:
        current_parts = parent_parts + [key]
        menu_idname = identifier_prefix + "_" + "_".join(p.upper().replace(' ', '_') for p in current_parts)
        menu_label = key.replace('_', ' ').title()

        if menu_idname not in _registered_menu_classes:
            # Create the menu class dynamically
            menu_cls = type(
                menu_idname, 
                (bpy.types.Menu,), 
                {
                    "bl_idname": menu_idname, 
                    "bl_label": menu_label, 
                    "draw": draw_submenu # Use the generic draw function
                }
            )
            _registered_menu_classes[menu_idname] = menu_cls
            
            # Recurse for subcategories within this key
            if isinstance(hierarchy_dict[key], dict):
                create_menus_recursive(hierarchy_dict[key], identifier_prefix, current_parts)


# --- Main Add Menu Integration ---

def draw_ackit_add_menu(self, context):
    """Draw function appended to NODE_MT_add."""
    # Check context: We need the node editor space and the correct tree type
    if not (context.space_data and hasattr(context.space_data, 'tree_type')):
        return
    
    module_short = getattr(GLOBALS, 'ADDON_MODULE_SHORT', 'ACKIT') 
    expected_tree_type = f"{module_short.upper()}_TREETYPE"
    if context.space_data.tree_type != expected_tree_type:
        return

    layout = self.layout
    
    # Draw top-level menus from the hierarchy
    # Filter out the special node list key
    sorted_top_keys = sorted([k for k in _category_hierarchy.keys() if k != _NODE_LIST_KEY])

    for key in sorted_top_keys:
        menu_idname = f"ACKIT_MT_category_{key.upper().replace(' ', '_')}"
        if menu_idname in _registered_menu_classes:
             layout.menu(menu_idname)
        else:
            print(f"Warning: Top-level menu class {menu_idname} not found.")
            # Optionally draw a label as fallback
            # layout.label(text=key.title()) 

    # Optionally draw nodes without a category directly here (if they were stored under _NODE_LIST_KEY at the root)
    # root_nodes = sorted(_category_hierarchy.get(_NODE_LIST_KEY, []), key=lambda nc: nc.bl_label)
    # if root_nodes:
    #     layout.separator()
    #     for node_class in root_nodes:
    #         op = layout.operator("node.add_node", text=node_class.bl_label)
    #         op.type = node_class.get_idname()


# --- Registration ---

def register():
    global _registered_menu_classes
    
    # 1. Build the hierarchy dictionary
    build_hierarchy()
    
    # 2. Create dynamic menu classes
    _registered_menu_classes.clear()
    create_menus_recursive(_category_hierarchy)
    
    # 3. Register menu classes
    for menu_cls in _registered_menu_classes.values():
        try:
            bpy.utils.register_class(menu_cls)
        except ValueError: # Might already be registered if code reloads
            print(f"Info: Menu class {menu_cls.bl_idname} might already be registered.")
        except Exception as e:
            print(f"Error registering menu class {menu_cls.bl_idname}: {e}")

    # 4. Append main draw function to the add menu
    try:
        bpy.types.NODE_MT_add.append(draw_ackit_add_menu)
    except Exception as e:
         print(f"Error appending draw function to NODE_MT_add: {e}")

def unregister():
    global _registered_menu_classes, _category_hierarchy

    # 1. Remove main draw function
    try:
        bpy.types.NODE_MT_add.remove(draw_ackit_add_menu)
    except ValueError: # Not found, maybe already removed or failed to append
        pass 
    except Exception as e:
         print(f"Error removing draw function from NODE_MT_add: {e}")

    # 2. Unregister dynamic menu classes (in reverse order of registration)
    for menu_cls in reversed(list(_registered_menu_classes.values())):
        try:
            bpy.utils.unregister_class(menu_cls)
        except RuntimeError: # Already unregistered
             pass
        except Exception as e:
            print(f"Error unregistering menu class {menu_cls.bl_idname}: {e}")

    # 3. Clear global storage
    _registered_menu_classes.clear()
    _category_hierarchy.clear()
