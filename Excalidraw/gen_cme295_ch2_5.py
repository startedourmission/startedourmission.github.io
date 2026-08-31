#!/usr/bin/env python3
"""Generate CME295 chapter 2-5 diagrams."""
import sys
sys.path.insert(0, "/Users/chajinwoo/Vaults/AutoVault/Excalidraw")
from gen_diagram import box, text, arrow, conn, save

BASE = "/Users/chajinwoo/Vaults/AutoVault/Excalidraw"

eid = 0
def nid():
    global eid; eid += 1; return f"e{eid}"

# ============================================================
# Chapter 2: Position Embeddings Comparison (LR flow)
# ============================================================
def gen_ch2():
    global eid; eid = 0
    els = []

    # Title
    els.append(text(nid(), 350, 30, "Position Embedding Comparison", size=20))

    # Three boxes in a row
    bw, bh = 140, 44
    y_box = 100
    xs = [120, 350, 580]
    labels = ["Sinusoidal", "ALiBi", "RoPE"]
    subs = ["Fixed, absolute", "Linear bias, no params", "Rotation, relative"]

    for i, (cx, lab, sub) in enumerate(zip(xs, labels, subs)):
        els.append(box(nid(), cx, y_box, bw, bh))
        els.append(text(nid(), cx, y_box, lab, size=16))
        els.append(text(nid(), cx, y_box + 40, sub, size=12))

    # Progression arrows between boxes
    for i in range(len(xs) - 1):
        els.append(arrow(nid(), xs[i] + bw/2 + 6, y_box, xs[i+1] - bw/2 - 6, y_box))

    # Timeline label
    els.append(text(nid(), 350, y_box + 75, "Evolution of position encoding methods", size=12))
    els.append(arrow(nid(), 140, y_box + 90, 580, y_box + 90))

    save(f"{BASE}/cme295-position-embeddings.excalidraw", els, auto_resolve=False)
    print("Done: ch2 position embeddings")


# ============================================================
# Chapter 3: Mixture of Experts Architecture
# ============================================================
def gen_ch3():
    global eid; eid = 0
    els = []

    # Title
    els.append(text(nid(), 380, 25, "Mixture of Experts", size=20))

    # Input token
    x_in = 60
    y_mid = 160
    els.append(box(nid(), x_in, y_mid, 100, 40))
    els.append(text(nid(), x_in, y_mid, "Input Token", size=14))

    # Gate/Router
    x_gate = 240
    els.append(box(nid(), x_gate, y_mid, 110, 44))
    els.append(text(nid(), x_gate, y_mid, "Gate / Router", size=14))

    # Arrow input -> gate
    els.append(arrow(nid(), x_in + 50 + 6, y_mid, x_gate - 55 - 6, y_mid))

    # Experts
    x_exp = 440
    expert_labels = ["E1", "E2", "E3", "E4"]
    exp_spacing = 60
    n_exp = len(expert_labels)
    exp_ys = [y_mid + (i - (n_exp - 1) / 2) * exp_spacing for i in range(n_exp)]
    selected = {0, 2}  # E1 and E3 selected

    for i, (lab, ey) in enumerate(zip(expert_labels, exp_ys)):
        sw = 2 if i in selected else 1
        el = box(nid(), x_exp, ey, 80, 36, thin=(i not in selected))
        if i in selected:
            el["strokeWidth"] = 3
        els.append(el)
        els.append(text(nid(), x_exp, ey, lab, size=14))

    # Connections gate -> experts
    for i, ey in enumerate(exp_ys):
        if i in selected:
            a = arrow(nid(), x_gate + 55 + 6, y_mid, x_exp - 40 - 6, ey)
            a["strokeWidth"] = 2
            a["strokeColor"] = "#000000"
            els.append(a)
        else:
            c = conn(nid(), x_gate + 55 + 6, y_mid, x_exp - 40 - 6, ey)
            els.append(c)

    # Output
    x_out = 620
    els.append(box(nid(), x_out, y_mid, 80, 40))
    els.append(text(nid(), x_out, y_mid, "Output", size=14))

    # Selected experts -> output
    for i, ey in enumerate(exp_ys):
        if i in selected:
            els.append(arrow(nid(), x_exp + 40 + 6, ey, x_out - 40 - 6, y_mid))

    # Label: "Top-k selection"
    els.append(text(nid(), x_gate, y_mid + 38, "Top-k selection", size=11))

    save(f"{BASE}/cme295-moe-architecture.excalidraw", els, auto_resolve=False)
    print("Done: ch3 MoE architecture")


