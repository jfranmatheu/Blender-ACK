from typing import Dict, Any, Set, Optional
import bpy
from bpy import types as bpy_types

# Import ACK from the root ackit library
from ....ackit import ACK
# Import ElementSocket from the sockets file in the same editor definition
from ..sockets import ElementSocket
from .enums import search_icon_items, icons_ids_set


# --- UI List Types ---

def process_ui_list_name(name: str) -> str:
    """Process the name of the UI list type."""
    if '_UL_' in name:
        split = name.split('_UL_')
        return f"[{split[0]}] {split[1].replace('_', ' ').title()}"
    return name.replace('_', ' ').title()

ui_list_types_x_names = None

def update_ui_list_types():
    global ui_list_types_x_names
    ui_list_types = bpy_types.UIList.__subclasses__()
    ui_list_types_x_names = {
        process_ui_list_name(item.__name__): item for item in ui_list_types
    }

def search_list_type_idname(self, context, edit_text):
    """Search function for list type idnames."""
    global ui_list_types_x_names
    if ui_list_types_x_names is None:
        update_ui_list_types()
    startswith = []
    contains = []
    for key in ui_list_types_x_names.keys():
        if key.startswith(edit_text):
            startswith.append(key)
        elif edit_text in key:
            contains.append(key)
    return startswith + contains


# --- Template List Node ---

@ACK.NE.add_node_to_category("Elements/Templates")
@ACK.NE.add_node_metadata(label="List", tooltip="Display a list of items from a data path", icon='RNA')
class TemplateListNode(ACK.NE.NodeExec):
    """Node that draws a list of items from a data path."""
    bl_width_default = 250
    bl_width_min = 200 # Allow slightly narrower

    # --- Inputs --- (None for execution flow)

    # --- Properties ---

    list_type_idname = ACK.PropTyped.String(
        name="List Type",
        description="Type of list to display",
        search=search_list_type_idname
    ).tag_node_drawable(order=0)

    '''list_id = ACK.PropTyped.String(
        name="List ID",
        default="",
        description="ID of the list to display"
    ).tag_node_drawable(order=1)'''

    data_path = ACK.PropTyped.String(
        name="Data Path",
        default="",
        description="Full RNA path from context (e.g., 'object.data')"
    ).tag_node_drawable(order=2)

    propname = ACK.PropTyped.String(
        name="Property Name",
        default="",
        description="Name of the collection property to display in the list"
    ).tag_node_drawable(order=3)
    
    active_data_path = ACK.PropTyped.String(
        name="Active Data Path",
        default="",
        description="Full RNA path from context (e.g., 'object.data.attributes')"
    ).tag_node_drawable(order=4)
    
    use_relative_active_data_path = ACK.PropTyped.Bool(
        name="",
        default=False,
        description="Mark if active data path is relative to the data path field"
    ).tag_node_drawable(order=4, text="", icon='DOT')

    active_propname = ACK.PropTyped.String(
        name="Active Property Name",
        default="",
        description="Name of the active (integer) property to display selected list item"
    ).tag_node_drawable(order=5)

    type = ACK.PropTyped.Enum(
        name="Type",
        items=[
            ("DEFAULT", "Default", "Default"),
            ("COMPACT", "Compact", "Compact"),
            ("GRID", "Grid", "Grid"),
        ],
    ).tag_node_drawable(order=6)

    rows = ACK.PropTyped.Int(
        name="Rows",
        min=3,
        default=5,
        description="Default number of rows to display"
    ).tag_node_drawable(order=7)

    max_rows = ACK.PropTyped.Int(
        name="Max Rows",
        default=10,
        description="Maximum number of rows to display"
    ).tag_node_drawable(order=7)

    columns = ACK.PropTyped.Int(
        name="Columns",
        default=3,
        description="Number of columns to display"
    ).tag_node_drawable(order=8, poll=lambda node, _ctx: node.type == 'GRID')

    '''sort_reverse = ACK.PropTyped.Bool(
        name="Sort Reverse",
        default=False,
        description="Sort the list in reverse order"
    ).tag_node_drawable(order=10)

    sort_lock = ACK.PropTyped.Bool(
        name="Sort Lock",
        default=False,
        description="Lock the sort order to default value"
    ).tag_node_drawable(order=11)'''


    # --- Outputs ---
    OutElement = ACK.NE.OutputSocket(ElementSocket, label="Element")

    # --- Execute Method ---
    def execute(self, context: bpy.types.Context, root_layout: bpy.types.UILayout, **kwargs) -> Optional[Dict[str, Dict[str, Any]]]:
        parent_layout: bpy.types.UILayout = kwargs.get('parent_layout', None)
        if not parent_layout:
            # print(f"Warning: PropNode '{self.name}' executed without 'parent_layout' in kwargs.")
            return None

        global ui_list_types_x_names
        if ui_list_types_x_names is None:
            update_ui_list_types()

        if not self.list_type_idname or not ui_list_types_x_names:
            return None

        list_type = ui_list_types_x_names[self.list_type_idname]

        if not self.data_path or not self.propname or not self.active_data_path or not self.active_propname:
            return None

        def _get_owner(context, data_path: str) -> Any:
            try:
                if isinstance(context, bpy.types.Context) and data_path.startswith('context.'):
                    data_path = data_path[len('context.'):]
                else:
                    data_path = data_path
                owner = context.path_resolve(data_path, False),  # coerce to False
                return owner[0]
            except Exception as e:
                print(f"Error: {e}")
                return None

        owner = _get_owner(context, self.data_path)
        active_owner = _get_owner(owner if self.use_relative_active_data_path else context, self.active_data_path)
        if not owner or not active_owner:
            return None

        ## print(f"owner: {owner}")
        ## print(f"active_owner: {active_owner}")

        parent_layout.template_list(
            list_type.bl_idname if hasattr(list_type, 'bl_idname') else list_type.__name__, "",
            owner,
            self.propname,
            active_owner,
            self.active_propname,
            item_dyntip_propname="",
            rows=self.rows,
            maxrows=self.max_rows,
            type=self.type,
            columns=self.columns if self.type == 'GRID' else 9,
            sort_reverse=False, #self.sort_reverse,
            sort_lock=False #self.sort_lock
        )

        # Return None as this node doesn't provide context for children via inputs
        return None
