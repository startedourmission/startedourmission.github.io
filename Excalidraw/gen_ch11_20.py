#!/usr/bin/env python3
"""Generate Excalidraw diagrams for CS229 chapters 11-20."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_diagram import (
    node, box, text, arrow, conn, labeled_box, labeled_node,
    connect_layers, save
)

OUTDIR = os.path.dirname(__file__)

def ch11_backprop():
    """Ch11: Backpropagation - 3-layer network (3-4-2)."""
    els = []
    els.append(text("title", 400, 30, "Backpropagation", size=20))

    # Layer positions
    layer1_x, layer2_x, layer3_x = 150, 400, 650
    # Layer 1: 3 nodes
    l1 = [(layer1_x, 120), (layer1_x, 200), (layer1_x, 280)]
    # Layer 2: 4 nodes
    l2 = [(layer2_x, 90), (layer2_x, 160), (layer2_x, 230), (layer2_x, 300)]
    # Layer 3: 2 nodes
    l3 = [(layer3_x, 160), (layer3_x, 240)]

    for i, (cx, cy) in enumerate(l1):
        els.append(node(f"l1n{i}", cx, cy, r=18))
    for i, (cx, cy) in enumerate(l2):
        els.append(node(f"l2n{i}", cx, cy, r=18))
    for i, (cx, cy) in enumerate(l3):
        els.append(node(f"l3n{i}", cx, cy, r=18))

    # Connections
    els.extend(connect_layers("c12_", l1, l2))
    els.extend(connect_layers("c23_", l2, l3))

    # Layer labels
    els.append(text("ll1", layer1_x, 340, "Input", size=12))
    els.append(text("ll2", layer2_x, 350, "Hidden", size=12))
    els.append(text("ll3", layer3_x, 300, "Output", size=12))

    # Forward arrow on top
    els.append(arrow("fwd", 180, 55, 620, 55))
    els.append(text("fwd_lbl", 400, 45, "Forward Pass", size=12))

    # Backward arrow on bottom
    els.append(arrow("bwd", 620, 380, 180, 380))
    els.append(text("bwd_lbl", 400, 370, "Backward Pass (gradients)", size=12))

    save(os.path.join(OUTDIR, "cs229-backprop.excalidraw"), els)


def ch12_debugging():
    """Ch12: ML Debugging Strategy."""
    els = []
    els.append(text("title", 400, 30, "ML Debugging Strategy", size=20))

    # Top: High Error
    els.extend(labeled_box("top", 400, 100, "High Error"))

    # Left branch
    els.append(arrow("a_left", 340, 125, 220, 190))
    els.extend(labeled_box("bias", 200, 220, "High Bias?"))
    els.append(arrow("a_bias", 200, 248, 200, 290))
    els.extend(labeled_box("fix_bias", 200, 330, "More features\nBigger model"))

    # Right branch
    els.append(arrow("a_right", 460, 125, 580, 190))
    els.extend(labeled_box("var", 600, 220, "High Variance?"))
    els.append(arrow("a_var", 600, 248, 600, 290))
    els.extend(labeled_box("fix_var", 600, 330, "More data\nRegularize"))

    save(os.path.join(OUTDIR, "cs229-debugging.excalidraw"), els)


def ch13_em():
    """Ch13: EM Algorithm."""
    els = []
    els.append(text("title", 400, 30, "EM Algorithm", size=20))

    # E-step box
    els.extend(labeled_box("estep", 220, 180, "E-step\nEstimate assignments"))
    # M-step box
    els.extend(labeled_box("mstep", 580, 180, "M-step\nUpdate parameters"))

    # Forward arrow E -> M
    els.append(arrow("em_fwd", 330, 170, 470, 170))

    # Backward arrow M -> E (loop back, below)
    els.append(arrow("em_back", 470, 200, 330, 200))
    els.append(text("loop_lbl", 400, 220, "Repeat until convergence", size=11))

    # Initialize arrow entering E-step
    els.append(arrow("init", 80, 180, 130, 180))
    els.append(text("init_lbl", 80, 155, "Initialize", size=12))

    save(os.path.join(OUTDIR, "cs229-em-algorithm.excalidraw"), els)


def ch14_factor():
    """Ch14: Factor Analysis."""
    els = []
    els.append(text("title", 400, 30, "Factor Analysis", size=20))

    els.extend(labeled_box("latent", 180, 180, "Latent z\n(low-dim)"))
    els.extend(labeled_box("observed", 620, 180, "Observed x\n(high-dim)"))
    els.append(arrow("fa_arr", 280, 180, 520, 180))
    els.append(text("fa_lbl", 400, 155, "W*z + mu", size=13))

    save(os.path.join(OUTDIR, "cs229-factor-analysis.excalidraw"), els)


def ch15_pca():
    """Ch15: PCA - scatter with principal component arrows."""
    els = []
    els.append(text("title", 400, 30, "Principal Component Analysis", size=20))

    import random
    random.seed(42)
    cx, cy = 400, 220
    # Scatter dots
    for i in range(25):
        dx = random.gauss(0, 80)
        dy = random.gauss(0, 30) + dx * 0.3
        els.append(node(f"dot{i}", cx + dx, cy + dy, r=4))

    # PC1 arrow (long, diagonal)
    els.append(arrow("pc1", cx - 140, cy + 42, cx + 140, cy - 42))
    els.append(text("pc1_lbl", cx + 155, cy - 55, "PC1 (max variance)", size=12))

    # PC2 arrow (short, perpendicular)
    els.append(arrow("pc2", cx + 20, cy + 60, cx - 20, cy - 60))
    els.append(text("pc2_lbl", cx - 60, cy - 75, "PC2", size=12))

    save(os.path.join(OUTDIR, "cs229-pca.excalidraw"), els)


def ch16_ica():
    """Ch16: ICA."""
    els = []
    els.append(text("title", 400, 30, "Independent Component Analysis", size=20))

    els.extend(labeled_box("mixed", 180, 180, "Mixed Signals"))
    els.extend(labeled_box("indep", 620, 180, "Independent Sources"))
    els.append(arrow("ica_arr", 290, 180, 510, 180))
    els.append(text("ica_lbl", 400, 155, "Unmixing W", size=13))

    save(os.path.join(OUTDIR, "cs229-ica.excalidraw"), els)


def ch17_mdp():
    """Ch17: MDP - 3 states in triangle with actions/rewards."""
    els = []
    els.append(text("title", 400, 30, "Markov Decision Process", size=20))

    # Triangle of states
    s1 = (400, 100)
    s2 = (250, 280)
    s3 = (550, 280)

    els.extend(labeled_node("s1", *s1, "S1", size=14, r=28))
    els.extend(labeled_node("s2", *s2, "S2", size=14, r=28))
    els.extend(labeled_node("s3", *s3, "S3", size=14, r=28))

    # Arrows S1->S2
    els.append(arrow("a12", 375, 125, 275, 255))
    els.append(text("a12_lbl", 300, 175, "a1", size=12))
    els.append(text("r12_lbl", 310, 192, "r=+1", size=11))

    # Arrows S2->S3
    els.append(arrow("a23", 280, 285, 520, 285))
    els.append(text("a23_lbl", 400, 300, "a2", size=12))
    els.append(text("r23_lbl", 400, 317, "r=-1", size=11))

    # Arrows S3->S1
    els.append(arrow("a31", 530, 258, 425, 128))
    els.append(text("a31_lbl", 495, 178, "a1", size=12))
    els.append(text("r31_lbl", 505, 195, "r=+2", size=11))

    save(os.path.join(OUTDIR, "cs229-mdp.excalidraw"), els)


def ch18_value_approx():
    """Ch18: Continuous State MDP."""
    els = []
    els.append(text("title", 400, 30, "Continuous State MDP", size=20))

    els.extend(labeled_box("disc", 180, 180, "Discrete States\n(grid)"))
    els.extend(labeled_box("cont", 620, 180, "Continuous\nValue Function"))
    els.append(arrow("va_arr", 290, 180, 510, 180))
    els.append(text("va_lbl", 400, 155, "Approximate", size=13))

    save(os.path.join(OUTDIR, "cs229-value-approximation.excalidraw"), els)


def ch19_lqr():
    """Ch19: LQR - Circular flow: State -> Controller -> Action -> System -> State."""
    els = []
    els.append(text("title", 400, 30, "Linear Quadratic Regulator", size=20))

    # Square layout for 4 boxes
    top_y, bot_y = 130, 280
    left_x, right_x = 200, 600

    els.extend(labeled_box("state", left_x, top_y, "State"))
    els.extend(labeled_box("ctrl", right_x, top_y, "Controller"))
    els.extend(labeled_box("action", right_x, bot_y, "Action"))
    els.extend(labeled_box("sys", left_x, bot_y, "System"))

    # Arrows: State -> Controller (top)
    els.append(arrow("a1", 270, top_y, 530, top_y))
    # Controller -> Action (right)
    els.append(arrow("a2", right_x, 158, right_x, 252))
    # Action -> System (bottom, right to left)
    els.append(arrow("a3", 530, bot_y, 270, bot_y))
    # System -> State (left, bottom to top)
    els.append(arrow("a4", left_x, 252, left_x, 158))

    save(os.path.join(OUTDIR, "cs229-lqr.excalidraw"), els)


def ch20_policy_search():
    """Ch20: Policy Search - Circular flow."""
    els = []
    els.append(text("title", 400, 30, "Policy Search", size=20))

    top_y, bot_y = 130, 280
    left_x, right_x = 200, 600

    els.extend(labeled_box("policy", left_x, top_y, "Policy"))
    els.extend(labeled_box("env", right_x, top_y, "Environment"))
    els.extend(labeled_box("rew", right_x, bot_y, "Rewards"))
    els.extend(labeled_box("upd", left_x, bot_y, "Update"))

    # Policy -> Environment (top)
    els.append(arrow("a1", 270, top_y, 530, top_y))
    # Environment -> Rewards (right)
    els.append(arrow("a2", right_x, 158, right_x, 252))
    # Rewards -> Update (bottom, right to left)
    els.append(arrow("a3", 530, bot_y, 270, bot_y))
    # Update -> Policy (left, bottom to top)
    els.append(arrow("a4", left_x, 252, left_x, 158))

    save(os.path.join(OUTDIR, "cs229-policy-search.excalidraw"), els)


if __name__ == "__main__":
    ch11_backprop()
    ch12_debugging()
    ch13_em()
    ch14_factor()
    ch15_pca()
    ch16_ica()
    ch17_mdp()
    ch18_value_approx()
    ch19_lqr()
    ch20_policy_search()
    print("All 10 diagrams generated.")
