import ctypes
from ctypes import (
    Structure, POINTER, CFUNCTYPE,
    c_int, c_float, c_char, c_char_p, c_void_p, c_short, c_bool, c_uint8,
    c_int8, c_byte, c_int64
)

# Constants
UI_MAX_NAME_STR = 128
BKE_ST_MAXNAME = 64

# Enums (represented as integers in ctypes)

# enum class EmbossType : uint8_t
EmbossType_Emboss = 0
EmbossType_None = 1
EmbossType_Pulldown = 2
EmbossType_PieMenu = 3
EmbossType_NoneOrStatus = 4
EmbossType_Undefined = 255

# enum uiItemType
ITEM_BUTTON = 0
ITEM_LAYOUT_ROW = 1
ITEM_LAYOUT_PANEL_HEADER = 2
ITEM_LAYOUT_PANEL_BODY = 3
ITEM_LAYOUT_COLUMN = 4
ITEM_LAYOUT_COLUMN_FLOW = 5
ITEM_LAYOUT_ROW_FLOW = 6
ITEM_LAYOUT_GRID_FLOW = 7
ITEM_LAYOUT_BOX = 8
ITEM_LAYOUT_ABSOLUTE = 9
ITEM_LAYOUT_SPLIT = 10
ITEM_LAYOUT_OVERLAP = 11
ITEM_LAYOUT_RADIAL = 12
ITEM_LAYOUT_ROOT = 13

# enum uiItemInternalFlag
UI_ITEM_AUTO_FIXED_SIZE = 1 << 0
UI_ITEM_FIXED_SIZE = 1 << 1
UI_ITEM_BOX_ITEM = 1 << 2
UI_ITEM_PROP_SEP = 1 << 3
UI_ITEM_INSIDE_PROP_SEP = 1 << 4
UI_ITEM_PROP_DECORATE = 1 << 5
UI_ITEM_PROP_DECORATE_NO_PAD = 1 << 6

# Forward declaration for pointers needed by function types first
class HeaderType(Structure): pass
class Header(Structure): pass

# Function pointer types
# Opaque pointers for unknown/incomplete types like bContext, PointerRNA, etc.
bContext_p = c_void_p
PointerRNA_p = c_void_p
FunctionRNA_p = c_void_p
ParameterList_p = c_void_p
StructRNA_p = c_void_p
uiLayoutRoot_p = c_void_p
bContextStore_p = c_void_p
uiItem_p = c_void_p # Representing blender::Vector<uiItem *> as opaque
uiStyle_p = c_void_p
uiBlock_p = c_void_p

StructCallbackFunc = CFUNCTYPE(c_int, bContext_p, PointerRNA_p, FunctionRNA_p, ParameterList_p)
StructFreeFunc = CFUNCTYPE(None, c_void_p)
HeaderPollFunc = CFUNCTYPE(c_bool, bContext_p, POINTER(HeaderType))
HeaderDrawFunc = CFUNCTYPE(None, bContext_p, POINTER(Header))
uiMenuHandleFunc = CFUNCTYPE(None, bContext_p, c_void_p, c_int)

# Define padding type for clarity
Padding = c_byte

# ExtensionRNA structure
class ExtensionRNA(Structure):
    _fields_ = [
        ("data", c_void_p),
        ("srna", StructRNA_p),
        ("call", StructCallbackFunc),
        ("free", StructFreeFunc),
    ]


class uiItem(Structure):
    _fields_ = [
        # --- Offset 0 --- (8 bytes)
        ("vtable", c_void_p),   # Hidden pointer due to virtual destructor

        # --- Offset 8 --- (8 bytes)
        ("type", c_int),        # uiItemType enum (4 bytes)
        ("flag", c_int)         # uiItemInternalFlag enum (4 bytes)
        # Total size = 16 bytes. Already multiple of 8 (alignment of vtable pointer),
        # so no padding needed at the end.
    ]


class rctf(Structure):
    _fields_ = [
        ("xmin", c_float),
        ("xmax", c_float),
        ("ymin", c_float),
        ("ymax", c_float),
    ]
    # Total size = 4 * 4 = 16 bytes

class uiLayoutRoot(Structure):
    _fields_ = [
        # --- Offset 0 --- (16 bytes)
        ("next", c_void_p),
        ("prev", c_void_p),

        # --- Offset 16 --- (8 bytes)
        ("type", c_int),            # 4 bytes
        ("opcontext", c_short),     # 2 bytes (Enum mapped to short)

        # --- Offset 24 --- (12 bytes)
        ("emw", c_int),             # 4 bytes
        ("emh", c_int),             # 4 bytes
        # ("padding", c_int),         # 4 bytes

        # --- Offset 40 --- (16 bytes)
        ("handlefunc", uiMenuHandleFunc), # 8 bytes (Function pointer)
        ("argv", c_void_p),         # 8 bytes (void*)

        # --- Offset 56 --- (24 bytes)
        ("style", c_void_p),       # 8 bytes (const uiStyle*)
        ("block", c_void_p),       # 8 bytes (uiBlock*)
        ("layout", c_void_p), # 8 bytes (uiLayout*)
        # Total size = 80 bytes. Already multiple of 8.
    ]


