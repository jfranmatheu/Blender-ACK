import ctypes
import enum
from .DNA_list_base import ListBase
from .DNA_view2d_types import View2D
from .DNA_vec_types import rcti
from .ui_layout import uiLayout
from .DNA_ID import ID
from .wm_draw import wmDrawBuffer


UI_UNIT_Y = 20  # defaults to 20 for 72 DPI setting
PNL_HEADER = UI_UNIT_Y * 1.25


class ARegionDoDrawFlags(enum.IntFlag):
    """ #ARegionRuntime.do_draw """
    DRAW = 1                # Region must be fully redrawn.
    DRAW_PARTIAL = 2        # Redraw only part of region
    DRAW_NO_REBUILD = 4     # Faster redraw without rebuilding (Outliner, 3D Viewport progressive render)
    DRAWING = 8             # Set while region is being drawn.
    REFRESH_UI = 16         # For popups, to refresh UI layout along with drawing.
    DRAW_EDITOR_OVERLAYS = 32 # Only editor overlays (gizmos) should be redrawn.


# Forward declaration for ARegion pointers
class ARegion(ctypes.Structure):
    pass

# Forward declaration needed for ARegionRuntime
class ARegionRuntime(ctypes.Structure):
    def check_do_draw_flag(self, flag: ARegionDoDrawFlags):
        return self.do_draw & flag.value
    
    def check_do_draw_paintcursor_flag(self, flag: ARegionDoDrawFlags):
        return self.do_draw_paintcursor & flag.value

ARegion._fields_ = [
    ("next", ctypes.POINTER(ARegion)),
    ("prev", ctypes.POINTER(ARegion)),
    ("v2d", View2D),
    ("winrct", rcti),
    ("winx", ctypes.c_short),
    ("winy", ctypes.c_short),
    ("category_scroll", ctypes.c_int),
    ("regiontype", ctypes.c_short),
    ("alignment", ctypes.c_short),
    ("flag", ctypes.c_short),
    ("sizex", ctypes.c_short),
    ("sizey", ctypes.c_short),
    ("overlap", ctypes.c_short),
    ("flagfullscreen", ctypes.c_short),
    ("_pad", ctypes.c_char * 2),
    ("panels", ListBase),
    ("panels_category_active", ListBase),
    ("ui_lists", ListBase),
    ("ui_previews", ListBase),
    ("view_states", ListBase),
    ("regiondata", ctypes.c_void_p),
    ("runtime", ctypes.POINTER(ARegionRuntime)), # Updated from c_void_p
]

class PanelFlags(enum.IntFlag):
    """ #Panel.flag """
    SELECT = (1 << 0)
    UNUSED_1 = (1 << 1) # Cleared
    CLOSED = (1 << 2)
    # TABBED = (1 << 3) # UNUSED
    # OVERLAP = (1 << 4) # UNUSED
    PIN = (1 << 5)
    POPOVER = (1 << 6)
    # The panel has been drag-drop reordered and the instanced panel list needs to be rebuilt.
    INSTANCED_LIST_ORDER_CHANGED = (1 << 7)
    
class PanelRuntimeFlags(enum.IntFlag):
    LAST_ADDED = (1 << 0)
    ACTIVE = (1 << 2)
    WAS_ACTIVE = (1 << 3)
    ANIM_ALIGN = (1 << 4)
    NEW_ADDED = (1 << 5)
    SEARCH_FILTER_MATCH = (1 << 7)
    USE_CLOSED_FROM_SEARCH = (1 << 8)
    WAS_CLOSED = (1 << 9)
    IS_DRAG_DROP = (1 << 10)
    ACTIVE_BORDER = (1 << 11)

class PanelTypeFlags(enum.IntFlag):
    """ #PanelType.flag """
    DEFAULT_CLOSED = (1 << 0)
    NO_HEADER = (1 << 1)
    HEADER_EXPAND = (1 << 2)
    LAYOUT_VERT_BAR = (1 << 3)
    INSTANCED = (1 << 4)
    NO_SEARCH = (1 << 7)


# Assuming BKE_ST_MAXNAME = 64
BKE_ST_MAXNAME = 64

# Assuming blender::float2 is struct { float x; float y; } or float data[2];
class Float2(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.c_float * 2) # float data[2];
    ]

