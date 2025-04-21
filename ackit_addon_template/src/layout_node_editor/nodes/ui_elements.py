from typing import Dict, Any, Set, Optional
import bpy
from bpy import types as bpy_types

# Import ACK from the root ackit library
from ....ackit import ACK
# Import ElementSocket from the sockets file in the same editor definition
from ..sockets import ElementSocket
from .enums import search_icon_items, icons_ids_set
from .base import BaseNode

__all__ = [
    'LabelNode',
    'OperatorNode',
    'PropNode',
]


class UIElementsNode(BaseNode):
    pass


# --- Enum Items for PropNode ---

prop_mode_items = [
    ('CONTEXT', "Context", "Access properties relative to the execution context (e.g., active object, scene)"),
    ('DATA', "bpy.data", "Access properties from a specific item in bpy.data (e.g., bpy.data.objects['Cube'])"),
]

prop_context_mode_items = [
    ('PRESET', "Preset", "Select a common context source (like Active Object, Scene)"),
    ('DATA_PATH', "Context Path", "Specify the path relative to the context object (e.g., 'object.location')"),
]

# Add more presets as needed
prop_context_preset_items = [
    ('ACTIVE_OBJECT', "Active Object", "context.object"),
    ('SCENE', "Scene", "context.scene"),
    ('WORLD', "World", "context.scene.world"),
    ('WINDOW_MANAGER', "Window Manager", "context.window_manager"),
    ('SCREEN', "Screen", "context.screen"),
    # ('TOOL_SETTINGS', "Tool Settings", "context.tool_settings"), # Example
]

# Get valid bpy.data collections (excluding private/internal ones)
prop_data_collection_items = []
def get_bdata_collections(self, context):
    prop_data_collection_items.clear()
    for attr_name in dir(bpy.data):
        # Basic filtering: avoid private/dunder, non-collection types, and specific known non-data attrs
        if not attr_name.startswith('_') and \
           hasattr(getattr(bpy.data, attr_name, None), 'get') and \
            attr_name not in ['bl_rna', 'rna_type', 'is_property_hidden', 'is_property_overridable_library', 'is_property_readonly']:
                # Check if it looks like a collection proxy
                # if isinstance(getattr(bpy.data, attr_name), (bpy.types.bpy_prop_collection, bpy.types.Collection)):
                prop_data_collection_items.append((attr_name, attr_name.replace("_", " ").title(), f"bpy.data.{attr_name}"))
    sorted(prop_data_collection_items)
    return prop_data_collection_items

# prop_data_collection_items = [(attr, attr.replace("_", " ").title(), f"bpy.data.{attr}") for attr in dir(bpy.data)] # get_bdata_collections()

# --- Search Function for bpy.data items ---

def search_data_items(self, context, edit_text):
    """Search function for bpy.data item names based on selected collection."""
    items = []
    collection_name = self.data_collection
    if not collection_name:
        return items # No collection selected

    collection = getattr(bpy.data, collection_name, None)
    if collection and hasattr(collection, 'keys'): # Check if it's dictionary-like
        # Limit results for performance if needed, especially for large collections like images/meshes
        limit = 100
        count = 0
        search_term = edit_text.lower() # Get current text in search box

        for name in collection.keys():
            if search_term in name.lower(): # Simple substring search
                 items.append(name) # (identifier, label, icon)
                 count += 1
                 if count >= limit:
                     break # Stop if limit is reached
    return sorted(items)


@ACK.NE.add_node_to_category("Elements")
@ACK.NE.add_node_metadata(label="Label", tooltip="Display a text label in a layout", icon='FONT_DATA')
class LabelNode(UIElementsNode, ACK.NE.NodeExec):
    """Node that draws a label into a layout."""
    # --- Inputs --- (None)

    # --- Properties ---
    text = ACK.PropTyped.String(name="Text", default="Label").tag_node_drawable(order=0)
    icon = ACK.PropTyped.String(name="Icon", default="NONE", search=search_icon_items).tag_node_drawable(order=1)

    # --- Outputs ---
    # Used to connect to LayoutNode.InContents (Child -> Parent)
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Element")

    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> None:
        layout.label(text=self.text, icon=self.icon if self.icon and self.icon in icons_ids_set else 'NONE')


