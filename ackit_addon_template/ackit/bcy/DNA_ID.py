import ctypes

MAX_ID_NAME = 66 # From DNA_ID.h

class ID_Runtime_Remap(ctypes.Structure):
    """Runtime data for ID remapping operations."""
    _fields_ = [
        # int status; /* Status during ID remapping. */
        ("status", ctypes.c_int),
        # int skipped_refcounted; /* Skipped use cases that refcount the data-block. */
        ("skipped_refcounted", ctypes.c_int),
        # int skipped_direct; /* Skipped direct use cases that could be remapped. */
        ("skipped_direct", ctypes.c_int),
        # int skipped_indirect; /* Skipped indirect use cases that could not be remapped. */
        ("skipped_indirect", ctypes.c_int),
    ]

class ID_Runtime(ctypes.Structure):
    """Runtime data associated with an ID."""
    _fields_ = [
        # ID_Runtime_Remap remap;
        ("remap", ID_Runtime_Remap),
        # struct Depsgraph *depsgraph; /* Owning depsgraph (if any). */
        ("depsgraph", ctypes.c_void_p),
        # struct ID_Readfile_Data *readfile_data; /* Temporary data used during readfile. */
        ("readfile_data", ctypes.c_void_p),
    ]

# Forward declaration for ID itself needed for orig_id field type hint (though using void_p anyway)
class ID(ctypes.Structure):
    pass

ID._fields_ = [
    # void *next, *prev;
    ("next", ctypes.c_void_p),
    ("prev", ctypes.c_void_p),
    # struct ID *newid;
    ("newid", ctypes.POINTER(ID)),

    # struct Library *lib;
    ("lib", ctypes.c_void_p),

    # struct AssetMetaData *asset_data; /* If the ID is an asset. */
    ("asset_data", ctypes.c_void_p),

    # char name[66]; /* MAX_ID_NAME. */
    ("name", ctypes.c_char * MAX_ID_NAME),
    # short flag; /* ID_FLAG_... */
    ("flag", ctypes.c_short),
    # int tag; /* ID_TAG_... (runtime only). */
    ("tag", ctypes.c_int),
    # int us; /* Users (refcount). */
    ("us", ctypes.c_int),
    # int icon_id;
    ("icon_id", ctypes.c_int),
    # unsigned int recalc;
    ("recalc", ctypes.c_uint),
    # unsigned int recalc_up_to_undo_push;
    ("recalc_up_to_undo_push", ctypes.c_uint),
    # unsigned int recalc_after_undo_push;
    ("recalc_after_undo_push", ctypes.c_uint),

    # unsigned int session_uid; /* Session-wide unique identifier. */
    ("session_uid", ctypes.c_uint),

    # IDProperty *properties;
    ("properties", ctypes.c_void_p),

    # IDOverrideLibrary *override_library; /* Reference linked ID which this one overrides. */
    ("override_library", ctypes.c_void_p),

    # struct ID *orig_id; /* Original ID if copy-on-evaluation or during undo. */
    ("orig_id", ctypes.POINTER(ID)), # Pointer to self type

    # void *py_instance; /* PyObject reference. */
    ("py_instance", ctypes.c_void_p),

    # struct LibraryWeakReference *library_weak_reference; /* Weak reference for re-using appended data. */
    ("library_weak_reference", ctypes.c_void_p),

    # struct ID_Runtime runtime;
    ("runtime", ID_Runtime),
]

# For self-referential pointers (like newid, orig_id)
# ID.newid = ctypes.POINTER(ID) # This is implicitly handled by the _fields_ definition
# ID.orig_id = ctypes.POINTER(ID) # This is implicitly handled by the _fields_ definition
