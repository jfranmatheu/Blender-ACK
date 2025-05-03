import ctypes

class uiFontStyle(ctypes.Structure):
    """ This state defines appearance of text. """
    _fields_ = [
        ("uifont_id", ctypes.c_short),
        ("_pad1", ctypes.c_char * 2),
        ("points", ctypes.c_float),
        ("italic", ctypes.c_short),
        ("bold", ctypes.c_short),
        ("shadow", ctypes.c_short),
        ("shadx", ctypes.c_short),
        ("shady", ctypes.c_short),
        ("_pad0", ctypes.c_char * 2),
        ("shadowalpha", ctypes.c_float),
        ("shadowcolor", ctypes.c_float),
        ("character_weight", ctypes.c_int),
    ]

# Forward declaration for uiStyle
class uiStyle(ctypes.Structure):
    _fields_ = [
        ("next", ctypes.c_void_p),
        ("prev", ctypes.c_void_p),
        ("name", ctypes.c_char * 64),
        ("paneltitle", uiFontStyle),
        ("grouplabel", uiFontStyle),
        ("widget", uiFontStyle),
        ("tooltip", uiFontStyle),
        ("panelzoom", ctypes.c_float),
        ("minlabelchars", ctypes.c_short),
        ("minwidgetchars", ctypes.c_short),
        ("columnspace", ctypes.c_short),
        ("templatespace", ctypes.c_short),
        ("boxspace", ctypes.c_short),
        ("buttonspacex", ctypes.c_short),
        ("buttonspacey", ctypes.c_short),
        ("panelspace", ctypes.c_short),
        ("panelouter", ctypes.c_short),
        ("_pad0", ctypes.c_char * 2),
    ]
