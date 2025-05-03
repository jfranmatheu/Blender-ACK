\
import ctypes

class rctf(ctypes.Structure):
    _fields_ = [
        ("xmin", ctypes.c_float),
        ("xmax", ctypes.c_float),
        ("ymin", ctypes.c_float),
        ("ymax", ctypes.c_float),
    ]

class rcti(ctypes.Structure):
    _fields_ = [
        ("xmin", ctypes.c_int),
        ("xmax", ctypes.c_int),
        ("ymin", ctypes.c_int),
        ("ymax", ctypes.c_int),
    ]
