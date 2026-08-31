#!/usr/bin/env python3
"""Generate 5 Hinton blog Excalidraw diagrams."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_diagram import labeled_box, arrow, text, save, conn

EDIR = os.path.dirname(__file__)

# ─── 1. SimCLR ───
def gen_simclr():
    els = []
    els += [text("title", 400, 20, "SimCLR", size=24)]
    # Image box
    els += labeled_box("img", 100, 120, "Image")
    # Augment 1 & 2
    els += labeled_box("aug1", 300, 70, "Augment 1")
    els += labeled_box("aug2", 300, 170, "Augment 2")
    # Arrows from Image to Augments
    els += [arrow("a1", 148, 110, 248, 75)]
    els += [arrow("a2", 148, 130, 248, 165)]
    # Encoder
    els += labeled_box("enc1", 480, 70, "Encoder")
    els += labeled_box("enc2", 480, 170, "Encoder")
    els += [arrow("a3", 358, 70, 428, 70)]
    els += [arrow("a4", 358, 170, 428, 170)]
    # Projection
    els += labeled_box("proj1", 640, 70, "Projection")
    els += labeled_box("proj2", 640, 170, "Projection")
    els += [arrow("a5", 532, 70, 582, 70)]
    els += [arrow("a6", 532, 170, 582, 170)]
    # Similarity arrow between projections
    els += [arrow("sim1", 700, 90, 700, 150)]
    els += [arrow("sim2", 700, 150, 700, 90)]
    els += [text("simlbl", 760, 115, "Maximize\nSimilarity", size=12)]
    save(os.path.join(EDIR, "hinton-simclr.excalidraw"), els)

# ─── 2. SimCLRv2 ───
def gen_simclrv2():
    els = []
    els += [text("title", 250, 20, "SimCLRv2 Pipeline", size=24)]
    cx = 250
    els += labeled_box("s1", cx, 100, "1. Self-supervised\nPre-training")
    els += labeled_box("s2", cx, 210, "2. Fine-tune\n(few labels)")
    els += labeled_box("s3", cx, 320, "3. Knowledge\nDistillation")
    els += [arrow("a1", cx, 135, cx, 175)]
    els += [arrow("a2", cx, 245, cx, 285)]
    save(os.path.join(EDIR, "hinton-simclrv2.excalidraw"), els)

# ─── 3. BYOL ───
def gen_byol():
    els = []
    els += [text("title", 350, 20, "BYOL", size=24)]
    # Online path
    els += labeled_box("on", 120, 100, "Online\nNetwork")
    els += labeled_box("pred", 320, 100, "Predictor")
    els += labeled_box("out1", 500, 100, "Output")
    els += [arrow("a1", 185, 100, 255, 100)]
    els += [arrow("a2", 385, 100, 445, 100)]
    # Target path
    els += labeled_box("tgt", 120, 230, "Target Network\n(EMA)")
    els += labeled_box("out2", 500, 230, "Output")
    els += [arrow("a3", 200, 230, 440, 230)]
    # Similarity
    els += [arrow("sim1", 540, 130, 540, 200)]
    els += [arrow("sim2", 540, 200, 540, 130)]
    els += [text("simlbl", 600, 160, "Maximize\nSimilarity", size=12)]
    # EMA update arrow
    els += [arrow("ema", 120, 140, 120, 195)]
    els += [text("emalbl", 50, 165, "EMA\nUpdate", size=11)]
    # No negatives text
    els += [text("noneg", 350, 310, "No Negative Samples", size=14)]
    save(os.path.join(EDIR, "hinton-byol.excalidraw"), els)

# ─── 4. GLOM ───
def gen_glom():
    els = []
    els += [text("title", 280, 15, "GLOM", size=24)]
    # Grid: 3 cols x 3 rows
    labels = [
        ["Object", "Object", "Object"],
        ["Part",   "Part",   "Part"],
        ["Pixel",  "Pixel",  "Pixel"],
    ]
    xs = [130, 280, 430]
    ys = [80, 170, 260]
    for r, row in enumerate(labels):
        for c, lbl in enumerate(row):
            els += labeled_box(f"g{r}{c}", xs[c], ys[r], lbl)
    # Horizontal arrows (Agree) - same level
    for r in range(3):
        for c in range(2):
            els += [arrow(f"h{r}{c}", xs[c]+50, ys[r], xs[c+1]-50, ys[r])]
    els += [text("agree_lbl", 280, 285, "Agree (same level)", size=11)]
    # Vertical arrows (top-down / bottom-up)
    for c in range(3):
        # top-down: Object -> Part
        els += [arrow(f"td{c}", xs[c], ys[0]+20, xs[c], ys[1]-20)]
        # bottom-up: Pixel -> Part
        els += [arrow(f"bu{c}", xs[c], ys[2]-20, xs[c], ys[1]+20)]
    els += [text("td_lbl", 490, 120, "Top-down", size=11)]
    els += [text("bu_lbl", 490, 220, "Bottom-up", size=11)]
    save(os.path.join(EDIR, "hinton-glom.excalidraw"), els)

# ─── 5. Forward-Forward ───
def gen_ff():
    els = []
    els += [text("title", 380, 15, "Forward-Forward Algorithm", size=24)]
    # Positive row
    els += labeled_box("pos", 80, 100, "Positive\nData")
    els += labeled_box("l1p", 240, 100, "Layer 1")
    els += labeled_box("l2p", 400, 100, "Layer 2")
    els += labeled_box("l3p", 560, 100, "Layer 3")
    els += [arrow("ap1", 145, 100, 185, 100)]
    els += [arrow("ap2", 298, 100, 345, 100)]
    els += [arrow("ap3", 458, 100, 505, 100)]
    # Goodness+ arrows (up from each layer)
    els += [arrow("gp1", 240, 72, 240, 50)]
    els += [text("gp1t", 240, 40, "Goodness+", size=10)]
    els += [arrow("gp2", 400, 72, 400, 50)]
    els += [text("gp2t", 400, 40, "Goodness+", size=10)]
    els += [arrow("gp3", 560, 72, 560, 50)]
    els += [text("gp3t", 560, 40, "Goodness+", size=10)]
    # Negative row
    els += labeled_box("neg", 80, 220, "Negative\nData")
    els += labeled_box("l1n", 240, 220, "Layer 1")
    els += labeled_box("l2n", 400, 220, "Layer 2")
    els += labeled_box("l3n", 560, 220, "Layer 3")
    els += [arrow("an1", 145, 220, 185, 220)]
    els += [arrow("an2", 298, 220, 345, 220)]
    els += [arrow("an3", 458, 220, 505, 220)]
    # Goodness- arrows (down from each layer)
    els += [arrow("gn1", 240, 248, 240, 270)]
    els += [text("gn1t", 240, 278, "Goodness-", size=10)]
    els += [arrow("gn2", 400, 248, 400, 270)]
    els += [text("gn2t", 400, 278, "Goodness-", size=10)]
    els += [arrow("gn3", 560, 248, 560, 270)]
    els += [text("gn3t", 560, 278, "Goodness-", size=10)]
    save(os.path.join(EDIR, "hinton-forward-forward.excalidraw"), els)

if __name__ == "__main__":
    gen_simclr()
    gen_simclrv2()
    gen_byol()
    gen_glom()
    gen_ff()
    print("All 5 diagrams generated.")
