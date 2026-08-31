#!/usr/bin/env python3
"""Generate Excalidraw diagrams for CS229 Book chapters 16-20."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_diagram import node, box, text, conn, arrow, save

OUTDIR = os.path.dirname(__file__)

# ============================================================
# Ch16: ICA concept
# ============================================================
def ch16_ica():
    els = []
    # Title
    els.append(text("title", 400, 30, "Independent Component Analysis", size=20))

    # Left box: "Mixed Signals"
    els.append(box("mixed_box", 150, 160, 180, 120))
    els.append(text("mixed_lbl", 150, 100, "Mixed Signals", size=14))

    # Wavy lines inside mixed box (overlapping) - represented as short line segments
    # Line 1 (zigzag)
    for i, (dx, dy) in enumerate([(0,0),(20,-15),(40,10),(60,-10),(80,15),(100,0),(120,-12),(140,5)]):
        if i > 0:
            prev = (70 + [(0,0),(20,-15),(40,10),(60,-10),(80,15),(100,0),(120,-12),(140,5)][i-1][0],
                     145 + [(0,0),(20,-15),(40,10),(60,-10),(80,15),(100,0),(120,-12),(140,5)][i-1][1])
            cur = (70 + dx, 145 + dy)
            els.append(conn(f"w1_{i}", prev[0], prev[1], cur[0], cur[1]))
    # Line 2 (zigzag offset)
    for i, (dx, dy) in enumerate([(0,0),(20,12),(40,-8),(60,15),(80,-12),(100,8),(120,10),(140,-5)]):
        if i > 0:
            prev = (70 + [(0,0),(20,12),(40,-8),(60,15),(80,-12),(100,8),(120,10),(140,-5)][i-1][0],
                     175 + [(0,0),(20,12),(40,-8),(60,15),(80,-12),(100,8),(120,10),(140,-5)][i-1][1])
            cur = (70 + dx, 175 + dy)
            els.append(conn(f"w2_{i}", prev[0], prev[1], cur[0], cur[1]))

    # Arrow from left to right
    els.append(arrow("unmix_arrow", 250, 160, 460, 160))
    els.append(text("unmix_lbl", 355, 140, "Unmixing W", size=14))

    # Right box: "Independent Sources"
    els.append(box("indep_box", 560, 160, 180, 120))
    els.append(text("indep_lbl", 560, 100, "Independent Sources", size=14))

    # Clean separate lines inside right box
    # Line 1: smooth wave top
    for i, (dx, dy) in enumerate([(0,0),(20,-8),(40,6),(60,-6),(80,8),(100,-4),(120,5),(140,0)]):
        if i > 0:
            prev_pts = [(0,0),(20,-8),(40,6),(60,-6),(80,8),(100,-4),(120,5),(140,0)]
            prev = (480 + prev_pts[i-1][0], 140 + prev_pts[i-1][1])
            cur = (480 + dx, 140 + dy)
            els.append(conn(f"c1_{i}", prev[0], prev[1], cur[0], cur[1]))
    # Line 2: smooth wave bottom
    for i, (dx, dy) in enumerate([(0,0),(20,6),(40,-4),(60,7),(80,-6),(100,4),(120,-3),(140,0)]):
        if i > 0:
            prev_pts = [(0,0),(20,6),(40,-4),(60,7),(80,-6),(100,4),(120,-3),(140,0)]
            prev = (480 + prev_pts[i-1][0], 180 + prev_pts[i-1][1])
            cur = (480 + dx, 180 + dy)
            els.append(conn(f"c2_{i}", prev[0], prev[1], cur[0], cur[1]))

    save(os.path.join(OUTDIR, "cs229-ica.excalidraw"), els)

# ============================================================
# Ch17: MDP diagram
# ============================================================
def ch17_mdp():
    els = []
    # Title
    els.append(text("title", 300, 30, "Markov Decision Process", size=20))

    # 3 state circles in triangle
    s1 = (200, 150)
    s2 = (400, 150)
    s3 = (300, 300)

    els.append(node("s1", *s1, r=30))
    els.append(text("s1_lbl", *s1, "S1", size=16))
    els.append(node("s2", *s2, r=30))
    els.append(text("s2_lbl", *s2, "S2", size=16))
    els.append(node("s3", *s3, r=30))
    els.append(text("s3_lbl", *s3, "S3", size=16))

    # Arrows between states with action/reward labels
    # S1 -> S2
    els.append(arrow("a_s1s2", 230, 140, 370, 140))
    els.append(text("a1_lbl", 300, 122, "a1", size=12))
    els.append(text("r1_lbl", 300, 155, "r", size=11))

    # S2 -> S3
    els.append(arrow("a_s2s3", 390, 180, 320, 275))
    els.append(text("a2_lbl", 368, 225, "a2", size=12))
    els.append(text("r2_lbl", 340, 245, "r", size=11))

    # S3 -> S1
    els.append(arrow("a_s3s1", 275, 280, 210, 180))
    els.append(text("a3_lbl", 228, 228, "a1", size=12))
    els.append(text("r3_lbl", 250, 248, "r", size=11))

    # S1 -> S3
    els.append(arrow("a_s1s3", 210, 180, 280, 275))
    els.append(text("a4_lbl", 230, 228, "a2", size=12))

    save(os.path.join(OUTDIR, "cs229-mdp.excalidraw"), els)

# ============================================================
# Ch18: Continuous State MDP
# ============================================================
def ch18_value_approx():
    els = []
    # Title
    els.append(text("title", 400, 30, "Continuous State MDP", size=20))

    # Left: 3x3 grid of state boxes
    grid_x, grid_y = 120, 160
    cell = 45
    for r in range(3):
        for c in range(3):
            cx = grid_x + c * cell
            cy = grid_y + r * cell
            els.append(box(f"cell_{r}{c}", cx, cy, cell, cell, thin=True))
            els.append(text(f"clbl_{r}{c}", cx, cy, f"s{r*3+c+1}", size=10))

    els.append(text("grid_lbl", grid_x + cell, grid_y - 35, "Discrete States", size=13))

    # Arrow
    els.append(arrow("approx_arr", grid_x + cell*1.8, grid_y + cell, grid_x + cell*3.5, grid_y + cell))
    els.append(text("approx_lbl", grid_x + cell*2.6, grid_y + cell - 20, "Approximate", size=12))

    # Right: continuous curve (smooth line segments)
    curve_x = grid_x + cell * 4
    curve_y = grid_y + cell * 1.5
    pts = [(0, 0), (25, -30), (50, -55), (75, -40), (100, -20),
           (125, -50), (150, -35), (175, -10), (200, -25)]
    for i in range(1, len(pts)):
        x1 = curve_x + pts[i-1][0]
        y1 = curve_y + pts[i-1][1]
        x2 = curve_x + pts[i][0]
        y2 = curve_y + pts[i][1]
        els.append(conn(f"curve_{i}", x1, y1, x2, y2))

    els.append(text("curve_lbl", curve_x + 100, grid_y - 35, "Continuous V(s)", size=13))

    save(os.path.join(OUTDIR, "cs229-value-approximation.excalidraw"), els)

# ============================================================
# Ch19: LQR control loop
# ============================================================
def ch19_lqr():
    els = []
    # Title
    els.append(text("title", 400, 30, "Linear Quadratic Regulator", size=20))

    # Boxes in a loop: State -> Controller -> Action -> System -> (back to State)
    bw, bh = 120, 45
    y_mid = 160

    # State s_t
    els.append(box("state_box", 100, y_mid, bw, bh))
    els.append(text("state_lbl", 100, y_mid, "State s_t", size=14))

    # Controller
    els.append(box("ctrl_box", 300, y_mid, bw, bh))
    els.append(text("ctrl_lbl", 300, y_mid, "Controller", size=14))

    # Action a_t
    els.append(box("act_box", 500, y_mid, bw, bh))
    els.append(text("act_lbl", 500, y_mid, "Action a_t", size=14))

    # System
    els.append(box("sys_box", 700, y_mid, bw, bh))
    els.append(text("sys_lbl", 700, y_mid, "System", size=14))

    # Forward arrows
    els.append(arrow("arr1", 160, y_mid, 240, y_mid))
    els.append(arrow("arr2", 360, y_mid, 440, y_mid))
    els.append(arrow("arr3", 560, y_mid, 640, y_mid))

    # Feedback loop: System -> down -> left -> up -> State
    feedback_y = y_mid + 80
    els.append(arrow("fb1", 700, y_mid + bh/2, 700, feedback_y))
    els.append(arrow("fb2", 700, feedback_y, 100, feedback_y))
    els.append(arrow("fb3", 100, feedback_y, 100, y_mid + bh/2))

    els.append(text("fb_lbl", 400, feedback_y + 12, "Next state s_{t+1}", size=12))

    save(os.path.join(OUTDIR, "cs229-lqr.excalidraw"), els)

# ============================================================
# Ch20: Policy Search / REINFORCE
# ============================================================
def ch20_policy_search():
    els = []
    # Title
    els.append(text("title", 350, 30, "Policy Search", size=20))

    # Central box: Policy
    els.append(box("policy_box", 350, 170, 160, 50))
    els.append(text("policy_lbl", 350, 170, "Policy pi(a|s)", size=14))

    # Right box: Environment
    els.append(box("env_box", 600, 170, 140, 50))
    els.append(text("env_lbl", 600, 170, "Environment", size=14))

    # Bottom box: Rewards
    els.append(box("rew_box", 600, 310, 140, 50))
    els.append(text("rew_lbl", 600, 310, "Collect Rewards", size=12))

    # Left box: Update
    els.append(box("upd_box", 350, 310, 160, 50))
    els.append(text("upd_lbl", 350, 310, "Update (gradient)", size=12))

    # Circular flow arrows
    # Policy -> Environment (right)
    els.append(arrow("arr1", 430, 170, 530, 170))
    els.append(text("arr1_lbl", 480, 148, "Execute", size=11))

    # Environment -> Collect Rewards (down)
    els.append(arrow("arr2", 600, 195, 600, 285))

    # Collect Rewards -> Update (left)
    els.append(arrow("arr3", 530, 310, 430, 310))

    # Update -> Policy (up)
    els.append(arrow("arr4", 350, 285, 350, 195))

    save(os.path.join(OUTDIR, "cs229-policy-search.excalidraw"), els)


if __name__ == "__main__":
    ch16_ica()
    ch17_mdp()
    ch18_value_approx()
    ch19_lqr()
    ch20_policy_search()
    print("All diagrams generated.")
