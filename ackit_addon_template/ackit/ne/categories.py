import bpy
from collections import defaultdict
import re # For parsing menu ID back to path

from ..core.btypes import BTypes
from ..globals import GLOBALS

# --- Global storage ---
# Stores the generated hierarchy, e.g., {'Inputs': {'Data': {'__nodes__': [(NodeA, 'TREE_A')], '__tree_types__': {'TREE_A'}}, '__nodes__': [(NodeB, 'TREE_B')], '__tree_types__': {'TREE_B'}}, ...}
_category_hierarchy = {}
# Stores dynamically created menu classes, mapping bl_idname to the class
_registered_menu_classes = {}

# Special key for storing direct node classes within a category level
_NODE_LIST_KEY = '__nodes__'
# Special key for storing the set of tree types applicable to a category level
_TREE_TYPES_KEY = '__tree_types__'

# --- Hierarchy Building ---

def add_to_hierarchy(hierarchy, path_parts, node_class, node_tree_type):
    """
    Recursively adds a node class and its tree type to the nested dictionary hierarchy,
    updating tree type sets along the path.
    """
    if not path_parts:
        return # Should not happen

    current_part = path_parts[0]
    remaining_parts = path_parts[1:]

    if current_part not in hierarchy:
        hierarchy[current_part] = {_TREE_TYPES_KEY: set()} # Initialize with tree type set

    # Add the tree type to the current level's set if it's valid
    if node_tree_type:
        hierarchy[current_part][_TREE_TYPES_KEY].add(node_tree_type)

    if not remaining_parts:
        # Leaf level: Add node class tuple to the list under the special key
        if _NODE_LIST_KEY not in hierarchy[current_part]:
            hierarchy[current_part][_NODE_LIST_KEY] = []
        # Store node class and its tree type together
        hierarchy[current_part][_NODE_LIST_KEY].append((node_class, node_tree_type))
    else:
        # Go deeper, ensuring the tree type propagates up if recursion returns
        add_to_hierarchy(hierarchy[current_part], remaining_parts, node_class, node_tree_type)
        # After child recursion, ensure parent also has the type (redundancy is handled by set)
        # Note: This might add the type even if the node wasn't ultimately placed *directly*
        # under this path due to deeper levels, which is correct for menu filtering.
        if node_tree_type:
             hierarchy[current_part][_TREE_TYPES_KEY].add(node_tree_type)


def build_hierarchy():
    """Builds the nested category hierarchy from registered node classes."""
    global _category_hierarchy
    _category_hierarchy.clear()
    # Initialize root level with its own tree type set
    _category_hierarchy[_TREE_TYPES_KEY] = set()
    node_classes = BTypes.Node.get_classes()

    for node_class in node_classes:
        category_path = getattr(node_class, '_node_category', None)
        node_tree_type = getattr(node_class, '_node_tree_type', None) # Get the tree type

        if category_path and node_tree_type: # Require both category and tree type
            path_parts = [p.strip() for p in category_path.strip('/').split('/') if p.strip()]
            if path_parts:
                add_to_hierarchy(_category_hierarchy, path_parts, node_class, node_tree_type.bl_idname)
                # Add tree type to the root level set as well
                _category_hierarchy[_TREE_TYPES_KEY].add(node_tree_type.bl_idname)
            else:
                print(f"Warning: Node class {node_class.__name__} has invalid category path: '{category_path}'")
        elif category_path and not node_tree_type:
             print(f"Warning: Node class {node_class.__name__} has category '{category_path}' but is missing '_node_tree_type'. Skipping.")
        # Nodes without category or tree type are ignored for the menu

# --- Dynamic Menu Drawing ---

def draw_submenu(self, context):
    """Generic draw function for all dynamically created submenus."""
    layout = self.layout
    current_context_tree_type = getattr(context.space_data, 'tree_type', None)
    if not current_context_tree_type:
        return # Cannot determine context tree type

    # Determine the path this menu represents from its bl_idname
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

    # Check if this menu category is relevant for the current tree type
    supported_types_for_menu = current_level.get(_TREE_TYPES_KEY, set())
    if current_context_tree_type not in supported_types_for_menu:
        # This whole menu branch is irrelevant for the current tree type
        # We might choose to draw nothing, or draw it greyed out.
        # For now, draw nothing by simply returning early.
        # layout.label(text=f"{self.bl_label} (No nodes for this tree)", icon='INFO') # Example: grey out
        return

    # Get sorted subcategories and node entries at this level
    # Filter out special keys when getting subcategory keys
    subcat_keys = sorted([k for k, v in current_level.items() if k not in (_NODE_LIST_KEY, _TREE_TYPES_KEY) and isinstance(v, dict)])
    # Get direct node entries (tuples of class, tree_type)
    direct_node_entries = sorted(current_level.get(_NODE_LIST_KEY, []), key=lambda entry: entry[0].bl_label) # Sort by node class label

    # 1. Draw Submenus (Filtered)
    drawn_submenu_count = 0
    for subcat_key in subcat_keys:
        sub_hierarchy = current_level.get(subcat_key, {})
        supported_types_for_subcat = sub_hierarchy.get(_TREE_TYPES_KEY, set())

        # Only draw submenu if it supports the current context's tree type
        if current_context_tree_type in supported_types_for_subcat:
            sub_path_parts = path_parts + [subcat_key]
            sub_menu_idname = prefix + "_".join(p.upper().replace(' ', '_') for p in sub_path_parts)
            if sub_menu_idname in _registered_menu_classes:
                layout.menu(sub_menu_idname)
                drawn_submenu_count += 1
            else:
                 print(f"Warning: Submenu class {sub_menu_idname} not found during drawing.")

    # Add separator only if we drew submenus AND will draw relevant nodes
    # Check if any direct nodes match the current tree type
    relevant_direct_nodes_exist = any(ntt == current_context_tree_type for nc, ntt in direct_node_entries)

    if drawn_submenu_count > 0 and relevant_direct_nodes_exist:
        layout.separator()

    # 2. Draw Node Operators (Filtered)
    for node_class, node_tree_type in direct_node_entries:
        # Only draw node if its tree type matches the current context's tree type
        if node_tree_type == current_context_tree_type:
            op = layout.operator("node.add_node", text=node_class.bl_label)
            op.type = node_class.get_idname()
            # Optionally set use_transform for placement: op.use_transform = True