@ACK.NE.add_node_to_category("Elements")
@ACK.NE.add_node_metadata(label="Operator Button", tooltip="Display a button that runs an operator", icon='PLAY')
class OperatorNode(UIElementsNode, ACK.NE.NodeExec):
    """Node that draws an operator button into a layout."""
    bl_width_default = 220
    bl_width_min = 180
    
    # --- Inputs --- (None)

    # --- Properties ---
    operator_id = ACK.PropTyped.String(name="Operator ID", default="wm.operator_defaults", description="The bl_idname of the operator to run").tag_node_drawable(order=0)
    use_text_override = ACK.PropTyped.Bool(name="Text Override", default=False, description="Enable Text Override").tag_node_drawable(order=1, text='')
    text_override = ACK.PropTyped.String(name="", default="", description="Optional text override for the button (uses operator label if empty)").tag_node_drawable(order=1, text='')
    icon = ACK.PropTyped.String(name="Icon", default="NONE", search=search_icon_items).tag_node_drawable(order=2)
    icon_only = ACK.PropTyped.Bool(name="Only", default=False, description="Only display the icon").tag_node_drawable(order=2, toggle=True)
    emboss = ACK.PropTyped.Bool(name="Emboss", default=True, description="Toggle emboss style for operator").tag_node_drawable(order=3)

    # --- Outputs ---
    # Used to connect to LayoutNode.InContents (Child -> Parent)
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Element")

    # Execute is called by _internal_execute
    def execute(self, context: bpy_types.Context, layout: bpy_types.UILayout) -> None:
        icon = self.icon if self.icon and self.icon in icons_ids_set else 'NONE'
        # TODO: evaluation input for depress state.
        layout.operator(self.operator_id,
                                text='' if self.icon_only else self.text_override if self.use_text_override else None,
                                icon=icon,
                                emboss=self.emboss)


# Define items for the source selection EnumProperty
prop_source_items = [
    ('ACTIVE_OBJECT', "Active Object", "Use the active object from the context"),
    ('SCENE', "Scene", "Use the current scene"),
    ('WORLD', "World", "Use the current scene's world"),
    ('SPECIFIC_OBJECT', "Specific Object", "Use an object specified by name"),
    # TODO: Add more sources like Material, Texture, etc. later if needed
]

