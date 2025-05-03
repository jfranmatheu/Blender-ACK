import ctypes

# Based on using int2 = VecBase<int32_t, 2>;
# Assuming VecBase<T, N> has a T data[N] member.
class Int2(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.c_int * 2) # int32_t data[2];
    ]

# Forward declarations for types used in GPUViewport
# Representing pointers and complex structs as void_p for now
# struct DRWData;
# struct GPUTexture;
# struct GPUFrameBuffer;
# struct ColorManagedViewSettings;
# struct ColorManagedDisplaySettings;
# struct CurveMapping;
# struct GPUViewportBatch;

class GPUViewport(ctypes.Structure):
    _fields_ = [
        ("size", Int2),                            # blender::int2 size;
        ("flag", ctypes.c_int),                    # int flag;
        ("active_view", ctypes.c_int),             # int active_view;
        ("draw_data", ctypes.c_void_p),            # DRWData *draw_data;
        ("color_render_tx", ctypes.c_void_p * 2),  # GPUTexture *color_render_tx[2];
        ("color_overlay_tx", ctypes.c_void_p * 2), # GPUTexture *color_overlay_tx[2];
        ("depth_tx", ctypes.c_void_p),             # GPUTexture *depth_tx;
        ("stereo_comp_fb", ctypes.c_void_p),       # GPUFrameBuffer *stereo_comp_fb;
        ("overlay_fb", ctypes.c_void_p),           # GPUFrameBuffer *overlay_fb;
        ("view_settings", ctypes.c_void_p),        # ColorManagedViewSettings view_settings;
        ("display_settings", ctypes.c_void_p),     # ColorManagedDisplaySettings display_settings;
        ("orig_curve_mapping", ctypes.c_void_p),   # CurveMapping *orig_curve_mapping;
        ("dither", ctypes.c_float),                # float dither;
        ("do_color_management", ctypes.c_bool),    # bool do_color_management;
        ("batch", ctypes.c_void_p),                # GPUViewportBatch batch;
    ]
