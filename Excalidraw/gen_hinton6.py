#!/usr/bin/env python3
"""Generate 6 Excalidraw diagrams for Hinton blog posts."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_diagram import labeled_box, text, arrow, node, box, save

OUTDIR = os.path.dirname(__file__)

# ── 1. Transforming Auto-encoder ──
def diagram_transforming_ae():
    els = []
    xs = [100, 320, 540, 760]
    y = 200
    labels = ["Input x", "Encoder\n(h, transform t)", "Decoder\n(h + delta_t)", "Output x'"]
    ids = ["tae_in", "tae_enc", "tae_dec", "tae_out"]
    for i, (x, lbl, eid) in enumerate(zip(xs, labels, ids)):
        els += labeled_box(eid, x, y, lbl)
    # arrows between boxes
    for i in range(3):
        els.append(arrow(f"tae_a{i}", xs[i]+70, y, xs[i+1]-70, y))
    els.append(text("tae_title", 430, 80, "Transforming Auto-encoder", size=20))
    save(os.path.join(OUTDIR, "hinton-transforming-ae.excalidraw"), els)

# ── 2. AlexNet ──
def diagram_alexnet():
    els = []
    xs = [80, 220, 360, 480, 600, 720]
    y = 200
    labels = ["Input\n224x224", "Conv1-5", "Pool", "FC1", "FC2", "FC3\n1000 classes"]
    ids = ["alex_in", "alex_conv", "alex_pool", "alex_fc1", "alex_fc2", "alex_fc3"]
    for i, (x, lbl, eid) in enumerate(zip(xs, labels, ids)):
        els += labeled_box(eid, x, y, lbl)
    for i in range(5):
        els.append(arrow(f"alex_a{i}", xs[i]+55, y, xs[i+1]-55, y))
    # Labels near FC layers
    els.append(text("alex_relu", 540, 130, "ReLU", size=12))
    els.append(text("alex_drop", 660, 130, "Dropout", size=12))
    els.append(text("alex_title", 400, 70, "AlexNet", size=20))
    save(os.path.join(OUTDIR, "hinton-alexnet.excalidraw"), els)

# ── 3. DNN-HMM Speech Recognition ──
def diagram_dnn_speech():
    els = []
    els += labeled_box("sp_audio", 100, 200, "Audio\nFrames")
    els += labeled_box("sp_dnn", 320, 200, "DNN\n(5-7 layers)")
    els += labeled_box("sp_states", 540, 200, "HMM States")
    els += labeled_box("sp_hmm", 540, 360, "HMM\n(time sequence)")
    els.append(arrow("sp_a1", 175, 200, 245, 200))
    els.append(arrow("sp_a2", 395, 200, 465, 200))
    els.append(arrow("sp_a3", 540, 240, 540, 320))
    els.append(text("sp_title", 320, 80, "DNN-HMM Speech Recognition", size=20))
    save(os.path.join(OUTDIR, "hinton-dnn-speech.excalidraw"), els)

# ── 4. Dropout (original) ──
def diagram_dropout_orig():
    els = []
    # Training network (left) with some nodes X'd out
    tx, ty = 160, 120
    els.append(text("do_train_lbl", tx, ty-60, "Training", size=16))
    # 3 layers: input(4), hidden(4 with 2 X'd), output(2)
    layers_t = []
    for li, (ny, yy) in enumerate([(4, ty), (4, ty+100), (2, ty+200)]):
        centers = []
        for ni in range(ny):
            cx = tx - (ny-1)*25 + ni*50
            cy = yy
            eid = f"do_t_n{li}_{ni}"
            els.append(node(eid, cx, cy, r=16))
            centers.append((cx, cy))
            # X out some hidden nodes
            if li == 1 and ni in (1, 3):
                els.append(text(f"do_t_x{li}_{ni}", cx, cy, "X", size=14))
        layers_t.append(centers)

    # Testing network (right) all active
    rx, ry = 440, 120
    els.append(text("do_test_lbl", rx, ry-60, "Testing", size=16))
    layers_r = []
    for li, (ny, yy) in enumerate([(4, ry), (4, ry+100), (2, ry+200)]):
        centers = []
        for ni in range(ny):
            cx = rx - (ny-1)*25 + ni*50
            cy = yy
            eid = f"do_r_n{li}_{ni}"
            els.append(node(eid, cx, cy, r=16))
            centers.append((cx, cy))
        layers_r.append(centers)

    els.append(text("do_title", 300, 20, "Dropout", size=20))
    save(os.path.join(OUTDIR, "hinton-dropout-orig.excalidraw"), els)

# ── 5. Initialization + Momentum ──
def diagram_init_momentum():
    els = []
    xs = [120, 340, 560]
    y = 200
    labels = ["Sparse Init", "Nesterov\nMomentum", "Deep Network\nTrainable"]
    ids = ["im_init", "im_nest", "im_deep"]
    for i, (x, lbl, eid) in enumerate(zip(xs, labels, ids)):
        els += labeled_box(eid, x, y, lbl)
    for i in range(2):
        els.append(arrow(f"im_a{i}", xs[i]+75, y, xs[i+1]-75, y))
    els.append(text("im_title", 340, 90, "Initialization + Momentum", size=20))
    save(os.path.join(OUTDIR, "hinton-init-momentum.excalidraw"), els)

# ── 6. Dropout as Ensemble (JMLR) ──
def diagram_dropout_jmlr():
    els = []
    els += labeled_box("dj_full", 300, 100, "Full Network")
    thin_xs = [120, 300, 480]
    thin_labels = ["Thin Net 1", "Thin Net 2", "Thin Net 3"]
    for i, (x, lbl) in enumerate(zip(thin_xs, thin_labels)):
        els += labeled_box(f"dj_t{i}", x, 240, lbl)
        els.append(arrow(f"dj_a_down{i}", 300, 135, x, 205))
    els += labeled_box("dj_avg", 300, 380, "Average\n= Ensemble")
    for i, x in enumerate(thin_xs):
        els.append(arrow(f"dj_a_up{i}", x, 275, 300, 340))
    els.append(text("dj_title", 300, 30, "Dropout as Ensemble", size=20))
    save(os.path.join(OUTDIR, "hinton-dropout-jmlr.excalidraw"), els)

if __name__ == "__main__":
    diagram_transforming_ae()
    diagram_alexnet()
    diagram_dnn_speech()
    diagram_dropout_orig()
    diagram_init_momentum()
    diagram_dropout_jmlr()
    print("All 6 diagrams generated.")
