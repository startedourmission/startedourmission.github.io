#!/usr/bin/env python3
"""Generate Excalidraw diagrams for CS229 Book chapters 6-10."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_diagram import node, box, text, conn, arrow, connect_layers, save

OUTDIR = os.path.dirname(__file__)

# ============================================================
# Chapter 6: Support Vector Machine
# ============================================================
def ch6_svm():
    els = []
    # Title
    els.append(text("t0", 400, 30, "Support Vector Machine", size=24))

    # Class 1: hollow circles (left side)
    class1_positions = [
        (120, 150), (140, 200), (100, 250), (150, 280), (130, 330),
        (170, 170), (110, 310), (160, 240)
    ]
    for i, (cx, cy) in enumerate(class1_positions):
        els.append(node(f"c1_{i}", cx, cy, r=8))

    # Class 2: filled circles (right side)
    class2_positions = [
        (580, 150), (620, 200), (650, 250), (600, 280), (630, 330),
        (570, 220), (660, 170), (610, 310)
    ]
    for i, (cx, cy) in enumerate(class2_positions):
        n = node(f"c2_{i}", cx, cy, r=8)
        n["backgroundColor"] = "#000000"
        els.append(n)

    # Decision boundary (solid line in middle)
    els.append({
        **{
            "id": "db", "type": "line", "strokeColor": "#000000", "strokeWidth": 2,
            "opacity": 100, "roughness": 0, "fillStyle": "solid",
            "backgroundColor": "transparent", "angle": 0, "seed": 100,
            "version": 1, "versionNonce": 101, "isDeleted": False,
            "boundElements": None, "updated": 1, "link": None, "locked": False
        },
        "x": 380, "y": 100, "width": 0, "height": 280,
        "points": [[0, 0], [0, 280]]
    })

    # Margin dashed lines
    for lid, lx in [("ml", 300), ("mr", 460)]:
        els.append({
            "id": lid, "type": "line", "strokeColor": "#888888", "strokeWidth": 1,
            "strokeStyle": "dashed",
            "opacity": 100, "roughness": 0, "fillStyle": "solid",
            "backgroundColor": "transparent", "angle": 0, "seed": 102,
            "version": 1, "versionNonce": 103, "isDeleted": False,
            "boundElements": None, "updated": 1, "link": None, "locked": False,
            "x": lx, "y": 100, "width": 0, "height": 280,
            "points": [[0, 0], [0, 280]]
        })

    # Margin arrows (horizontal, showing width)
    els.append(arrow("ma1", 305, 400, 375, 400))
    els.append(arrow("ma2", 455, 400, 385, 400))
    els.append(text("mt", 380, 420, "margin", size=12))

    # Labels
    els.append(text("lbl1", 130, 380, "Class -1", size=14))
    els.append(text("lbl2", 620, 380, "Class +1", size=14))

    save(os.path.join(OUTDIR, "cs229-svm.excalidraw"), els)

# ============================================================
# Chapter 7: Kernel Trick
# ============================================================
def ch7_kernel():
    els = []
    # Title
    els.append(text("t0", 400, 30, "Kernel Trick", size=24))

    # Left: Input Space box
    els.append(box("ib", 150, 230, 220, 220))
    els.append(text("il", 150, 100, "Input Space", size=16))

    # Mixed dots in input space (not linearly separable - interleaved)
    input_class1 = [(100, 200), (130, 250), (160, 180), (140, 280), (180, 230)]
    input_class2 = [(150, 210), (120, 260), (170, 270), (200, 200), (190, 250)]
    for i, (cx, cy) in enumerate(input_class1):
        els.append(node(f"i1_{i}", cx, cy, r=6))
    for i, (cx, cy) in enumerate(input_class2):
        n = node(f"i2_{i}", cx, cy, r=6)
        n["backgroundColor"] = "#000000"
        els.append(n)

    # Arrow from left to right
    els.append(arrow("ka", 280, 230, 500, 230))
    els.append(text("kl", 390, 200, "Kernel phi(x)", size=14))

    # Right: Feature Space box
    els.append(box("fb", 650, 230, 220, 220))
    els.append(text("fl", 650, 100, "Feature Space", size=16))

    # Separated dots in feature space
    feat_class1 = [(570, 180), (580, 210), (590, 240), (575, 260), (600, 195)]
    feat_class2 = [(700, 180), (720, 210), (710, 240), (730, 260), (715, 195)]
    for i, (cx, cy) in enumerate(feat_class1):
        els.append(node(f"f1_{i}", cx, cy, r=6))
    for i, (cx, cy) in enumerate(feat_class2):
        n = node(f"f2_{i}", cx, cy, r=6)
        n["backgroundColor"] = "#000000"
        els.append(n)

    # Separating line in feature space
    els.append({
        "id": "sep", "type": "line", "strokeColor": "#000000", "strokeWidth": 2,
        "opacity": 100, "roughness": 0, "fillStyle": "solid",
        "backgroundColor": "transparent", "angle": 0, "seed": 200,
        "version": 1, "versionNonce": 201, "isDeleted": False,
        "boundElements": None, "updated": 1, "link": None, "locked": False,
        "x": 650, "y": 150, "width": 0, "height": 180,
        "points": [[0, 0], [0, 180]]
    })

    save(os.path.join(OUTDIR, "cs229-kernel-trick.excalidraw"), els)

# ============================================================
# Chapter 8: Bias-Variance Tradeoff
# ============================================================
def ch8_bias_variance():
    els = []
    # Title
    els.append(text("t0", 400, 20, "Bias-Variance Tradeoff", size=24))

    # X-axis
    els.append(arrow("xa", 50, 380, 750, 380))
    els.append(text("xl", 400, 410, "Model Complexity", size=14))

    # Y-axis
    els.append(arrow("ya", 50, 380, 50, 60))

    # --- Left section: High Bias (Underfit) ---
    els.append(text("hb", 180, 70, "High Bias", size=14))
    els.append(text("hb2", 180, 88, "(Underfit)", size=12))

    # Scattered dots
    left_dots = [(100,220),(130,260),(160,200),(190,240),(220,180),(250,230)]
    for i, (cx, cy) in enumerate(left_dots):
        n = node(f"ld_{i}", cx, cy, r=5)
        n["backgroundColor"] = "#000000"
        els.append(n)

    # Straight line through dots (underfit)
    els.append({
        "id": "ul", "type": "line", "strokeColor": "#000000", "strokeWidth": 2,
        "opacity": 100, "roughness": 0, "fillStyle": "solid",
        "backgroundColor": "transparent", "angle": 0, "seed": 300,
        "version": 1, "versionNonce": 301, "isDeleted": False,
        "boundElements": None, "updated": 1, "link": None, "locked": False,
        "x": 80, "y": 250, "width": 200, "height": -30,
        "points": [[0, 0], [200, -30]]
    })

    # --- Middle section: Just Right ---
    els.append(text("jr", 400, 70, "Just Right", size=14))

    mid_dots = [(340,240),(370,200),(400,220),(430,180),(460,210),(490,190)]
    for i, (cx, cy) in enumerate(mid_dots):
        n = node(f"md_{i}", cx, cy, r=5)
        n["backgroundColor"] = "#000000"
        els.append(n)

    # Smooth curve (just right)
    els.append({
        "id": "jrl", "type": "line", "strokeColor": "#000000", "strokeWidth": 2,
        "opacity": 100, "roughness": 0, "fillStyle": "solid",
        "backgroundColor": "transparent", "angle": 0, "seed": 302,
        "version": 1, "versionNonce": 303, "isDeleted": False,
        "boundElements": None, "updated": 1, "link": None, "locked": False,
        "x": 320, "y": 250, "width": 200, "height": -60,
        "points": [[0, 0], [50, -30], [100, -40], [150, -50], [200, -60]]
    })

    # --- Right section: High Variance (Overfit) ---
    els.append(text("hv", 630, 70, "High Variance", size=14))
    els.append(text("hv2", 630, 88, "(Overfit)", size=12))

    right_dots = [(560,230),(590,180),(620,250),(650,170),(680,240),(710,190)]
    for i, (cx, cy) in enumerate(right_dots):
        n = node(f"rd_{i}", cx, cy, r=5)
        n["backgroundColor"] = "#000000"
        els.append(n)

    # Wiggly line (overfit) - passes through every dot
    els.append({
        "id": "ofl", "type": "line", "strokeColor": "#000000", "strokeWidth": 2,
        "opacity": 100, "roughness": 0, "fillStyle": "solid",
        "backgroundColor": "transparent", "angle": 0, "seed": 304,
        "version": 1, "versionNonce": 305, "isDeleted": False,
        "boundElements": None, "updated": 1, "link": None, "locked": False,
        "x": 560, "y": 230, "width": 150, "height": 0,
        "points": [[0, 0], [30, -50], [60, 20], [90, -60], [120, 10], [150, -40]]
    })

    save(os.path.join(OUTDIR, "cs229-bias-variance.excalidraw"), els)

# ============================================================
# Chapter 9: Ensemble Methods
# ============================================================
def ch9_ensemble():
    els = []
    # Title
    els.append(text("t0", 400, 30, "Ensemble Methods", size=24))

    # Three tree boxes at top
    for i, (label, cx) in enumerate([("Tree 1", 200), ("Tree 2", 400), ("Tree 3", 600)]):
        els.append(box(f"tb{i}", cx, 120, 120, 50))
        els.append(text(f"tl{i}", cx, 120, label, size=14))

    # Arrows from trees to vote box
    for i, cx in enumerate([200, 400, 600]):
        els.append(arrow(f"a1_{i}", cx, 145, 400, 220))

    # Vote / Average box
    els.append(box("vb", 400, 250, 160, 50))
    els.append(text("vl", 400, 250, "Vote / Average", size=14))

    # Arrow to final prediction
    els.append(arrow("a2", 400, 275, 400, 340))

    # Final Prediction box
    els.append(box("fb", 400, 370, 180, 50))
    els.append(text("fl", 400, 370, "Final Prediction", size=14))

    save(os.path.join(OUTDIR, "cs229-ensemble.excalidraw"), els)

# ============================================================
# Chapter 10: Neural Network
# ============================================================
def ch10_neural_network():
    els = []
    # Title
    els.append(text("t0", 400, 20, "Neural Network", size=24))

    # Input layer: 3 nodes
    input_y = [150, 250, 350]
    input_centers = [(100, y) for y in input_y]
    for i, (cx, cy) in enumerate(input_centers):
        els.append(node(f"in_{i}", cx, cy, r=18))

    # Hidden layer: 4 nodes
    hidden_y = [120, 210, 300, 390]
    hidden_centers = [(350, y) for y in hidden_y]
    for i, (cx, cy) in enumerate(hidden_centers):
        els.append(node(f"h_{i}", cx, cy, r=18))

    # Output layer: 2 nodes
    output_y = [200, 300]
    output_centers = [(600, y) for y in output_y]
    for i, (cx, cy) in enumerate(output_centers):
        els.append(node(f"o_{i}", cx, cy, r=18))

    # Connections
    els.extend(connect_layers("c1_", input_centers, hidden_centers))
    els.extend(connect_layers("c2_", hidden_centers, output_centers))

    # Labels
    els.append(text("li", 100, 420, "Input", size=14))
    els.append(text("lh", 350, 420, "Hidden", size=14))
    els.append(text("lo", 600, 420, "Output", size=14))

    save(os.path.join(OUTDIR, "cs229-neural-network.excalidraw"), els)


if __name__ == "__main__":
    ch6_svm()
    ch7_kernel()
    ch8_bias_variance()
    ch9_ensemble()
    ch10_neural_network()
    print("All diagrams generated.")
