#!/usr/bin/env python3
"""
Excalidraw diagram generator with accurate text measurement + collision avoidance.
Uses node-pretext for font width AND height calculation.
"""
import json, subprocess

# --- Measure text via node-pretext (width + height) ---
_measure_cache = {}
NODE_PRETEXT = "/Users/chajinwoo/Dev/node-pretext/src/cli.js"

def measure_text(text, font="14px Helvetica"):
    """Returns (width, height) measured by node-pretext."""
    key = (text, font)
    if key in _measure_cache:
        return _measure_cache[key]
    try:
        result = subprocess.run(
            ["node", NODE_PRETEXT, "--json", font, text],
            capture_output=True, text=True, timeout=5
        )
        data = json.loads(result.stdout.strip())
        # Use font size as minimum line height (ascent+descent can be smaller than visual)
        font_size = float(font.split("px")[0])
        w = data["width"]
        h = max(data["height"], font_size)  # at least font_size tall
        wh = (w, h)
    except:
        font_size = float(font.split("px")[0]) if "px" in font else 14
        wh = (len(text) * font_size * 0.6, font_size)
    _measure_cache[key] = wh
    return wh

def measure_multiline(text, font="14px Helvetica"):
    """Measure multi-line text. Returns (max_width, total_height, line_count)."""
    lines = text.split("\n")
    font_size = float(font.split("px")[0]) if "px" in font else 14
    line_height = font_size * 1.4  # Excalidraw uses ~1.25-1.4 line height
    max_w = 0
    for line in lines:
        w, _ = measure_text(line, font)
        max_w = max(max_w, w)
    total_h = line_height * len(lines)
    return (max_w, total_h, len(lines))

def _font_str(size, mono=False):
    return f"{size}px Courier" if mono else f"{size}px Helvetica"

# --- Bounding box helpers ---
def get_bbox(el):
    x = el.get("x", 0)
    y = el.get("y", 0)
    w = el.get("width", 0)
    h = el.get("height", 0)
    if el["type"] in ("arrow",) and "points" in el:
        pts = el["points"]
        xs = [x + p[0] for p in pts]
        ys = [y + p[1] for p in pts]
        return (min(xs), min(ys), max(xs), max(ys))
    return (x, y, x + abs(w), y + abs(h))

def overlaps(bbox1, bbox2, padding=4):
    x1, y1, x2, y2 = bbox1
    x3, y3, x4, y4 = bbox2
    return not (x2 + padding < x3 or x4 + padding < x1 or
                y2 + padding < y3 or y4 + padding < y1)

def nudge_text_away(text_el, obstacles, max_attempts=8, step=12):
    directions = [(0, step), (0, -step), (step, 0), (-step, 0),
                  (step, step), (-step, -step), (step, -step), (-step, step)]
    text_bbox = get_bbox(text_el)
    has_overlap = False
    for obs in obstacles:
        if overlaps(text_bbox, get_bbox(obs)):
            has_overlap = True
            break
    if not has_overlap:
        return text_el
    orig_x, orig_y = text_el["x"], text_el["y"]
    for dx, dy in directions:
        text_el["x"] = orig_x + dx
        text_el["y"] = orig_y + dy
        text_bbox = get_bbox(text_el)
        clean = True
        for obs in obstacles:
            if overlaps(text_bbox, get_bbox(obs)):
                clean = False
                break
        if clean:
            return text_el
    text_el["x"] = orig_x
    text_el["y"] = orig_y + step * 2
    return text_el

# --- Style constants ---
CONN = {
    "type": "arrow", "strokeColor": "#bbbbbb", "strokeWidth": 1, "opacity": 100,
    "roughness": 0, "fillStyle": "solid", "endArrowhead": None, "startArrowhead": None,
    "backgroundColor": "transparent"
}
ARROW = {
    "type": "arrow", "strokeColor": "#000000", "strokeWidth": 2, "opacity": 100,
    "roughness": 0, "fillStyle": "solid", "endArrowhead": "arrow", "startArrowhead": None,
    "backgroundColor": "transparent"
}
NODE = {
    "type": "ellipse", "strokeColor": "#000000", "strokeWidth": 2, "opacity": 100,
    "roughness": 0, "fillStyle": "solid", "backgroundColor": "transparent"
}
BOX = {
    "type": "rectangle", "strokeColor": "#000000", "strokeWidth": 2, "opacity": 100,
    "roughness": 0, "fillStyle": "solid", "backgroundColor": "transparent"
}
BOX_THIN = {**BOX, "strokeWidth": 1}

_seed = 0
def _next_seed():
    global _seed; _seed += 1; return _seed

def _base(eid):
    return {
        "id": eid, "angle": 0, "seed": _next_seed(),
        "version": 1, "versionNonce": _next_seed(),
        "isDeleted": False, "boundElements": None, "updated": 1,
        "link": None, "locked": False
    }

