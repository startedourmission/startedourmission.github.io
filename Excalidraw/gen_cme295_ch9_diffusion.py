#!/usr/bin/env python3
"""Generate Diffusion-based LLM diagram for CME295 Chapter 9."""
import sys
sys.path.insert(0, "/Users/chajinwoo/Vaults/AutoVault/Excalidraw")
from gen_diagram import box, text, arrow, save

elements = []
eid = 0
def nid():
    global eid; eid += 1; return f"e{eid}"

# Layout (top to bottom)
cx = 300
y_masked = 80
y_partial = 240
y_complete = 400

token_w = 50
token_h = 34
n_tokens = 6
tokens_w = n_tokens * (token_w + 8)
start_x = cx - tokens_w / 2 + token_w / 2

# --- Row 1: Masked Tokens ---
elements.append(text(nid(), cx, y_masked - 45, "Masked Tokens", size=15))
masked_labels = ["X", "The", "X", "X", "sat", "X"]
for i, label in enumerate(masked_labels):
    tx = start_x + i * (token_w + 8)
    thin = (label != "X")
    elements.append(box(nid(), tx, y_masked, token_w, token_h, thin=thin))
    elements.append(text(nid(), tx, y_masked + token_h/2 + 14, label, size=13, mono=True))

# Arrow down labeled "Reverse (Unmask)"
elements.append(arrow(nid(), cx, y_masked + token_h/2 + 30, cx, y_partial - token_h/2 - 30))
elements.append(text(nid(), cx + 100, (y_masked + y_partial) / 2, "Reverse (Unmask)", size=12))

# --- Row 2: Partially Revealed ---
elements.append(text(nid(), cx, y_partial - 45, "Partially Revealed", size=15))
partial_labels = ["X", "The", "cat", "X", "sat", "on"]
for i, label in enumerate(partial_labels):
    tx = start_x + i * (token_w + 8)
    thin = (label != "X")
    elements.append(box(nid(), tx, y_partial, token_w, token_h, thin=thin))
    elements.append(text(nid(), tx, y_partial + token_h/2 + 14, label, size=13, mono=True))

# Arrow down
elements.append(arrow(nid(), cx, y_partial + token_h/2 + 30, cx, y_complete - token_h/2 - 30))

# --- Row 3: Complete Text ---
elements.append(text(nid(), cx, y_complete - 45, "Complete Text", size=15))
complete_labels = ["Oh", "The", "cat", "really", "sat", "on"]
for i, label in enumerate(complete_labels):
    tx = start_x + i * (token_w + 8)
    elements.append(box(nid(), tx, y_complete, token_w, token_h, thin=True))
    elements.append(text(nid(), tx, y_complete + token_h/2 + 14, label, size=13, mono=True))

# --- Side label: Coarse to Fine ---
label_x = cx + tokens_w / 2 + 60
elements.append(text(nid(), label_x, y_masked, "Coarse", size=14))
elements.append(arrow(nid(), label_x, y_masked + 15, label_x, y_complete - 15))
elements.append(text(nid(), label_x, y_complete, "Fine", size=14))

out_path = "/Users/chajinwoo/Vaults/AutoVault/Excalidraw/cme295-diffusion-llm.excalidraw"
save(out_path, elements)
print("Done: Diffusion-based LLM diagram")
