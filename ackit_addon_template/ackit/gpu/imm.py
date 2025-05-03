import gpu
from gpu_extras.batch import batch_for_shader
from gpu import state as gpu_state
import math
from typing import Tuple

RGBA = Tuple[float, float, float, float]


def rect_2d(x: int, y: int, w: int, h: int, rgba: RGBA):
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(
        shader, 'TRIS',
        {"pos": ((x, y), (x + w, y), (x, y + h), (x + w, y + h))},
        indices=((0, 1, 2), (2, 1, 3))
    )
    gpu_state.blend_set('ADDITIVE_PREMULT')
    shader.uniform_float("color", rgba)
    batch.draw(shader)
    gpu_state.blend_set('NONE')

def rect_rounded_2d(x: int, y: int, w: int, h: int, r: float, rgba: RGBA, segments_per_corner: int = 8):
    """Draws a 2D rounded rectangle using a triangle fan."""
    
    # Clamp radius to valid range
    r = min(r, w / 2, h / 2)
    if r < 0: r = 0

    # --- Generate Perimeter Vertices ---
    perimeter_verts = []
    
    # Calculate corner centers
    cx_bl, cy_bl = x + r, y + r
    cx_br, cy_br = x + w - r, y + r
    cx_tr, cy_tr = x + w - r, y + h - r
    cx_tl, cy_tl = x + r, y + h - r

    # Generate vertices for each corner arc
    # Bottom-left corner (180 to 270 deg)
    start_angle = math.pi
    end_angle = 3 * math.pi / 2
    for i in range(segments_per_corner + 1):
        angle = start_angle + (end_angle - start_angle) * i / segments_per_corner
        vx = cx_bl + r * math.cos(angle)
        vy = cy_bl + r * math.sin(angle)
        perimeter_verts.append((vx, vy))

    # Bottom-right corner (270 to 360 deg)
    start_angle = 3 * math.pi / 2
    end_angle = 2 * math.pi
    for i in range(1, segments_per_corner + 1): # Start from 1 to avoid duplicate vertex
        angle = start_angle + (end_angle - start_angle) * i / segments_per_corner
        vx = cx_br + r * math.cos(angle)
        vy = cy_br + r * math.sin(angle)
        perimeter_verts.append((vx, vy))

    # Top-right corner (0 to 90 deg)
    start_angle = 0
    end_angle = math.pi / 2
    for i in range(1, segments_per_corner + 1): # Start from 1
        angle = start_angle + (end_angle - start_angle) * i / segments_per_corner
        vx = cx_tr + r * math.cos(angle)
        vy = cy_tr + r * math.sin(angle)
        perimeter_verts.append((vx, vy))

    # Top-left corner (90 to 180 deg)
    start_angle = math.pi / 2
    end_angle = math.pi
    for i in range(1, segments_per_corner + 1): # Start from 1
        angle = start_angle + (end_angle - start_angle) * i / segments_per_corner
        vx = cx_tl + r * math.cos(angle)
        vy = cy_tl + r * math.sin(angle)
        perimeter_verts.append((vx, vy))

    # Add a center vertex for the triangle fan
    center_x = x + w / 2
    center_y = y + h / 2
    all_verts = [(center_x, center_y)] + perimeter_verts

    # --- Generate Indices for Triangle Fan ---
    indices = []
    num_perimeter_verts = len(perimeter_verts)
    # Create triangles connecting the center to each pair of adjacent perimeter vertices
    for i in range(num_perimeter_verts):
        p1_idx = 0 # Center vertex index
        p2_idx = i + 1
        # Connect the last perimeter vertex back to the first one
        p3_idx = (i + 1) % num_perimeter_verts + 1 
        indices.append((p1_idx, p2_idx, p3_idx))

    # --- Create Batch and Draw ---
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    
    # batch_for_shader expects a list of vertex coordinate tuples for "pos"
    batch = batch_for_shader(
        shader, 'TRIS',
        {"pos": all_verts}, # Pass the list of (x, y) tuples
        indices=indices
    )
    
    # Enable alpha blending for transparency
    gpu_state.blend_set('MULTIPLY') 
    shader.uniform_float("color", rgba)
    batch.draw(shader)
    # Restore default blend state
    gpu_state.blend_set('NONE')

def rect_3d(x: int, y: int, z: int, w: int, h: int, rgba: RGBA):
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(
        shader, 'TRIS',
        {"pos": ((x, y, z), (x + w, y, z), (x, y + h, z), (x + w, y + h, z))},
        indices=((0, 1, 2), (2, 1, 3))
    )
    gpu_state.blend_set('ALPHA')
    shader.uniform_float("color", rgba)
    batch.draw(shader)
    gpu_state.blend_set('NONE')
