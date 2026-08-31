#!/usr/bin/env python3
"""Generate 6 Excalidraw diagrams for Hinton blog posts."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_diagram import (labeled_box, labeled_node, node, text, arrow, conn,
                         connect_layers, save)

SAVE_DIR = os.path.dirname(__file__)

# ============================================================
# 1. Helmholtz Machine
# ============================================================
def helmholtz():
    els = []
    # Title
    els.append(text("t", 300, 20, "Helmholtz Machine", size=20))

    # Left column: Recognition (bottom-up)
    els.append(text("rl", 130, 60, "Recognition (bottom-up)", size=14))
    ly = [280, 200, 120]  # bottom to top y positions
    labels = ["Data (visible)", "Hidden 1", "Hidden 2"]
    centers_left = []
    for i, (y, lab) in enumerate(zip(ly, labels)):
        els.extend(labeled_box(f"rb{i}", 130, y, lab))
        centers_left.append((130, y))

    # Upward arrows for recognition
    for i in range(len(ly)-1):
        els.append(arrow(f"ra{i}", 130, ly[i]-20, 130, ly[i+1]+20))

    # Right column: Generation (top-down)
    els.append(text("gl", 470, 60, "Generation (top-down)", size=14))
    labels_r = ["Hidden 2", "Hidden 1", "Reconstruction"]
    centers_right = []
    for i, (y, lab) in enumerate(zip([120, 200, 280], labels_r)):
        els.extend(labeled_box(f"gb{i}", 470, y, lab))
        centers_right.append((470, y))

    # Downward arrows for generation
    for i in range(len(ly)-1):
        els.append(arrow(f"ga{i}", 470, [120,200,280][i]+20, 470, [120,200,280][i+1]-20))

    save(os.path.join(SAVE_DIR, "hinton-helmholtz.excalidraw"), els)

# ============================================================
# 2. Contrastive Divergence
# ============================================================
def contrastive_divergence():
    els = []
    els.append(text("t", 350, 30, "Contrastive Divergence", size=20))

    boxes = ["Data", "Hidden\nSample", "Reconstruction", "Compare"]
    xs = [100, 270, 440, 610]
    y = 120
    for i, (lab, x) in enumerate(zip(boxes, xs)):
        els.extend(labeled_box(f"b{i}", x, y, lab))

    # Forward arrows
    for i in range(3):
        els.append(arrow(f"a{i}", xs[i]+60, y, xs[i+1]-60, y))

    # Feedback arrow: Compare -> back to top labeled "Update Weights"
    # Curved path: right side of Compare, up, then left back to Data
    els.append(arrow(f"fb1", 610, y+30, 610, y+70))
    els.append(arrow(f"fb2", 610, y+70, 100, y+70))
    els.append(arrow(f"fb3", 100, y+70, 100, y+30))
    els.append(text("fb_t", 350, y+80, "Update Weights", size=12))

    save(os.path.join(SAVE_DIR, "hinton-cd.excalidraw"), els)

# ============================================================
# 3. Deep Belief Nets Pretraining
# ============================================================
def deep_belief_nets():
    els = []
    els.append(text("t", 350, 30, "Deep Belief Nets Pretraining", size=20))

    stages = ["Stage 1\nRBM Layer 1-2", "Stage 2\nRBM Layer 2-3", "Stage 3\nFine-tune All"]
    xs = [120, 350, 580]
    y = 130
    for i, (lab, x) in enumerate(zip(stages, xs)):
        els.extend(labeled_box(f"s{i}", x, y, lab))

    # Arrows between stages
    els.append(arrow("a01", 200, y, 270, y))
    els.append(arrow("a12", 430, y, 500, y))

    save(os.path.join(SAVE_DIR, "hinton-dbn.excalidraw"), els)

# ============================================================
# 4. Deep Autoencoder
# ============================================================
def autoencoder():
    els = []
    els.append(text("t", 300, 10, "Deep Autoencoder", size=20))

    labels = ["Input (784)", "1000", "500", "250", "Code (30)", "250", "500", "1000", "Output (784)"]
    widths = [140, 120, 100, 90, 80, 90, 100, 120, 140]
    y_start = 60
    y_step = 50
    cx = 300
    ys = [y_start + i * y_step for i in range(9)]

    for i, (lab, w, y) in enumerate(zip(labels, widths, ys)):
        els.extend(labeled_box(f"ae{i}", cx, y, lab, pad_x=max(10, (w-60)//2)))

    # Arrows between layers
    for i in range(8):
        els.append(arrow(f"aa{i}", cx, ys[i]+18, cx, ys[i+1]-18))

    # Encoder/Decoder labels
    els.append(text("enc", 200, 170, "Encoder", size=12))
    els.append(text("dec", 200, 350, "Decoder", size=12))

    save(os.path.join(SAVE_DIR, "hinton-autoencoder.excalidraw"), els)

# ============================================================
# 5. t-SNE Visualization
# ============================================================
def tsne():
    els = []
    els.append(text("t", 300, 20, "t-SNE Visualization", size=20))

    # Left box: high-dim data
    els.extend(labeled_box("hd", 120, 140, "High-dim Data\n(1000-D)"))

    # Arrow labeled t-SNE
    els.append(arrow("ar", 210, 140, 330, 140))
    els.append(text("al", 270, 115, "t-SNE", size=14))

    # Right box: 2D Map (larger)
    els.extend(labeled_box("ld", 440, 100, "2D Map", pad_x=60, pad_y=50))

    # Scattered dots inside the right box area
    import random
    random.seed(42)
    for i in range(15):
        dx = random.randint(-45, 45)
        dy = random.randint(-25, 35)
        els.append(node(f"dot{i}", 440+dx, 115+dy, r=4))

    save(os.path.join(SAVE_DIR, "hinton-tsne.excalidraw"), els)

# ============================================================
# 6. ReLU Activation
# ============================================================
def relu():
    els = []
    els.append(text("t", 300, 20, "ReLU Activation", size=20))

    # Left: Sigmoid box
    els.extend(labeled_box("sig", 130, 120, "Sigmoid\nSaturates"))

    # Right: ReLU box
    els.extend(labeled_box("rel", 430, 120, "ReLU\nmax(0,x)"))

    # Arrow between with "Replace" label
    els.append(arrow("ar", 210, 120, 350, 120))
    els.append(text("arl", 280, 95, "Replace", size=12))

    # Below: benefit box
    els.extend(labeled_box("ben", 280, 230, "Faster Training\nNo Vanishing Gradient"))

    save(os.path.join(SAVE_DIR, "hinton-relu.excalidraw"), els)

# ============================================================
if __name__ == "__main__":
    helmholtz()
    contrastive_divergence()
    deep_belief_nets()
    autoencoder()
    tsne()
    relu()
    print("All 6 diagrams generated.")
