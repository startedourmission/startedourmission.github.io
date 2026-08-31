#!/usr/bin/env python3
"""Generate CS229 Book chapters 1-10 Excalidraw diagrams using gen_diagram.py helpers."""
import sys, os, subprocess, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_diagram import (
    labeled_box, labeled_node, text, node, arrow, conn, box,
    connect_layers, save, measure_text, _font_str, _base, _next_seed,
    ARROW, NODE, BOX, BOX_THIN
)

EXCALIDRAW_DIR = "/Users/chajinwoo/Vaults/AutoVault/Excalidraw"
ASSETS_DIR = "/Users/chajinwoo/Vaults/AutoVault/raw/CS229 Book/_assets"

# --- Multi-line labeled_box helper ---
def ml_labeled_box(eid, cx, cy, label, size=14, pad_x=24, pad_y=16, thin=False):
    """labeled_box that correctly handles multi-line labels.
    Now delegates to labeled_box from gen_diagram which handles multiline properly."""
    return labeled_box(eid, cx, cy, label, size=size, pad_x=pad_x, pad_y=pad_y, thin=thin)


def line_el(eid, x1, y1, x2, y2, width=2, color="#000000"):
    """Simple line segment (no arrowhead)."""
    base = _base(eid)
    return {
        **base,
        "type": "line", "strokeColor": color, "strokeWidth": width,
        "opacity": 100, "roughness": 0, "fillStyle": "solid",
        "backgroundColor": "transparent",
        "x": x1, "y": y1, "width": x2 - x1, "height": y2 - y1,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "startArrowhead": None, "endArrowhead": None,
    }


def dashed_line(eid, x1, y1, x2, y2, width=1, color="#000000"):
    """Dashed line segment."""
    el = line_el(eid, x1, y1, x2, y2, width=width, color=color)
    el["strokeStyle"] = "dashed"
    return el


def filled_circle(eid, cx, cy, r=8):
    """Filled black circle."""
    base = _base(eid)
    return {
        **base, **NODE,
        "x": cx - r, "y": cy - r, "width": r * 2, "height": r * 2,
        "backgroundColor": "#000000", "fillStyle": "solid"
    }


# ============================================================
# Ch1: Machine Learning Categories
# ============================================================
def ch1():
    els = []
    els.append(text("t1", 350, 30, "Machine Learning Categories", size=20))
    els.extend(ml_labeled_box("sup", 120, 100, "Supervised\nx -> y mapping"))
    els.extend(ml_labeled_box("unsup", 350, 100, "Unsupervised\nFind structure"))
    els.extend(ml_labeled_box("rl", 580, 100, "Reinforcement\nReward signal"))
    return els


# ============================================================
# Ch2: Gradient Descent
# ============================================================
def ch2():
    els = []
    els.append(text("t2", 300, 20, "Gradient Descent", size=20))

    # Approximate cost curve using line segments
    curve_pts = [
        (80, 100), (120, 180), (160, 230), (200, 250),
        (240, 240), (280, 210), (320, 190), (360, 180),
        (400, 185), (440, 200), (480, 230), (520, 270)
    ]
    for i in range(len(curve_pts) - 1):
        x1, y1 = curve_pts[i]
        x2, y2 = curve_pts[i + 1]
        els.append(line_el(f"c{i}", x1, y1, x2, y2))

    # Dot on the curve (at a high point)
    els.append(filled_circle("dot", 160, 230, r=6))

    # Arrow pointing downhill from the dot
    els.append(arrow("step", 170, 225, 310, 190))
    els.append(text("steplbl", 260, 195, "Step", size=12))

    # Axis labels
    els.append(text("ylbl", 40, 170, "Cost J", size=13))
    els.append(text("xlbl", 300, 290, "theta", size=13))

    return els


# ============================================================
# Ch3: Logistic Regression
# ============================================================
def ch3():
    els = []
    els.append(text("t3", 350, 30, "Logistic Regression", size=20))
    els.extend(ml_labeled_box("inp", 100, 120, "Input x"))
    els.extend(ml_labeled_box("sig", 300, 120, "Sigmoid"))
    els.extend(ml_labeled_box("out", 530, 120, "P(y=1|x)"))
    els.append(arrow("a1", 170, 120, 240, 120))
    els.append(arrow("a2", 360, 120, 460, 120))
    return els


