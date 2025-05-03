import ctypes

# Forward declaration for GPUOffScreen
class GPUOffScreen(ctypes.Structure):
    pass

# Inner structure for framebuffers array in GPUOffScreen
class FramebufferInfo(ctypes.Structure):
    _fields_ = [
        ("ctx", ctypes.c_void_p),  # Context *
        ("fb", ctypes.c_void_p),   # GPUFrameBuffer *
    ]

# Define GPUOffScreen structure
GPUOffScreen._fields_ = [
    ("framebuffers", FramebufferInfo * 3), # Uses MAX_CTX_FB_LEN = 3
    ("color", ctypes.c_void_p),          # GPUTexture *
    ("depth", ctypes.c_void_p),          # GPUTexture *
]
