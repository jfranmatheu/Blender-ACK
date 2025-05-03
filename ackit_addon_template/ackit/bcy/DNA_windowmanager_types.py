import ctypes
from .DNA_list_base import ListBase
from .DNA_screen_type import ScrAreaMap

# Based on DNA_screen_types.h: typedef struct ScrAreaMap { struct ScrArea *next, *prev; } ScrAreaMap;
# Effectively a ListBase

class wmWindow(ctypes.Structure):
    """Window structure (wmWindow)"""
    _fields_ = [
        # struct wmWindow *next, *prev;
        ("next", ctypes.c_void_p), 
        ("prev", ctypes.c_void_p),

        # void *ghostwin; /* Don't want to include ghost.h stuff. */
        ("ghostwin", ctypes.c_void_p),
        # void *gpuctx; /* Don't want to include gpu stuff. */
        ("gpuctx", ctypes.c_void_p),

        # struct wmWindow *parent; /* Parent window. */
        ("parent", ctypes.c_void_p),

        # struct Scene *scene; /* Active scene displayed in this window. */
        ("scene", ctypes.c_void_p),
        # struct Scene *new_scene; /* Temporary when switching. */
        ("new_scene", ctypes.c_void_p),
        # char view_layer_name[64]; /* Active view layer displayed in this window. */
        ("view_layer_name", ctypes.c_char * 64),
        # struct Scene *unpinned_scene; /* The "overridden" or "default" scene */
        ("unpinned_scene", ctypes.c_void_p),

        # struct WorkSpaceInstanceHook *workspace_hook;
        ("workspace_hook", ctypes.c_void_p),

        # ScrAreaMap global_areas; /* Global areas aren't part of the screen */
        ("global_areas", ScrAreaMap),

        # struct bScreen *screen; /* Deprecated */
        ("screen", ctypes.c_void_p),

        # int winid; /* Window-ID */
        ("winid", ctypes.c_int),
        # short posx, posy; /* Window coords (in pixels). */
        ("posx", ctypes.c_short), 
        ("posy", ctypes.c_short),
        # short sizex, sizey; /* Window size (in pixels). */
        ("sizex", ctypes.c_short), 
        ("sizey", ctypes.c_short),
        # char windowstate; /* Normal, maximized, full-screen, #GHOST_TWindowState. */
        ("windowstate", ctypes.c_char),
        # char active; /* Set to 1 if an active window */
        ("active", ctypes.c_char),
        # short cursor; /* Current mouse cursor type. */
        ("cursor", ctypes.c_short),
        # short lastcursor; /* Previous cursor when setting modal one. */
        ("lastcursor", ctypes.c_short),
        # short modalcursor; /* The current modal cursor. */
        ("modalcursor", ctypes.c_short),
        # short grabcursor; /* Cursor grab mode #GHOST_TGrabCursorMode */
        ("grabcursor", ctypes.c_short),

        # short pie_event_type_lock; /* Internal, lock pie creation */
        ("pie_event_type_lock", ctypes.c_short),
        # short pie_event_type_last; /* Exception for nested pies */
        ("pie_event_type_last", ctypes.c_short),

        # char addmousemove; /* Internal: tag for extra mouse-move event */
        ("addmousemove", ctypes.c_char),
        # char tag_cursor_refresh;
        ("tag_cursor_refresh", ctypes.c_char),

        # char event_queue_check_click; /* Enable when #KM_PRESS not handled */
        ("event_queue_check_click", ctypes.c_char),
        # char event_queue_check_drag; /* Enable when #KM_PRESS not handled */
        ("event_queue_check_drag", ctypes.c_char),
        # char event_queue_check_drag_handled; /* Enable when drag was handled */
        ("event_queue_check_drag_handled", ctypes.c_char),

        # char event_queue_consecutive_gesture_type; /* The last event type */
        ("event_queue_consecutive_gesture_type", ctypes.c_char),
        # int event_queue_consecutive_gesture_xy[2]; /* Cursor location for gesture */
        ("event_queue_consecutive_gesture_xy", ctypes.c_int * 2),
        # struct wmEvent_ConsecutiveData *event_queue_consecutive_gesture_data;
        ("event_queue_consecutive_gesture_data", ctypes.c_void_p),

        # struct wmEvent *eventstate; /* Storage for event system */
        ("eventstate", ctypes.c_void_p),
        # struct wmEvent *event_last_handled; /* Last handled event in queue */
        ("event_last_handled", ctypes.c_void_p),

        # const struct wmIMEData *ime_data; /* Input Method Editor data */
        ("ime_data", ctypes.c_void_p),
        # char ime_data_is_composing;
        ("ime_data_is_composing", ctypes.c_char),
        # char _pad1[7];
        ("_pad1", ctypes.c_char * 7),

        # ListBase event_queue; /* All events #wmEvent */
        ("event_queue", ListBase),
        # ListBase handlers; /* Window+screen handlers */
        ("handlers", ListBase),
        # ListBase modalhandlers; /* Priority handlers */
        ("modalhandlers", ListBase),

        # ListBase gesture; /* Gesture stuff. */
        ("gesture", ListBase),

        # struct Stereo3dFormat *stereo3d_format; /* Properties for stereoscopic displays. */
        ("stereo3d_format", ctypes.c_void_p),

        # ListBase drawcalls; /* Custom drawing callbacks. */
        ("drawcalls", ListBase),

        # void *cursor_keymap_status; /* Private runtime info for status bar. */
        ("cursor_keymap_status", ctypes.c_void_p),

        # uint64_t eventstate_prev_press_time_ms; /* Time of last key press */
        ("eventstate_prev_press_time_ms", ctypes.c_uint64),
    ]

# Pointer handling for linked list structure (next, prev, parent)
# Using c_void_p is generally safe, but for more type safety later,
# you might resolve these pointers once all related structures are defined.
# For now, c_void_p avoids definition order issues.
