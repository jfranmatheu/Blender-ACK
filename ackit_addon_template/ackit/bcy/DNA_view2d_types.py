import ctypes
from .DNA_vec_types import rctf, rcti

class View2D(ctypes.Structure):
    _fields_ = [
        ("tot", rctf),
        ("cur", rctf),
        ("vert", rcti),
        ("hor", rcti),
        ("mask", rcti),
        ("min", ctypes.c_float * 2),
        ("max", ctypes.c_float * 2),
        ("minzoom", ctypes.c_float),
        ("maxzoom", ctypes.c_float),
        ("scroll", ctypes.c_short),
        ("scroll_ui", ctypes.c_short),
        ("keeptot", ctypes.c_short),
        ("keepzoom", ctypes.c_short),
        ("keepofs", ctypes.c_short),
        ("flag", ctypes.c_short),
        ("align", ctypes.c_short),
        ("winx", ctypes.c_short),
        ("winy", ctypes.c_short),
        ("oldwinx", ctypes.c_short),
        ("oldwiny", ctypes.c_short),
        ("around", ctypes.c_short),
        ("alpha_vert", ctypes.c_char),
        ("alpha_hor", ctypes.c_char),
        ("_pad", ctypes.c_char * 2),
        ("page_size_y", ctypes.c_float),
        ("sms", ctypes.c_void_p),  # struct SmoothView2DStore *
        ("smooth_timer", ctypes.c_void_p),  # struct wmTimer *
    ]