@ACK.NE.add_node_to_category("Elements")
@ACK.NE.add_node_metadata(label="Property", tooltip="Display a property from Blender data (Context or bpy.data)", icon='RNA')
class PropNode(UIElementsNode, ACK.NE.NodeExec):
    """Node that draws a property widget into a layout, accessing data via Context or bpy.data."""
    bl_width_default = 250
    bl_width_min = 200 # Allow slightly narrower

    # --- Properties ---

    # -- Top Level Mode --
    mode = ACK.PropTyped.Enum(
        name="Mode",
        items=prop_mode_items,
        default='CONTEXT',
        description="How to access the property data"
    ).tag_node_drawable(order=0)

    # -- CONTEXT Mode Properties --
    context_mode = ACK.PropTyped.Enum(
        name="Context Mode",
        items=prop_context_mode_items,
        default='PRESET',
        description="How to specify the context data source"
    ).tag_node_drawable(order=1, poll=lambda node, _ctx: node.mode == 'CONTEXT')

    context_preset = ACK.PropTyped.Enum(
        name="Preset",
        items=prop_context_preset_items,
        default='ACTIVE_OBJECT',
        description="Select a common context data source"
    ).tag_node_drawable(order=2, poll=lambda node, _ctx: node.mode == 'CONTEXT' and node.context_mode == 'PRESET')

    context_preset_data_path = ACK.PropTyped.String(
        name="Data Path",
        default="",
        description="RNA data path on the selected Preset (e.g., 'location.x')"
    ).tag_node_drawable(order=3, poll=lambda node, _ctx: node.mode == 'CONTEXT' and node.context_mode == 'PRESET')

    context_data_path = ACK.PropTyped.String(
        name="Context Path",
        default="",
        description="Full RNA path from context (e.g., 'object.data.vertices[0].co')"
    ).tag_node_drawable(order=2, poll=lambda node, _ctx: node.mode == 'CONTEXT' and node.context_mode == 'DATA_PATH')


    # -- DATA Mode Properties --
    data_collection = ACK.PropTyped.Enum(
        name="Collection",
        items=get_bdata_collections, # prop_data_collection_items,
        # default='objects',
        description="Select the bpy.data collection (e.g., objects, materials)"
    ).tag_node_drawable(order=1, poll=lambda node, _ctx: node.mode == 'DATA')

    # Use the custom search function here
    data_item_name = ACK.PropTyped.String(
        name="Item Name",
        default="",
        description="Name of the item within the selected bpy.data collection",
        search=search_data_items # Assign the search function
    ).tag_node_drawable(order=2, poll=lambda node, _ctx: node.mode == 'DATA')

    data_item_path = ACK.PropTyped.String(
        name="Data Path",
        default="",
        description="RNA data path on the selected bpy.data item (e.g., 'location.z')"
    ).tag_node_drawable(order=3, poll=lambda node, _ctx: node.mode == 'DATA')


    # -- Common Properties --
    use_text_override = ACK.PropTyped.Bool(
        name="Text Override",
        default=False,
        description="Override the default property label"
    ).tag_node_drawable(order=10, text='') # Increase order to place below mode-specific props

    text_override = ACK.PropTyped.String(
        name="", # No label needed, tied to the checkbox
        default="",
        description="Custom text label for the property"
    ).tag_node_drawable(order=10, poll=lambda node, _ctx: node.use_text_override)

    # --- Outputs ---
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Element")

    # --- Execute Method ---
    def execute(self, context: bpy.types.Context, layout: bpy.types.UILayout) -> None:
        data_block: Optional[bpy.types.ID] = None
        prop_path: Optional[str] = None
        owner_description = "Unknown" # For error messages

        try:
            # --- Determine data_block and prop_path based on mode ---
            if self.mode == 'CONTEXT':
                owner_description = f"Context ({self.context_mode})"
                if self.context_mode == 'PRESET':
                    owner_description = f"Context Preset ({self.context_preset})"
                    preset = self.context_preset
                    if preset == 'ACTIVE_OBJECT': data_block = context.object
                    elif preset == 'SCENE': data_block = context.scene
                    elif preset == 'WORLD': data_block = context.scene.world
                    elif preset == 'WINDOW_MANAGER': data_block = context.window_manager
                    elif preset == 'SCREEN': data_block = context.screen
                    # Add other presets here...
                    else: data_block = None # Unknown preset

                    prop_path = self.context_preset_data_path

                elif self.context_mode == 'DATA_PATH':
                    full_path = self.context_data_path
                    owner_description = f"Context Path ('{full_path}')"
                    if not full_path:
                        print(f"Error: PropNode '{self.name}': Invalid Context Path '{full_path}'.")
                        layout.label(text=f"Invalid Context Path", icon='ERROR')
                        return None

                    # Separate owner path from property name
                    if '.' not in full_path:
                        data_block = context
                        prop_path = full_path
                    else:
                        owner_path, prop_name = full_path.rsplit('.', 1)
                        try:
                            # Resolve the owner object/struct
                            data_block = context.path_resolve(owner_path, False) # coerce=False
                            prop_path = prop_name
                        except ValueError: # path_resolve raises ValueError if path is invalid
                            print(f"Error: PropNode '{self.name}': Could not resolve context owner path '{owner_path}'")
                            data_block = None
                            prop_path = None
                        except Exception as e_resolve:
                            print(f"Error resolving context path '{owner_path}' in PropNode '{self.name}': {e_resolve}")
                            data_block = None
                            prop_path = None


            elif self.mode == 'DATA':
                owner_description = f"bpy.data.{self.data_collection}['{self.data_item_name}']"
                if not self.data_collection or not self.data_item_name:
                    # print(f"Warning: PropNode '{self.name}': bpy.data collection or item name not specified.")
                    return None # Need both collection and item name

                collection = getattr(bpy.data, self.data_collection, None)
                if collection and hasattr(collection, 'get'):
                    data_block = collection.get(self.data_item_name)
                else:
                    print(f"Error: PropNode '{self.name}': Invalid bpy.data collection '{self.data_collection}'.")
                    data_block = None

                prop_path = self.data_item_path
                
                if data_block and prop_path:
                    split_path = prop_path.split('.')
                    data_block = data_block.path_resolve('.'.join(split_path[:-1]), False) # coerce=False
                    prop_path = split_path[-1]

            # --- Validate and Draw ---
            if data_block is None:
                # print(f"Warning: PropNode '{self.name}': Could not find data source: {owner_description}.")
                # Optionally draw error in UI
                # parent_layout.label(text=f"Source Not Found: {owner_description[:30]}...", icon='ERROR')
                return None

            if not prop_path:
                # print(f"Warning: PropNode '{self.name}': No property data path specified for source {owner_description}.")
                # Optionally draw error in UI
                # parent_layout.label(text=f"No Data Path", icon='ERROR')
                return None

            # Determine display text
            display_text = ""
            if self.use_text_override and self.text_override:
                display_text = self.text_override

            # Draw the property
            layout.prop(data_block, prop_path, text=display_text)

        except AttributeError:
            # Handle cases where the prop_path is invalid for the data_block
            print(f"Error: PropNode '{self.name}': Invalid data path '{prop_path}' for source '{owner_description}' ({type(data_block).__name__}).")
            layout.label(text=f"Invalid Path: '{prop_path}'", icon='ERROR')
        except Exception as e:
            # Catch other potential errors
            print(f"Error executing PropNode '{self.name}': {e}")
            import traceback
            traceback.print_exc()
            layout.label(text=f"Node Error", icon='ERROR')