# ============================================================
# Ch4: Generalized Linear Models
# ============================================================
def ch4():
    els = []
    els.append(text("t4", 350, 20, "Generalized Linear Models", size=20))
    els.extend(ml_labeled_box("exp", 350, 90, "Exponential Family"))
    els.extend(ml_labeled_box("lr", 120, 240, "Linear Regression\n(Gaussian)"))
    els.extend(ml_labeled_box("log", 350, 240, "Logistic Regression\n(Bernoulli)"))
    els.extend(ml_labeled_box("sm", 580, 240, "Softmax Regression\n(Multinomial)"))
    els.append(arrow("a1", 280, 115, 180, 210))
    els.append(arrow("a2", 350, 115, 350, 210))
    els.append(arrow("a3", 420, 115, 520, 210))
    return els


# ============================================================
# Ch5: Generative vs Discriminative
# ============================================================
def ch5():
    els = []
    els.append(text("t5", 350, 20, "Generative vs Discriminative", size=20))

    # Divider
    els.append(dashed_line("div", 350, 50, 350, 310))

    # Left column - Generative
    els.extend(ml_labeled_box("g1", 170, 90, "Generative"))
    els.extend(ml_labeled_box("g2", 170, 170, "Models P(x|y)"))
    els.extend(ml_labeled_box("g3", 170, 260, "GDA, Naive Bayes"))
    els.append(arrow("ga1", 170, 115, 170, 145))
    els.append(arrow("ga2", 170, 195, 170, 230))

    # Right column - Discriminative
    els.extend(ml_labeled_box("d1", 530, 90, "Discriminative"))
    els.extend(ml_labeled_box("d2", 530, 170, "Models P(y|x)"))
    els.extend(ml_labeled_box("d3", 530, 260, "Logistic Regression"))
    els.append(arrow("da1", 530, 115, 530, 145))
    els.append(arrow("da2", 530, 195, 530, 230))

    return els


# ============================================================
# Ch6: Support Vector Machine
# ============================================================
def ch6():
    els = []
    els.append(text("t6", 300, 20, "Support Vector Machine", size=20))

    # Class -1 (empty circles on left)
    left_pts = [(100, 100), (130, 150), (80, 180), (140, 210), (110, 250)]
    for i, (x, y) in enumerate(left_pts):
        els.append(node(f"ln{i}", x, y, r=8))

    # Class +1 (filled circles on right)
    right_pts = [(360, 110), (390, 160), (340, 190), (400, 220), (370, 260)]
    for i, (x, y) in enumerate(right_pts):
        els.append(filled_circle(f"rn{i}", x, y, r=8))

    # Decision boundary (vertical line)
    els.append(line_el("db", 240, 70, 240, 290, width=2))

    # Margin dashed lines
    els.append(dashed_line("ml", 190, 70, 190, 290))
    els.append(dashed_line("mr", 290, 70, 290, 290))

    # Margin label with arrows
    els.append(text("mlbl", 240, 310, "margin", size=12))
    els.append(arrow("ma1", 215, 320, 195, 320))
    els.append(arrow("ma2", 265, 320, 285, 320))

    # Class labels
    els.append(text("c1lbl", 110, 285, "Class -1", size=11))
    els.append(text("c2lbl", 370, 285, "Class +1", size=11))

    return els


# ============================================================
# Ch7: Kernel Trick
# ============================================================
def ch7():
    els = []
    els.append(text("t7", 350, 30, "Kernel Trick", size=20))
    els.extend(ml_labeled_box("inp", 140, 130, "Input Space\n(not separable)"))
    els.extend(ml_labeled_box("feat", 520, 130, "Feature Space\n(separable)"))
    els.append(arrow("a1", 240, 130, 420, 130))
    els.append(text("phi", 330, 110, "phi(x)", size=13))
    return els