def node(eid, cx, cy, r=18):
    """Circle node centered at (cx, cy) with radius r."""
    return {**_base(eid), **NODE, "x": cx-r, "y": cy-r, "width": r*2, "height": r*2}

def box(eid, cx, cy, w, h, thin=False):
    """Rectangle centered at (cx, cy)."""
    style = BOX_THIN if thin else BOX
    return {**_base(eid), **style, "x": cx-w/2, "y": cy-h/2, "width": w, "height": h}

def text(eid, cx, cy, txt, size=14, align="center", mono=False):
    """Text centered at (cx, cy). Width+height measured via node-pretext."""
    font = _font_str(size, mono)
    if "\n" in txt:
        w, h, _ = measure_multiline(txt, font)
    else:
        w, h = measure_text(txt, font)
    x = cx - w/2 if align == "center" else cx
    y = cy - h/2
    style = {
        "type": "text", "strokeColor": "#000000", "opacity": 100, "roughness": 0,
        "fillStyle": "solid", "backgroundColor": "transparent",
        "fontFamily": 3 if mono else 1
    }
    return {**_base(eid), **style, "x": x, "y": y, "width": w, "height": h,
            "text": txt, "fontSize": size, "textAlign": align}

def labeled_box(eid, cx, cy, label, size=14, mono=False, pad_x=24, pad_y=16, thin=False):
    """Box with text inside, auto-sized to fit the label using measured dimensions.
    Returns a list of [box_element, text_element]."""
    font = _font_str(size, mono)
    if "\n" in label:
        tw, th, _ = measure_multiline(label, font)
    else:
        tw, th = measure_text(label, font)
    bw = tw + pad_x * 2
    bh = th + pad_y * 2

    box_el = box(f"{eid}_box", cx, cy, bw, bh, thin=thin)
    box_el["boundElements"] = [{"id": f"{eid}_txt", "type": "text"}]

    txt_el = text(f"{eid}_txt", cx, cy, label, size=size, mono=mono)
    txt_el["containerId"] = f"{eid}_box"
    txt_el["verticalAlign"] = "middle"
    txt_el["textAlign"] = "center"
    txt_el["x"] = cx - tw/2
    txt_el["y"] = cy - th/2

    return [box_el, txt_el]

def labeled_node(eid, cx, cy, label, size=12, r=None):
    """Circle node with text inside, auto-sized.
    Returns a list of [node_element, text_element]."""
    font = _font_str(size)
    tw, th = measure_text(label, font)
    if r is None:
        r = max(tw/2 + 8, th/2 + 8, 18)

    node_el = node(f"{eid}_node", cx, cy, r)
    node_el["boundElements"] = [{"id": f"{eid}_txt", "type": "text"}]

    txt_el = text(f"{eid}_txt", cx, cy, label, size=size)
    txt_el["containerId"] = f"{eid}_node"
    txt_el["verticalAlign"] = "middle"
    txt_el["textAlign"] = "center"
    txt_el["x"] = cx - tw/2
    txt_el["y"] = cy - th/2

    return [node_el, txt_el]

def conn(eid, x1, y1, x2, y2):
    """Connection line (no arrowheads)."""
    return {**_base(eid), **CONN, "x": x1, "y": y1,
            "width": x2-x1, "height": y2-y1, "points": [[0,0],[x2-x1,y2-y1]]}

def arrow(eid, x1, y1, x2, y2):
    """Arrow with arrowhead."""
    return {**_base(eid), **ARROW, "x": x1, "y": y1,
            "width": x2-x1, "height": y2-y1, "points": [[0,0],[x2-x1,y2-y1]]}

def connect_layers(prefix, centers_from, centers_to):
    """Connect all nodes between two layers. Centers are (x,y) tuples."""
    conns = []
    idx = 0
    for (x1, y1) in centers_from:
        for (x2, y2) in centers_to:
            conns.append(conn(f"{prefix}{idx}", x1, y1, x2, y2))
            idx += 1
    return conns

def resolve_overlaps(elements):
    """Post-process: nudge text elements that overlap with non-text elements.
    Skip text that has containerId (those are intentionally inside boxes)."""
    non_text = [el for el in elements if el["type"] != "text"]
    for el in elements:
        if el["type"] == "text" and not el.get("containerId"):
            nudge_text_away(el, non_text)
    return elements

def make_excalidraw(elements):
    return {
        "type": "excalidraw", "version": 2, "source": "cli",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {}
    }

def save(path, elements, auto_resolve=True):
    if auto_resolve:
        elements = resolve_overlaps(elements)
    with open(path, 'w') as f:
        json.dump(make_excalidraw(elements), f, indent=2)
    print(f"Saved: {path}")