class uiBut(Structure):
    _fields_ = [
        # --- Offset 0 --- (16 bytes)
        ("next", c_void_p),
        ("prev", c_void_p),

        # --- Offset 16 --- (8 bytes)
        ("layout", c_void_p), # Pointer to the previously defined uiLayout

        # --- Offset 24 --- (20 bytes)
        ("flag", c_int),            # 4 bytes
        ("flag2", c_int),           # 4 bytes
        ("drawflag", c_int),        # 4 bytes
        ("type", c_short),            # 4 bytes (Assuming eButType maps to int)
        ("pointype", c_short),        # 4 bytes (Assuming eButPointerType maps to int)

        # --- Offset 44 --- (18 bytes)
        ("bit", c_short),           # 2 bytes
        ("bitnr", c_short),         # 2 bytes
        ("retval", c_short),        # 2 bytes
        ("strwidth", c_short),      # 2 bytes
        ("alignnr", c_short),       # 2 bytes
        ("ofs", c_short),           # 2 bytes
        ("pos", c_short),           # 2 bytes
        ("selsta", c_short),        # 2 bytes
        ("selend", c_short),        # 2 bytes

        # --- Offset 64 --- (64 bytes) - std::string members (assuming 32 bytes each)
        ("str", c_byte * 24),      # Placeholder for std::string
        ("drawstr", c_byte * 24),  # Placeholder for std::string

        # --- Offset 128 --- (8 bytes)
        ("placeholder", c_char_p),  # char*

        # --- Offset 136 --- (16 bytes)
        ("rect", rctf),             # Embed the rctf struct

    ]


class uiLayout(Structure):
    _fields_ = [
        # --- Offset 0 --- (8 bytes) - Inherited vtable from uiItem
        ("vtable", c_void_p),

        # --- Offset 8 --- (8 bytes) - Inherited from uiItem
        ("type", c_int),        # uiItemType enum (4 bytes)
        ("flag", c_int),        # uiItemInternalFlag enum (4 bytes)

        # --- Offset 16 --- (24 bytes) - uiLayout members
        ("root", c_void_p),    # Pointer
        ("context", c_void_p), # Pointer
        ("parent", c_void_p), # Pointer (using specific type here is fine)

        # --- Offset 40 --- (32 bytes) - blender::Vector<uiItem *> items (Debug Build)
        ("items_begin_", c_void_p),      # T* begin_
        ("items_end_", c_void_p),        # T* end_
        ("items_capacity_end_", c_void_p), # T* capacity_end_
        ("items_debug_size_", c_int64), # int64_t debug_size_
        
        # unknown
        ("_unknown_data", c_byte * 18),

        # --- Offset 72 --- (128 bytes) - uiLayout member
        ("heading", c_char * UI_MAX_NAME_STR),

        # --- Offset 200 --- (8 bytes) - uiLayout member
        ("child_items_layout", c_void_p), # Pointer

        # --- Offset 208 --- (16 bytes) - uiLayout members
        ("x", c_int),
        ("y", c_int),
        ("w", c_int),
        ("h", c_int),

        # --- Offset 224 --- (8 bytes) - uiLayout member
        ("scale", c_float * 2),

        # --- Offset 232 --- (12 bytes) - uiLayout members
        ("space", c_short),             # 2 bytes
        ("align", c_bool),             # 1 byte
        ("active", c_bool),            # 1 byte
        ("active_default", c_bool),    # 1 byte
        ("activate_init", c_bool),     # 1 byte
        ("enabled", c_bool),           # 1 byte
        ("redalert", c_bool),          # 1 byte
        ("keepaspect", c_bool),        # 1 byte
        ("variable_size", c_bool),     # 1 byte
        ("alignment", c_char),         # 1 byte
        ("emboss", c_short),           # 2 bytes  # or maybe c_uint8 (1 byte)?

        # --- Offset 248 --- (8 bytes) - uiLayout member
        ("units", c_float * 2),

        # --- Offset 256 --- (4 bytes) - uiLayout member
        ("search_weight", c_float),

        # --- Offset 260 --- (4 bytes padding)
        # ("_pad1", Padding * 4), # Pad to make total size (264) multiple of 8
        
        # uiLayoutItemBx...
        ("roundbox", uiBut)
    ]

# Verify calculated size
struct_size = ctypes.sizeof(uiLayout)
expected_size = 264
if struct_size != expected_size:
    print(f"WARNING: Calculated ctypes uiLayout size ({struct_size}) does not match expected size ({expected_size})!")

# HeaderType structure definition (uses Header)
HeaderType._fields_ = [
    ("next", POINTER(HeaderType)),
    ("prev", POINTER(HeaderType)),
    ("idname", c_char * BKE_ST_MAXNAME),
    ("space_type", c_int),
    ("region_type", c_int),
    ("poll", HeaderPollFunc),
    ("draw", HeaderDrawFunc),
    ("rna_ext", ExtensionRNA),
]

# Header structure definition (uses HeaderType and uiLayout)
Header._fields_ = [
    ("type", POINTER(HeaderType)),
    ("layout", POINTER(uiLayout)),
]

# Clean up temporary classes used only for forward declaration hints
# del HeaderType
# del Header
# del uiLayout
