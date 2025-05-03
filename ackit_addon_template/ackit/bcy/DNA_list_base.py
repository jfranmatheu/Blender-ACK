import ctypes

class ListBase(ctypes.Structure):
    _fields_ = [
        ("first", ctypes.c_void_p),
        ("last", ctypes.c_void_p),
    ]