# Forward declaration for PanelType pointers
class PanelType(ctypes.Structure):
    _fields_ = [
        ("next", ctypes.c_void_p),           # PanelType *next
        ("prev", ctypes.c_void_p),           # PanelType *prev
        ("idname", ctypes.c_char * BKE_ST_MAXNAME),    # char idname[BKE_ST_MAXNAME];
        ("label", ctypes.c_char * BKE_ST_MAXNAME),     # char label[BKE_ST_MAXNAME];
        ("description", ctypes.c_char_p),              # const char *description;
        ("translation_context", ctypes.c_char * BKE_ST_MAXNAME), # char translation_context[BKE_ST_MAXNAME];
        ("context", ctypes.c_char * BKE_ST_MAXNAME),   # char context[BKE_ST_MAXNAME];
        ("category", ctypes.c_char * BKE_ST_MAXNAME),  # char category[BKE_ST_MAXNAME];
        ("owner_id", ctypes.c_char * 128),             # char owner_id[128];
        ("parent_id", ctypes.c_char * BKE_ST_MAXNAME), # char parent_id[BKE_ST_MAXNAME];
        ("active_property", ctypes.c_char * BKE_ST_MAXNAME), # char active_property[BKE_ST_MAXNAME];
        ("pin_to_last_property", ctypes.c_char * BKE_ST_MAXNAME), # char pin_to_last_property[BKE_ST_MAXNAME];
        ("space_type", ctypes.c_short),                # short space_type;
        ("region_type", ctypes.c_short),               # short region_type;
        ("ui_units_x", ctypes.c_int),                  # int ui_units_x;
        ("offset_units_xy", Float2),                   # blender::float2 offset_units_xy;
        ("order", ctypes.c_int),                       # int order;
        ("flag", ctypes.c_int),                        # int flag; -> PanelTypeFlags
        # ... more attributes if needed ...
    ]


# Forward declaration for Panel pointers
class Panel(ctypes.Structure):
    _fields_ = [
        ("next", ctypes.c_void_p), # Using c_void_p for now, assuming it points to Panel
        ("prev", ctypes.c_void_p), # Using c_void_p for now, assuming it points to Panel
        ("type", ctypes.POINTER(PanelType)),  # struct PanelType * <-- Updated from c_void_p
        ("layout", ctypes.POINTER(uiLayout)),  # struct uiLayout *
        ("panelname", ctypes.c_char * 64),
        ("drawname", ctypes.c_char_p),
        ("ofsx", ctypes.c_int),
        ("ofsy", ctypes.c_int),
        ("sizex", ctypes.c_int),
        ("sizey", ctypes.c_int),
        ("blocksizex", ctypes.c_int),
        ("blocksizey", ctypes.c_int),
        ("labelofs", ctypes.c_short),
        ("flag", ctypes.c_short),  # PanelFlags
        ("runtime_flag", ctypes.c_short),  # PanelFlags
        ("_pad", ctypes.c_char * 6),
        ("sortorder", ctypes.c_int),
        ("activedata", ctypes.c_void_p),
        ("children", ListBase),
        ("layout_panel_states", ListBase),
        ("runtime", ctypes.c_void_p),  # struct Panel_Runtime *
    ]

    # Getters.
    # ------------

    def get_next_panel(self):
        if self.next is None:
            return None
        return self.next.contents

    def get_prev_panel(self):
        if self.prev is None:
            return None
        return self.prev.contents
    
    def get_runtime_data(self):
        if self.runtime is None:
            return None
        return self.runtime.contents
    
    def get_type(self):
        if self.type is None:
            return None
        return self.type.contents

    @property
    def type_flag(self):
        if panel_type := self.get_type():
            return panel_type.flag
        return 0


    # Check flags.
    # ------------

    def check_flag(self, flag: PanelFlags) -> bool:
        return bool(self.flag & flag.value)

    def check_runtime_flag(self, flag: PanelRuntimeFlags) -> bool:
        return bool(self.runtime_flag & flag.value)

    def check_type_flag(self, flag: PanelTypeFlags) -> bool:
        return bool(self.type_flag & flag.value)

    @property
    def is_closed(self) -> bool:
        """ Header-less panels can never be closed, otherwise they could disappear. """
        if not self.has_header:
            return False

        if self.check_runtime_flag(PanelRuntimeFlags.USE_CLOSED_FROM_SEARCH):
            return False  # TODO: !UI_panel_matches_search_filter(panel);

        return self.check_flag(PanelFlags.CLOSED)

    @property
    def is_dragging(self) -> bool:
        return self.check_runtime_flag(PanelRuntimeFlags.IS_DRAG_DROP)

    @property
    def is_pinned(self) -> bool:
        return self.check_flag(PanelFlags.PIN)

    @property
    def is_selected(self) -> bool:
        return self.check_flag(PanelFlags.SELECT)

    @property
    def is_active(self) -> bool:
        return self.check_runtime_flag(PanelRuntimeFlags.ACTIVE)

    @property
    def is_active_border(self) -> bool:
        return self.check_runtime_flag(PanelRuntimeFlags.ACTIVE_BORDER)

    @property
    def has_header(self) -> bool:
        return not self.check_type_flag(PanelTypeFlags.NO_HEADER)


    # Utils.
    # ------------

    def get_panel_size_y(self):
        if self.check_type_flag(PanelTypeFlags.NO_HEADER):
            return self.sizey
        return PNL_HEADER + self.sizey

    def get_panel_real_size_y(self):
        sizey = 0 if self.is_closed else self.sizey

        if self.check_type_flag(PanelTypeFlags.NO_HEADER):
            return sizey

        return PNL_HEADER + sizey
    
    def get_panel_real_ofsy(self):
        if self.is_closed:
            return self.ofsy + self.sizey
        return self.ofsy