# --- Dynamic Menu Creation ---

def create_menus_recursive(hierarchy_dict, identifier_prefix="ACKIT_MT_category", parent_parts=[]):
    """
    Recursively creates bpy.types.Menu classes for the hierarchy.
    Does not need tree type awareness itself, filtering happens in draw functions.
    """
    global _registered_menu_classes

    # Iterate over actual category keys, excluding the special node list and tree type keys
    sorted_keys = sorted([k for k in hierarchy_dict.keys() if k not in (_NODE_LIST_KEY, _TREE_TYPES_KEY)])

    for key in sorted_keys:
        current_parts = parent_parts + [key]
        menu_idname = identifier_prefix + "_" + "_".join(p.upper().replace(' ', '_') for p in current_parts)
        menu_label = key.replace('_', ' ').title()

        # Check if the sub-hierarchy actually contains nodes or further submenus
        # (Prevents creating empty menu classes, though filtering in draw handles display)
        sub_hierarchy = hierarchy_dict[key]
        has_nodes = _NODE_LIST_KEY in sub_hierarchy and sub_hierarchy[_NODE_LIST_KEY]
        has_subcats = any(k not in (_NODE_LIST_KEY, _TREE_TYPES_KEY) for k in sub_hierarchy.keys())

        if (has_nodes or has_subcats) and menu_idname not in _registered_menu_classes:
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
            if isinstance(sub_hierarchy, dict):
                create_menus_recursive(sub_hierarchy, identifier_prefix, current_parts)


# --- Main Add Menu Integration ---

def draw_ackit_add_menu(self, context):
    """Draw function appended to NODE_MT_add, filtered by context tree type."""
    # Check context: We need the node editor space and its tree_type
    space = context.space_data
    if not (space and hasattr(space, 'tree_type')):
        return

    current_context_tree_type = space.tree_type
    if not current_context_tree_type:
         return # Cannot determine context tree type

    layout = self.layout

    # Draw top-level menus from the hierarchy, filtered by tree type
    # Filter out the special keys from top-level keys
    sorted_top_keys = sorted([k for k in _category_hierarchy.keys() if k not in (_NODE_LIST_KEY, _TREE_TYPES_KEY)])

    for key in sorted_top_keys:
        top_level_category = _category_hierarchy.get(key, {})
        supported_types = top_level_category.get(_TREE_TYPES_KEY, set())

        # Only draw top-level menu if it supports the current context's tree type
        if current_context_tree_type in supported_types:
            menu_idname = f"ACKIT_MT_category_{key.upper().replace(' ', '_')}"
            if menu_idname in _registered_menu_classes:
                 layout.menu(menu_idname)
            else:
                # This might happen if a category was defined but contained nodes
                # only for *other* tree types, so no menu class was needed/created
                # for *this* branch, or if create_menus_recursive had an issue.
                # Optionally print a warning or draw a disabled label.
                # print(f"Warning: Top-level menu class {menu_idname} not found but expected for tree type {current_context_tree_type}.")
                # layout.label(text=key.title() + " (?)") # Fallback label
                pass

    # Optionally draw nodes defined directly at the root (if any)
    # These would have been added with an empty path_parts in build_hierarchy
    # (Currently, build_hierarchy requires a non-empty path_parts)
    # root_node_entries = sorted(_category_hierarchy.get(_NODE_LIST_KEY, []), key=lambda entry: entry[0].bl_label)
    # relevant_root_nodes_exist = any(ntt == current_context_tree_type for nc, ntt in root_node_entries)

    # if sorted_top_keys and relevant_root_nodes_exist: # Add separator if menus and relevant root nodes exist
    #     layout.separator()

    # for node_class, node_tree_type in root_node_entries:
    #     if node_tree_type == current_context_tree_type:
    #         op = layout.operator("node.add_node", text=node_class.bl_label)
    #         op.type = node_class.get_idname()

# --- Registration ---

def late_register():
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
