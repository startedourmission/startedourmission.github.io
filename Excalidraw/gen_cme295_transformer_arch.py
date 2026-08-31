#!/usr/bin/env python3
"""Generate Transformer encoder-decoder architecture diagram for CME295 Chapter 1."""
import sys
sys.path.insert(0, "/Users/chajinwoo/Vaults/AutoVault/Excalidraw")
from gen_diagram import box, text, arrow, conn, save

elements = []
eid = 0
def nid():
    global eid; eid += 1; return f"e{eid}"

# Layout
enc_x = 180     # encoder column center
dec_x = 520     # decoder column center
box_w = 220
box_h = 40
gap = 65        # vertical gap between boxes

# --- Title ---
mid_x = (enc_x + dec_x) / 2
elements.append(text(nid(), mid_x, 20, "Transformer Architecture", size=22))

# ========== ENCODER (left) ==========
elements.append(text(nid(), enc_x, 65, "Encoder", size=18))

enc_boxes_labels = [
    "Input Embedding + Position",
    "Multi-Head Self-Attention",
    "Feed Forward",
]
enc_y_start = 110
enc_centers = []
for i, label in enumerate(enc_boxes_labels):
    cy = enc_y_start + i * gap
    enc_centers.append((enc_x, cy))
    elements.append(box(nid(), enc_x, cy, box_w, box_h))
    elements.append(text(nid(), enc_x, cy, label, size=13))

# Arrows between encoder boxes (upward data flow shown as downward connection)
for i in range(len(enc_centers) - 1):
    x1, y1 = enc_centers[i]
    x2, y2 = enc_centers[i + 1]
    elements.append(arrow(nid(), x1, y1 + box_h/2, x2, y2 - box_h/2))

# "x N" label next to encoder stack
enc_stack_top = enc_centers[1][1] - box_h/2
enc_stack_bot = enc_centers[2][1] + box_h/2
enc_bracket_x = enc_x + box_w/2 + 20
elements.append(text(nid(), enc_bracket_x + 18, (enc_stack_top + enc_stack_bot)/2, "x N", size=16))
# Bracket lines
elements.append(conn(nid(), enc_bracket_x, enc_stack_top, enc_bracket_x + 8, enc_stack_top))
elements.append(conn(nid(), enc_bracket_x, enc_stack_bot, enc_bracket_x + 8, enc_stack_bot))
elements.append(conn(nid(), enc_bracket_x + 8, enc_stack_top, enc_bracket_x + 8, enc_stack_bot))

# Encoder output label
enc_out_y = enc_centers[-1][1] + box_h/2 + 20
elements.append(text(nid(), enc_x, enc_out_y + 5, "Encoder Output", size=12))

# ========== DECODER (right) ==========
elements.append(text(nid(), dec_x, 65, "Decoder", size=18))

dec_boxes_labels = [
    "Output Embedding + Position",
    "Masked Self-Attention",
    "Cross-Attention",
    "Feed Forward",
    "Linear + Softmax",
]
dec_y_start = 110
dec_centers = []
for i, label in enumerate(dec_boxes_labels):
    cy = dec_y_start + i * gap
    dec_centers.append((dec_x, cy))
    elements.append(box(nid(), dec_x, cy, box_w, box_h))
    elements.append(text(nid(), dec_x, cy, label, size=13))

# Arrows between decoder boxes
for i in range(len(dec_centers) - 1):
    x1, y1 = dec_centers[i]
    x2, y2 = dec_centers[i + 1]
    elements.append(arrow(nid(), x1, y1 + box_h/2, x2, y2 - box_h/2))

# "x N" label next to decoder stack (covers Masked Self-Attention through Feed Forward)
dec_stack_top = dec_centers[1][1] - box_h/2
dec_stack_bot = dec_centers[3][1] + box_h/2
dec_bracket_x = dec_x + box_w/2 + 20
elements.append(text(nid(), dec_bracket_x + 18, (dec_stack_top + dec_stack_bot)/2, "x N", size=16))
elements.append(conn(nid(), dec_bracket_x, dec_stack_top, dec_bracket_x + 8, dec_stack_top))
elements.append(conn(nid(), dec_bracket_x, dec_stack_bot, dec_bracket_x + 8, dec_stack_bot))
elements.append(conn(nid(), dec_bracket_x + 8, dec_stack_top, dec_bracket_x + 8, dec_stack_bot))

# --- Cross-attention arrow from encoder to decoder ---
# Arrow from encoder output area to Cross-Attention box in decoder
cross_attn_cy = dec_centers[2][1]  # Cross-Attention y
# Draw arrow from encoder top output to decoder cross-attention
elements.append(arrow(nid(), enc_x + box_w/2, enc_out_y,
                       dec_x - box_w/2, cross_attn_cy))
# Label on the cross-attention arrow
arrow_mid_x = (enc_x + box_w/2 + dec_x - box_w/2) / 2
arrow_mid_y = (enc_out_y + cross_attn_cy) / 2 - 15
elements.append(text(nid(), arrow_mid_x, arrow_mid_y, "K, V", size=14))

# Output label at bottom
out_y = dec_centers[-1][1] + box_h/2 + 20
elements.append(text(nid(), dec_x, out_y + 5, "Output Probabilities", size=12))

out_path = "/Users/chajinwoo/Vaults/AutoVault/Excalidraw/cme295-transformer-architecture.excalidraw"
save(out_path, elements)
print("Done: transformer architecture diagram")