# ============================================================
# Chapter 4: Training Pipeline (top to bottom)
# ============================================================
def gen_ch4():
    global eid; eid = 0
    els = []

    cx = 250
    bw, bh = 280, 44
    y_positions = [60, 180, 300]
    labels = [
        "Pre-training (next token prediction)",
        "SFT (instruction tuning)",
        "LoRA / QLoRA (parameter-efficient)",
    ]
    data_labels = [
        "Trillions of tokens",
        "~100K examples",
        "~10K examples",
    ]

    # Title
    els.append(text(nid(), cx, 15, "LLM Training Pipeline", size=20))

    for i, (y, lab, dlab) in enumerate(zip(y_positions, labels, data_labels)):
        els.append(box(nid(), cx, y, bw, bh))
        els.append(text(nid(), cx, y, lab, size=14))
        # Data scale label on the right
        els.append(text(nid(), cx + bw/2 + 80, y, dlab, size=12))

    # Arrows between stages
    for i in range(len(y_positions) - 1):
        els.append(arrow(nid(), cx, y_positions[i] + bh/2 + 4, cx, y_positions[i+1] - bh/2 - 4))

    # Side annotation: data scale shrinks
    x_side = cx + bw/2 + 80
    els.append(arrow(nid(), x_side + 50, y_positions[0] + 10, x_side + 50, y_positions[-1] - 10))
    els.append(text(nid(), x_side + 80, (y_positions[0] + y_positions[-1]) / 2, "Data scale", size=11))

    save(f"{BASE}/cme295-training-pipeline.excalidraw", els, auto_resolve=False)
    print("Done: ch4 training pipeline")


# ============================================================
# Chapter 5: RLHF Pipeline
# ============================================================
def gen_ch5():
    global eid; eid = 0
    els = []

    # Title
    els.append(text(nid(), 320, 20, "RLHF Pipeline", size=20))

    bw, bh = 140, 42

    # Prompt box (top-left)
    px, py = 100, 90
    els.append(box(nid(), px, py, 100, bh))
    els.append(text(nid(), px, py, "Prompt", size=14))

    # LLM (Policy) box
    lx, ly = 300, 90
    els.append(box(nid(), lx, ly, bw, bh))
    els.append(text(nid(), lx, ly, "LLM (Policy)", size=14))

    # Arrow Prompt -> LLM
    els.append(arrow(nid(), px + 50 + 6, py, lx - bw/2 - 6, ly))

    # Response box
    rx, ry = 510, 90
    els.append(box(nid(), rx, ry, 110, bh))
    els.append(text(nid(), rx, ry, "Response", size=14))

    # Arrow LLM -> Response
    els.append(arrow(nid(), lx + bw/2 + 6, ly, rx - 55 - 6, ry))

    # Reward Model box (below response)
    rmx, rmy = 510, 220
    els.append(box(nid(), rmx, rmy, bw, bh))
    els.append(text(nid(), rmx, rmy, "Reward Model", size=14))

    # Arrow Response -> Reward Model
    els.append(arrow(nid(), rx, ry + bh/2 + 4, rmx, rmy - bh/2 - 4))

    # Score box
    sx, sy = 300, 220
    els.append(box(nid(), sx, sy, 80, bh))
    els.append(text(nid(), sx, sy, "Score", size=14))

    # Arrow Reward Model -> Score
    els.append(arrow(nid(), rmx - bw/2 - 6, rmy, sx + 40 + 6, sy))

    # Arrow Score -> LLM (PPO update feedback)
    a = arrow(nid(), sx, sy - bh/2 - 4, lx, ly + bh/2 + 4)
    els.append(a)
    # PPO update label next to feedback arrow
    els.append(text(nid(), sx - 70, (sy + ly) / 2 + 5, "PPO update", size=12))

    # Human Preferences -> Reward Model (from the left side)
    hx, hy = 510, 330
    els.append(box(nid(), hx, hy, 160, bh))
    els.append(text(nid(), hx, hy, "Human Preferences", size=13))
    els.append(arrow(nid(), hx, hy - bh/2 - 4, rmx, rmy + bh/2 + 4))
    els.append(text(nid(), hx + 95, (hy + rmy) / 2, "trains", size=11))

    save(f"{BASE}/cme295-rlhf-pipeline.excalidraw", els, auto_resolve=False)
    print("Done: ch5 RLHF pipeline")


if __name__ == "__main__":
    gen_ch2()
    gen_ch3()
    gen_ch4()
    gen_ch5()
    print("\nAll 4 diagrams generated.")
