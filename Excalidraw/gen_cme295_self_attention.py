#!/usr/bin/env python3
"""Generate self-attention mechanism diagram for CME295 Chapter 1."""
import sys
sys.path.insert(0, "/Users/chajinwoo/Vaults/AutoVault/Excalidraw")
from gen_diagram import box, text, arrow, conn, save

elements = []
eid = 0
def nid():
    global eid; eid += 1; return f"e{eid}"

# Layout constants
tokens = ["a", "cute", "teddy", "bear"]
n = len(tokens)
col_spacing = 130
start_x = 100
y_input = 50       # input token boxes
y_qkv_label = 130  # Q, K, V labels
y_matrix = 280     # attention matrix center
y_output = 460     # output tokens

# --- Input token boxes ---
input_centers = []
for i, tok in enumerate(tokens):
    cx = start_x + i * col_spacing
    input_centers.append((cx, y_input))
    elements.append(box(nid(), cx, y_input, 80, 36))
    elements.append(text(nid(), cx, y_input, tok, size=16))

# --- Q, K, V projection labels ---
qkv_labels = ["Q", "K", "V"]
qkv_y_offsets = [0, 22, 44]
for i in range(n):
    cx = start_x + i * col_spacing
    for j, label in enumerate(qkv_labels):
        ly = y_qkv_label + qkv_y_offsets[j]
        elements.append(text(nid(), cx, ly, label, size=13, mono=True))
    # Arrow from input box bottom to Q/K/V area
    elements.append(arrow(nid(), cx, y_input + 18, cx, y_qkv_label - 12))

# --- Attention matrix (4x4 grid) ---
matrix_cx = start_x + (n - 1) * col_spacing / 2  # center of all columns
matrix_cy = y_matrix
cell = 50
grid_w = n * cell
grid_h = n * cell
# Outer border
elements.append(box(nid(), matrix_cx, matrix_cy, grid_w, grid_h, thin=True))

# Grid lines (inner)
for i in range(1, n):
    # Vertical lines
    x_line = matrix_cx - grid_w/2 + i * cell
    elements.append(conn(nid(), x_line, matrix_cy - grid_h/2, x_line, matrix_cy + grid_h/2))
    # Horizontal lines
    y_line = matrix_cy - grid_h/2 + i * cell
    elements.append(conn(nid(), matrix_cx - grid_w/2, y_line, matrix_cx + grid_w/2, y_line))

# Row labels (left side) - which token is the query
for i, tok in enumerate(tokens):
    lx = matrix_cx - grid_w/2 - 30
    ly = matrix_cy - grid_h/2 + i * cell + cell/2
    elements.append(text(nid(), lx, ly, tok, size=11))

# Column labels (top) - which token is the key
for j, tok in enumerate(tokens):
    lx = matrix_cx - grid_w/2 + j * cell + cell/2
    ly = matrix_cy - grid_h/2 - 15
    elements.append(text(nid(), lx, ly, tok, size=11))

# Fill cells with dot symbols to indicate attention weights
for i in range(n):
    for j in range(n):
        cx_cell = matrix_cx - grid_w/2 + j * cell + cell/2
        cy_cell = matrix_cy - grid_h/2 + i * cell + cell/2
        # Vary dot to suggest different weights
        elements.append(text(nid(), cx_cell, cy_cell, ".", size=18))

# Formula label
elements.append(text(nid(), matrix_cx, matrix_cy + grid_h/2 + 22, "Q * K^T / sqrt(d_k)", size=13, mono=True))

# Arrows from Q/K/V area to matrix
for i in range(n):
    cx = start_x + i * col_spacing
    elements.append(arrow(nid(), cx, y_qkv_label + 56,
                          matrix_cx - grid_w/2 + i * cell + cell/2, matrix_cy - grid_h/2 - 25))

# --- Output token boxes ---
output_centers = []
for i, tok in enumerate(tokens):
    cx = start_x + i * col_spacing
    output_centers.append((cx, y_output))
    elements.append(box(nid(), cx, y_output, 80, 36))
    elements.append(text(nid(), cx, y_output, tok + "'", size=14))

# Arrows from matrix bottom to output
for i in range(n):
    cx = start_x + i * col_spacing
    elements.append(arrow(nid(), matrix_cx - grid_w/2 + i * cell + cell/2, matrix_cy + grid_h/2 + 38,
                          cx, y_output - 18))

# --- Title / section labels ---
elements.append(text(nid(), matrix_cx, y_input - 35, "Self-Attention Mechanism", size=20))
elements.append(text(nid(), matrix_cx - grid_w/2 - 75, matrix_cy, "Attention\nScores", size=12))

out_path = "/Users/chajinwoo/Vaults/AutoVault/Excalidraw/cme295-self-attention.excalidraw"
save(out_path, elements)
print("Done: self-attention diagram")
