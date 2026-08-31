#!/usr/bin/env python3
"""Generate LLM-as-a-Judge diagram for CME295 Chapter 8."""
import sys
sys.path.insert(0, "/Users/chajinwoo/Vaults/AutoVault/Excalidraw")
from gen_diagram import box, text, arrow, save

elements = []
eid = 0
def nid():
    global eid; eid += 1; return f"e{eid}"

# Layout (top to bottom, centered)
cx = 300
y_input = 60
y_judge = 190
y_outputs = 320

# --- Input box ---
elements.append(box(nid(), cx, y_input, 300, 50))
elements.append(text(nid(), cx, y_input, "Prompt + Response + Criteria", size=15))

# Arrow to Judge LLM
elements.append(arrow(nid(), cx, y_input + 25, cx, y_judge - 30))

# --- Judge LLM ---
elements.append(box(nid(), cx, y_judge, 160, 55))
elements.append(text(nid(), cx, y_judge, "Judge LLM", size=18))

# Arrow to outputs (fan out)
x_rationale = cx - 100
x_score = cx + 100

elements.append(arrow(nid(), cx - 30, y_judge + 28, x_rationale, y_outputs - 25))
elements.append(arrow(nid(), cx + 30, y_judge + 28, x_score, y_outputs - 25))

# --- Rationale ---
elements.append(box(nid(), x_rationale, y_outputs, 140, 44))
elements.append(text(nid(), x_rationale, y_outputs, "Rationale", size=16))

# --- Score ---
elements.append(box(nid(), x_score, y_outputs, 120, 44))
elements.append(text(nid(), x_score, y_outputs, "Score", size=16))

# --- Side note: Biases ---
bias_x = cx + 250
bias_y = y_judge
elements.append(text(nid(), bias_x, bias_y - 20, "Biases:", size=14))
elements.append(text(nid(), bias_x, bias_y + 2, "Position", size=12))
elements.append(text(nid(), bias_x, bias_y + 20, "Verbosity", size=12))
elements.append(text(nid(), bias_x, bias_y + 38, "Self-enhancement", size=12))

out_path = "/Users/chajinwoo/Vaults/AutoVault/Excalidraw/cme295-llm-judge.excalidraw"
save(out_path, elements)
print("Done: LLM-as-a-Judge diagram")
