import ctypes
from .gpu_framebuffer import GPUOffScreen
from .gpu_viewport import GPUViewport


# Define wmDrawBuffer structure
class wmDrawBuffer(ctypes.Structure):
    _fields_ = [
        ("offscreen", ctypes.POINTER(GPUOffScreen)), # GPUOffScreen *
        ("viewport", ctypes.POINTER(GPUViewport)), # GPUViewport * <--- Changed from c_void_p
        ("stereo", ctypes.c_bool),
        ("bound_view", ctypes.c_int),
    ]
