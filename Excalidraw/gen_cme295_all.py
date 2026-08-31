#!/usr/bin/env python3
"""Generate all 11 CME295 Excalidraw diagrams using gen_diagram.py helpers."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_diagram import (
    labeled_box, labeled_node, box, text, arrow, conn, save, node
)

SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

def s(name):
    return os.path.join(SAVE_DIR, name)

# ============================================================
# 1. Self-Attention Mechanism
# ============================================================
def diagram_self_attention():
    els = []
    # Title
    els.append(text("title", 400, 30, "Self-Attention Mechanism", size=20))

    # Input tokens
    tokens = ["a", "cute", "teddy", "bear"]
    xs = [200, 320, 440, 560]
    for i, tok in enumerate(tokens):
        els.extend(labeled_box(f"in{i}", xs[i], 80, tok))

    # Q/K/V labels
    els.append(text("qlbl", 140, 140, "Q", size=12))
    els.append(text("klbl", 170, 140, "K", size=12))
    els.append(text("vlbl", 200, 140, "V", size=12))

    # Arrows from inputs to grid
    for i in range(4):
        els.append(arrow(f"in_arr{i}", xs[i], 100, xs[i], 160))

    # 4x4 attention grid
    cell = 40
    gx0 = 200 - cell/2
    gy0 = 180
    for r in range(4):
        for c in range(4):
            cx = gx0 + c * cell + cell/2
            cy = gy0 + r * cell + cell/2
            shade = 0.3 + 0.7 * ((r + c) % 3) / 2
            els.append(box(f"cell{r}{c}", cx, cy, cell-2, cell-2, thin=True))

    # Label near grid
    els.append(text("gridlbl", 620, 220, "Q * K^T / sqrt(d_k)", size=12))

    # Arrows from grid to outputs
    for i in range(4):
        els.append(arrow(f"out_arr{i}", xs[i], gy0 + 4*cell + 10, xs[i], gy0 + 4*cell + 50))

    # Output tokens
    out_tokens = ["a'", "cute'", "teddy'", "bear'"]
    for i, tok in enumerate(out_tokens):
        els.extend(labeled_box(f"out{i}", xs[i], gy0 + 4*cell + 80, tok))

    save(s("cme295-self-attention.excalidraw"), els)

# ============================================================
# 2. Transformer Architecture
# ============================================================
def diagram_transformer():
    els = []
    els.append(text("title", 400, 20, "Transformer Architecture", size=20))

    # --- Encoder (left) ---
    ex = 200
    els.append(text("enc_title", ex, 60, "Encoder", size=16))
    enc_boxes = [
        ("enc1", ex, 110, "Input Emb + Pos"),
        ("enc2", ex, 180, "Multi-Head\nSelf-Attention"),
        ("enc3", ex, 260, "Feed Forward"),
    ]
    for eid, cx, cy, lbl in enc_boxes:
        els.extend(labeled_box(eid, cx, cy, lbl))
    els.append(arrow("enc_a1", ex, 130, ex, 155))
    els.append(arrow("enc_a2", ex, 210, ex, 235))
    els.append(text("enc_xn", ex + 100, 180, "x N", size=14))

    # --- Decoder (right) ---
    dx = 550
    els.append(text("dec_title", dx, 60, "Decoder", size=16))
    dec_boxes = [
        ("dec1", dx, 110, "Output Emb + Pos"),
        ("dec2", dx, 180, "Masked\nSelf-Attention"),
        ("dec3", dx, 260, "Cross-Attention"),
        ("dec4", dx, 340, "Feed Forward"),
        ("dec5", dx, 420, "Linear + Softmax"),
    ]
    for eid, cx, cy, lbl in dec_boxes:
        els.extend(labeled_box(eid, cx, cy, lbl))
    els.append(arrow("dec_a1", dx, 130, dx, 155))
    els.append(arrow("dec_a2", dx, 210, dx, 235))
    els.append(arrow("dec_a3", dx, 285, dx, 315))
    els.append(arrow("dec_a4", dx, 365, dx, 395))
    els.append(text("dec_xn", dx + 110, 220, "x N", size=14))

    # Arrow from encoder to cross-attention
    els.append(arrow("enc2dec", ex + 80, 260, dx - 80, 260))
    els.append(text("kv_lbl", 375, 248, "K, V", size=12))

    save(s("cme295-transformer-architecture.excalidraw"), els)

# ============================================================
# 3. Position Embeddings
# ============================================================
def diagram_position_embeddings():
    els = []
    els.append(text("title", 400, 30, "Position Embeddings", size=20))

    items = [
        ("pe1", 150, 120, "Sinusoidal\nFixed, absolute"),
        ("pe2", 400, 120, "ALiBi\nLinear bias"),
        ("pe3", 650, 120, "RoPE\nRotation, relative"),
    ]
    for eid, cx, cy, lbl in items:
        els.extend(labeled_box(eid, cx, cy, lbl))

    els.append(arrow("a1", 230, 120, 310, 120))
    els.append(arrow("a2", 490, 120, 570, 120))

    save(s("cme295-position-embeddings.excalidraw"), els)

# ============================================================
# 4. Mixture of Experts
# ============================================================
def diagram_moe():
    els = []
    els.append(text("title", 400, 30, "Mixture of Experts", size=20))

    els.extend(labeled_box("inp", 80, 160, "Input"))
    els.extend(labeled_box("gate", 240, 160, "Gate/Router"))
    els.append(arrow("a1", 120, 160, 180, 160))

    experts = ["E1", "E2", "E3", "E4"]
    ey = [100, 160, 220, 280]
    for i, (e, y) in enumerate(zip(experts, ey)):
        thin = i not in (0, 2)
        b = labeled_box(f"e{i}", 420, y, e, thin=thin)
        if not thin:
            b[0]["strokeWidth"] = 4  # thicker border for selected
        els.extend(b)
        els.append(arrow(f"ga{i}", 300, 160, 380, y))

    els.extend(labeled_box("out", 600, 160, "Output"))
    for i, y in enumerate(ey):
        els.append(arrow(f"ea{i}", 460, y, 560, 160))

    save(s("cme295-moe-architecture.excalidraw"), els)

# ============================================================
# 5. LLM Training Pipeline
# ============================================================
def diagram_training():
    els = []
    els.append(text("title", 300, 30, "LLM Training Pipeline", size=20))

    steps = [
        ("t1", 300, 100, "Pre-training\n(next token)"),
        ("t2", 300, 200, "SFT\n(instruction tuning)"),
        ("t3", 300, 300, "LoRA / QLoRA"),
    ]
    for eid, cx, cy, lbl in steps:
        els.extend(labeled_box(eid, cx, cy, lbl))

    els.append(arrow("ta1", 300, 135, 300, 170))
    els.append(arrow("ta2", 300, 235, 300, 275))

    # Side labels
    els.append(text("dl1", 480, 100, "Trillions of tokens", size=11))
    els.append(text("dl2", 480, 200, "~100K examples", size=11))
    els.append(text("dl3", 480, 300, "Parameter-efficient", size=11))

    save(s("cme295-training-pipeline.excalidraw"), els)

# ============================================================
# 6. RLHF Pipeline
# ============================================================
def diagram_rlhf():
    els = []
    els.append(text("title", 400, 20, "RLHF Pipeline", size=20))

    # Main flow
    els.extend(labeled_box("pr", 80, 120, "Prompt"))
    els.extend(labeled_box("llm", 240, 120, "LLM\n(Policy)"))
    els.extend(labeled_box("resp", 420, 120, "Response"))
    els.extend(labeled_box("rm", 600, 120, "Reward\nModel"))
    els.extend(labeled_box("sc", 600, 240, "Score"))

    els.append(arrow("a1", 130, 120, 180, 120))
    els.append(arrow("a2", 310, 120, 360, 120))
    els.append(arrow("a3", 480, 120, 540, 120))
    els.append(arrow("a4", 600, 155, 600, 210))

    # Feedback arrow from Score back to LLM
    els.append(arrow("fb", 560, 240, 240, 170))
    els.append(text("ppo_lbl", 380, 220, "PPO", size=12))

    # Human preferences
    els.extend(labeled_box("hp", 750, 50, "Human\nPreferences"))
    els.append(arrow("hp_a", 750, 85, 670, 95))

    save(s("cme295-rlhf-pipeline.excalidraw"), els)

# ============================================================
# 7. GRPO
# ============================================================
def diagram_grpo():
    els = []
    els.append(text("title", 350, 20, "GRPO", size=20))

    els.extend(labeled_box("pr", 350, 70, "Prompt"))
    els.append(arrow("a1", 350, 95, 350, 120))
    els.extend(labeled_box("llm", 350, 150, "LLM"))

    # 4 outputs
    oxs = [200, 300, 400, 500]
    for i, ox in enumerate(oxs):
        els.append(arrow(f"oa{i}", 350, 175, ox, 220))
        els.extend(labeled_box(f"o{i}", ox, 245, f"o{i+1}", size=12))

    # Rewards
    els.extend(labeled_box("rew", 350, 320, "Rewards\nR1..R4"))
    for i, ox in enumerate(oxs):
        els.append(arrow(f"ra{i}", ox, 265, 350, 295))

    # Group advantage
    els.extend(labeled_box("ga", 350, 410, "Group Advantage\nmean/std"))
    els.append(arrow("a5", 350, 350, 350, 380))

    # Update back to LLM
    els.append(arrow("upd", 200, 410, 200, 150))
    els.append(text("upd_lbl", 140, 280, "Update", size=12))

    # Label
    els.append(text("nvm", 520, 410, "No Value Model", size=12))

    save(s("cme295-grpo.excalidraw"), els)

# ============================================================
# 8. RAG Pipeline
# ============================================================
def diagram_rag():
    els = []
    els.append(text("title", 450, 30, "RAG Pipeline", size=20))

    items = [
        ("q", 80, 120, "Query"),
        ("ret", 230, 120, "Retriever"),
        ("kb", 400, 120, "Knowledge\nBase"),
        ("aug", 580, 120, "Augmented\nPrompt"),
        ("llm", 740, 120, "LLM"),
        ("resp", 880, 120, "Response"),
    ]
    for eid, cx, cy, lbl in items:
        els.extend(labeled_box(eid, cx, cy, lbl))

    arrows_x = [(130, 170), (290, 340), (470, 520), (650, 690), (780, 830)]
    for i, (x1, x2) in enumerate(arrows_x):
        els.append(arrow(f"ra{i}", x1, 120, x2, 120))

    save(s("cme295-rag-pipeline.excalidraw"), els)

# ============================================================
# 9. LLM-as-a-Judge
# ============================================================
def diagram_llm_judge():
    els = []
    els.append(text("title", 350, 20, "LLM-as-a-Judge", size=20))

    els.extend(labeled_box("inp", 350, 90, "Prompt +\nResponse +\nCriteria"))
    els.append(arrow("a1", 350, 130, 350, 170))
    els.extend(labeled_box("judge", 350, 200, "Judge LLM"))

    # Two outputs
    els.append(arrow("a2l", 300, 225, 240, 270))
    els.append(arrow("a2r", 400, 225, 460, 270))
    els.extend(labeled_box("rat", 240, 300, "Rationale"))
    els.extend(labeled_box("scr", 460, 300, "Score"))

    save(s("cme295-llm-judge.excalidraw"), els)

# ============================================================
# 10. Vision Transformer
# ============================================================
def diagram_vit():
    els = []
    els.append(text("title", 500, 30, "Vision Transformer", size=20))

    items = [
        ("img", 80, 120, "Image"),
        ("pat", 220, 120, "Patches"),
        ("flat", 380, 120, "Flatten +\nLinear"),
        ("pos", 540, 120, "Pos Emb"),
        ("enc", 700, 120, "Transformer\nEncoder"),
        ("cls", 880, 120, "[CLS]\nClassify"),
    ]
    for eid, cx, cy, lbl in items:
        els.extend(labeled_box(eid, cx, cy, lbl))

    arrows_x = [(130, 170), (270, 310), (450, 490), (590, 630), (780, 820)]
    for i, (x1, x2) in enumerate(arrows_x):
        els.append(arrow(f"va{i}", x1, 120, x2, 120))

    save(s("cme295-vit.excalidraw"), els)

# ============================================================
# 11. Diffusion-based LLM
# ============================================================
def diagram_diffusion_llm():
    els = []
    els.append(text("title", 350, 20, "Diffusion-based LLM", size=20))

    els.extend(labeled_box("d1", 350, 90, "Masked Tokens\n[X][X][the][X]"))
    els.append(arrow("da1", 350, 125, 350, 165))
    els.append(text("dlbl1", 450, 145, "Reverse (Unmask)", size=11))

    els.extend(labeled_box("d2", 350, 200, "Partial\n[A][X][the][cat]"))
    els.append(arrow("da2", 350, 235, 350, 275))

    els.extend(labeled_box("d3", 350, 310, "Complete Text\n[A][cute][the][cat]"))

    els.append(text("side", 550, 200, "Coarse to Fine", size=13))

    save(s("cme295-diffusion-llm.excalidraw"), els)

# ============================================================
# Run all
# ============================================================
if __name__ == "__main__":
    diagram_self_attention()
    diagram_transformer()
    diagram_position_embeddings()
    diagram_moe()
    diagram_training()
    diagram_rlhf()
    diagram_grpo()
    diagram_rag()
    diagram_llm_judge()
    diagram_vit()
    diagram_diffusion_llm()
    print("All 11 diagrams generated.")