# ============================================================
# Ch8: Bias-Variance Tradeoff
# ============================================================
def ch8():
    els = []
    els.append(text("t8", 350, 30, "Bias-Variance Tradeoff", size=20))
    els.extend(ml_labeled_box("hb", 120, 120, "High Bias\n(Underfit)"))
    els.extend(ml_labeled_box("jr", 350, 120, "Just Right"))
    els.extend(ml_labeled_box("hv", 580, 120, "High Variance\n(Overfit)"))
    els.append(arrow("a1", 210, 120, 290, 120))
    els.append(arrow("a2", 410, 120, 490, 120))
    return els


# ============================================================
# Ch9: Ensemble Methods
# ============================================================
def ch9():
    els = []
    els.append(text("t9", 350, 20, "Ensemble Methods", size=20))
    els.extend(ml_labeled_box("t1", 150, 90, "Tree 1"))
    els.extend(ml_labeled_box("t2", 350, 90, "Tree 2"))
    els.extend(ml_labeled_box("t3", 550, 90, "Tree 3"))
    els.extend(ml_labeled_box("vote", 350, 210, "Vote / Average"))
    els.extend(ml_labeled_box("pred", 350, 310, "Prediction"))
    els.append(arrow("a1", 150, 115, 300, 190))
    els.append(arrow("a2", 350, 115, 350, 190))
    els.append(arrow("a3", 550, 115, 400, 190))
    els.append(arrow("a4", 350, 235, 350, 285))
    return els


# ============================================================
# Ch10: Neural Network
# ============================================================
def ch10():
    els = []
    els.append(text("t10", 300, 20, "Neural Network", size=20))

    # Input layer: 3 nodes
    inp_y = [100, 170, 240]
    inp_centers = [(100, y) for y in inp_y]
    for i, (x, y) in enumerate(inp_centers):
        els.append(node(f"i{i}", x, y, r=18))

    # Hidden layer: 4 nodes
    hid_y = [80, 147, 213, 280]
    hid_centers = [(300, y) for y in hid_y]
    for i, (x, y) in enumerate(hid_centers):
        els.append(node(f"h{i}", x, y, r=18))

    # Output layer: 2 nodes
    out_y = [140, 210]
    out_centers = [(500, y) for y in out_y]
    for i, (x, y) in enumerate(out_centers):
        els.append(node(f"o{i}", x, y, r=18))

    # Connections
    els.extend(connect_layers("ih", inp_centers, hid_centers))
    els.extend(connect_layers("ho", hid_centers, out_centers))

    # Layer labels
    els.append(text("il", 100, 280, "Input", size=12))
    els.append(text("hl", 300, 320, "Hidden", size=12))
    els.append(text("ol", 500, 250, "Output", size=12))

    return els


# ============================================================
# Build all and export
# ============================================================
diagrams = [
    ("cs229-ml-overview", "1-cs229-ml-overview.png", ch1),
    ("cs229-gradient-descent", "2-cs229-gradient-descent.png", ch2),
    ("cs229-logistic-regression", "3-cs229-logistic-regression.png", ch3),
    ("cs229-glm", "4-cs229-glm.png", ch4),
    ("cs229-generative-discriminative", "5-cs229-generative-discriminative.png", ch5),
    ("cs229-svm", "6-cs229-svm.png", ch6),
    ("cs229-kernel-trick", "7-cs229-kernel-trick.png", ch7),
    ("cs229-bias-variance", "8-cs229-bias-variance.png", ch8),
    ("cs229-ensemble", "9-cs229-ensemble.png", ch9),
    ("cs229-neural-network", "10-cs229-neural-network.png", ch10),
]

for name, png_name, fn in diagrams:
    exc_path = os.path.join(EXCALIDRAW_DIR, f"{name}.excalidraw")
    png_path = os.path.join(ASSETS_DIR, png_name)
    els = fn()
    save(exc_path, els)
    # Export to PNG
    result = subprocess.run(
        ["npx", "@swiftlysingh/excalidraw-cli", "convert", exc_path, "--format", "png", "-o", png_path, "--scale", "2"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        print(f"Exported: {png_path}")
    else:
        print(f"Export FAILED for {name}: {result.stderr}")

print("\nDone! All 10 diagrams generated.")