# Define ARegionRuntime structure
ARegionRuntime._fields_ = [
    ("type", ctypes.c_void_p),            # struct ARegionType *
    ("drawrct", rcti),
    ("visible_rect", rcti),
    ("offset_x", ctypes.c_int),
    ("offset_y", ctypes.c_int),
    ("category", ctypes.c_char_p),
    ("block_name_map", ctypes.c_void_p * 64),   # Map<std::string, uiBlock *> # ≈ 56–64 bytes
    ("uiblocks", ListBase),
    ("handlers", ListBase),
    ("headerstr", ctypes.c_char_p),
    ("gizmo_map", ctypes.c_void_p),        # wmGizmoMap *
    ("regiontimer", ctypes.c_void_p),      # wmTimer *
    ("draw_buffer", ctypes.POINTER(wmDrawBuffer)),      # wmDrawBuffer *
    ("panels_category", ListBase),  # ListBase of PanelCategoryDyn *
    ("visible", ctypes.c_short),
    ("do_draw", ctypes.c_short),
    ("do_draw_paintcursor", ctypes.c_short),
    ("popup_block_panel", ctypes.POINTER(Panel)) # Panel *
]

class ScrAreaMap(ctypes.Structure):
    """Area map structure (ScrAreaMap)"""
    _fields_ = [
        # ListBase vertbase; /* ScrVert - screens have vertices/edges to define areas. */
        ("vertbase", ListBase),
        # ListBase edgebase; /* ScrEdge. */
        ("edgebase", ListBase),
        # ListBase areabase; /* ScrArea. */
        ("areabase", ListBase),
    ]

class bScreen(ctypes.Structure):
    """Screen structure (bScreen)"""
    _fields_ = [
        # ID id;
        ("id", ID),

        # ListBase vertbase;
        ("vertbase", ListBase),
        # ListBase edgebase;
        ("edgebase", ListBase),
        # ListBase areabase;
        ("areabase", ListBase),
        # ListBase regionbase; /* Screen level regions (menus), runtime only. */
        ("regionbase", ListBase),

        # struct Scene *scene; /* Deprecated */
        ("scene", ctypes.c_void_p),

        # short flag; /* General flags. */
        ("flag", ctypes.c_short),
        # short winid; /* Window-ID from WM, starts with 1. */
        ("winid", ctypes.c_short),
        # short redraws_flag; /* User-setting for redraws during animation playback. */
        ("redraws_flag", ctypes.c_short),

        # char temp; /* Temp screen, don't save */
        ("temp", ctypes.c_char),
        # char state; /* Temp screen for image render or file-select. */
        ("state", ctypes.c_char),
        # char do_draw; /* Notifier for drawing edges. */
        ("do_draw", ctypes.c_char),
        # char do_refresh; /* Notifier for scale screen, etc. */
        ("do_refresh", ctypes.c_char),
        # char do_draw_gesture; /* Notifier for gesture draw. */
        ("do_draw_gesture", ctypes.c_char),
        # char do_draw_paintcursor; /* Notifier for paint cursor draw. */
        ("do_draw_paintcursor", ctypes.c_char),
        # char do_draw_drag; /* Notifier for dragging draw. */
        ("do_draw_drag", ctypes.c_char),
        # char skip_handling; /* Delay screen handling after maximizing area. */
        ("skip_handling", ctypes.c_char),
        # char scrubbing; /* Set when scrubbing to avoid costly updates. */
        ("scrubbing", ctypes.c_char),
        # char _pad[1];
        ("_pad", ctypes.c_char * 1),

        # struct ARegion *active_region; /* Active region with mouse focus. */
        ("active_region", ctypes.POINTER(ARegion)),

        # struct wmTimer *animtimer; /* Screen's timer handler. */
        ("animtimer", ctypes.c_void_p),
        # void /*bContextDataCallback*/ *context; /* Context callback. */
        ("context", ctypes.c_void_p),

        # struct wmTooltipState *tool_tip; /* Runtime tooltip state. */
        ("tool_tip", ctypes.c_void_p),

        # PreviewImage *preview;
        ("preview", ctypes.c_void_p),
    ]

