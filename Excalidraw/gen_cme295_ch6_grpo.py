#!/usr/bin/env python3
"""Generate GRPO algorithm flow diagram for CME295 Chapter 6."""
import sys
sys.path.insert(0, "/Users/chajinwoo/Vaults/AutoVault/Excalidraw")
from gen_diagram import box, text, arrow, save

elements = []
eid = 0
def nid():
    global eid; eid += 1; return f"e{eid}"

# Layout
cx = 300
y_prompt = 50
y_llm = 150
y_completions = 270
y_reward = 380
y_scores = 450
y_group = 540
y_update = 650

# --- Prompt ---
elements.append(box(nid(), cx, y_prompt, 120, 40))
elements.append(text(nid(), cx, y_prompt, "Prompt", size=16))

# Arrow to LLM
elements.append(arrow(nid(), cx, y_prompt + 20, cx, y_llm - 25))

# --- LLM ---
elements.append(box(nid(), cx, y_llm, 120, 50))
elements.append(text(nid(), cx, y_llm, "LLM", size=18))

# Label: generates G completions
elements.append(text(nid(), cx + 100, y_llm, "Generates G completions", size=12))

# Arrow from LLM to completions area
elements.append(arrow(nid(), cx, y_llm + 25, cx, y_completions - 35))

# --- Completions (4 small boxes) ---
comp_labels = ["o1", "o2", "o3", "o4"]
comp_spacing = 90
comp_start_x = cx - (len(comp_labels) - 1) * comp_spacing / 2
comp_centers = []
for i, label in enumerate(comp_labels):
    bx = comp_start_x + i * comp_spacing
    comp_centers.append(bx)
    elements.append(box(nid(), bx, y_completions, 60, 36, thin=True))
    elements.append(text(nid(), bx, y_completions, label, size=14, mono=True))

# Fan-out arrows from center to each completion
for bx in comp_centers:
    elements.append(arrow(nid(), cx, y_completions - 35, bx, y_completions - 18))

# --- Reward ---
elements.append(box(nid(), cx, y_reward, 120, 40))
elements.append(text(nid(), cx, y_reward, "Reward", size=16))

# Arrows from completions to reward
for bx in comp_centers:
    elements.append(arrow(nid(), bx, y_completions + 18, cx, y_reward - 20))

# --- Scores ---
score_labels = ["R1", "R2", "R3", "R4"]
for i, label in enumerate(score_labels):
    sx = comp_start_x + i * comp_spacing
    elements.append(text(nid(), sx, y_scores, label, size=13, mono=True))

# Arrows from reward to scores
for i, sx in enumerate(comp_centers):
    elements.append(arrow(nid(), cx, y_reward + 20, sx, y_scores - 10))

# --- Group Relative Advantage ---
elements.append(box(nid(), cx, y_group, 260, 44))
elements.append(text(nid(), cx, y_group - 8, "Group Relative Advantage", size=15))
elements.append(text(nid(), cx, y_group + 12, "Compute mean/std of rewards", size=12))

# Arrows from scores to group advantage
for sx in comp_centers:
    elements.append(arrow(nid(), sx, y_scores + 10, cx, y_group - 22))

# --- Update LLM ---
elements.append(box(nid(), cx, y_update, 140, 44))
elements.append(text(nid(), cx, y_update, "Update LLM", size=16))

# Arrow from group advantage to update
elements.append(arrow(nid(), cx, y_group + 22, cx, y_update - 22))

# --- Feedback loop arrow (right side, from Update back to LLM) ---
loop_x = cx + 200
elements.append(arrow(nid(), cx + 70, y_update, loop_x, y_update))
elements.append(arrow(nid(), loop_x, y_update, loop_x, y_llm))
elements.append(arrow(nid(), loop_x, y_llm, cx + 60, y_llm))

# --- Label: No Value Model needed ---
elements.append(text(nid(), cx - 190, y_group, "No Value Model\nneeded", size=14))

out_path = "/Users/chajinwoo/Vaults/AutoVault/Excalidraw/cme295-grpo.excalidraw"
save(out_path, elements)
print("Done: GRPO diagram")
