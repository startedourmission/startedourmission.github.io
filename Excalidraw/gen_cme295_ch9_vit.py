#!/usr/bin/env python3
"""Generate Vision Transformer diagram for CME295 Chapter 9."""
import sys
sys.path.insert(0, "/Users/chajinwoo/Vaults/AutoVault/Excalidraw")
from gen_diagram import box, text, arrow, conn, save

elements = []
eid = 0
def nid():
    global eid; eid += 1; return f"e{eid}"

# Layout (left to right)
y_main = 200
x_image = 60
x_patches = 200
x_flatten = 370
x_posemb = 530
x_encoder = 680
x_cls = 830
x_class = 960

# --- Image ---
elements.append(box(nid(), x_image, y_main, 80, 80))
elements.append(text(nid(), x_image, y_main, "Image", size=14))

# Arrow
elements.append(arrow(nid(), x_image + 40, y_main, x_patches - 55, y_main))

# --- Patches (3x3 grid) ---
patch_size = 24
grid_n = 3
grid_w = grid_n * patch_size
grid_h = grid_n * patch_size
patches_cx = x_patches
patches_cy = y_main

# Outer border
elements.append(box(nid(), patches_cx, patches_cy, grid_w, grid_h, thin=True))

# Inner grid lines
for i in range(1, grid_n):
    # Vertical
    lx = patches_cx - grid_w/2 + i * patch_size
    elements.append(conn(nid(), lx, patches_cy - grid_h/2, lx, patches_cy + grid_h/2))
    # Horizontal
    ly = patches_cy - grid_h/2 + i * patch_size
    elements.append(conn(nid(), patches_cx - grid_w/2, ly, patches_cx + grid_w/2, ly))

elements.append(text(nid(), patches_cx, patches_cy + grid_h/2 + 16, "Patches", size=12))

# Arrow
elements.append(arrow(nid(), patches_cx + grid_w/2 + 5, y_main, x_flatten - 70, y_main))

# --- Flatten + Linear ---
elements.append(box(nid(), x_flatten, y_main, 120, 44))
elements.append(text(nid(), x_flatten, y_main - 8, "Flatten +", size=13))
elements.append(text(nid(), x_flatten, y_main + 10, "Linear", size=13))

# Arrow
elements.append(arrow(nid(), x_flatten + 60, y_main, x_posemb - 65, y_main))

# --- Position Embedding ---
elements.append(box(nid(), x_posemb, y_main, 120, 44))
elements.append(text(nid(), x_posemb, y_main - 8, "Position", size=13))
elements.append(text(nid(), x_posemb, y_main + 10, "Embedding", size=13))

# Arrow
elements.append(arrow(nid(), x_posemb + 60, y_main, x_encoder - 40, y_main))

# --- Transformer Encoder (tall box) ---
elements.append(box(nid(), x_encoder, y_main, 80, 120))
elements.append(text(nid(), x_encoder, y_main - 15, "Transformer", size=13))
elements.append(text(nid(), x_encoder, y_main + 5, "Encoder", size=13))

# Arrow
elements.append(arrow(nid(), x_encoder + 40, y_main, x_cls - 55, y_main))

# --- [CLS] Token ---
elements.append(box(nid(), x_cls, y_main, 100, 44))
elements.append(text(nid(), x_cls, y_main, "[CLS] Token", size=13))

# Arrow
elements.append(arrow(nid(), x_cls + 50, y_main, x_class - 65, y_main))

# --- Classification ---
elements.append(box(nid(), x_class, y_main, 120, 44))
elements.append(text(nid(), x_class, y_main, "Classification", size=14))

out_path = "/Users/chajinwoo/Vaults/AutoVault/Excalidraw/cme295-vit.excalidraw"
save(out_path, elements)
print("Done: ViT diagram")
