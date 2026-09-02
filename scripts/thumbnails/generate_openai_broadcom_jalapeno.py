from PIL import Image, ImageDraw, ImageFont
import os


SAVE_PATH = "/Users/chajinwoo/Vaults/AutoVault/markdown-blog/grid_Posts/_assets/openai-broadcom-jalapeno.png"
WIDTH, HEIGHT = 1200, 630
BLACK = "#111111"
GREEN = "#1a7a1a"
WHITE = "#ffffff"


def get_font(size, bold=False):
    candidates = []
    if bold:
        candidates.extend([
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf",
            "/System/Library/Fonts/SFNS.ttf",
        ])
    candidates.extend([
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ])

    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                pass
    return ImageFont.load_default()


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def centered_text(draw, y, text, font, fill, tracking=0):
    if tracking == 0:
        w, _ = text_size(draw, text, font)
        draw.text(((WIDTH - w) / 2, y), text, font=font, fill=fill)
        return

    widths = [text_size(draw, c, font)[0] for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (WIDTH - total) / 2
    for c, cw in zip(text, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += cw + tracking


def draw_chip(draw):
    cx, cy = WIDTH // 2, 346
    pkg_w, pkg_h = 520, 250
    left, top = cx - pkg_w // 2, cy - pkg_h // 2
    right, bottom = cx + pkg_w // 2, cy + pkg_h // 2

    pin_len = 17
    pin_gap = 24
    for x in range(left + 34, right - 30, pin_gap):
        draw.line((x, top - pin_len, x, top - 4), fill=BLACK, width=2)
        draw.line((x, bottom + 4, x, bottom + pin_len), fill=BLACK, width=2)
    for y in range(top + 30, bottom - 25, pin_gap):
        draw.line((left - pin_len, y, left - 4, y), fill=BLACK, width=2)
        draw.line((right + 4, y, right + pin_len, y), fill=BLACK, width=2)

    draw.rounded_rectangle((left, top, right, bottom), radius=4, outline=GREEN, width=4, fill=WHITE)

    die_margin_x, die_margin_y = 54, 34
    dleft, dtop = left + die_margin_x, top + die_margin_y
    dright, dbottom = right - die_margin_x, bottom - die_margin_y
    draw.rectangle((dleft, dtop, dright, dbottom), outline=BLACK, width=3)

    cols, rows = 8, 5
    for i in range(1, cols):
        x = dleft + (dright - dleft) * i / cols
        draw.line((x, dtop, x, dbottom), fill=BLACK, width=1)
    for j in range(1, rows):
        y = dtop + (dbottom - dtop) * j / rows
        draw.line((dleft, y, dright, y), fill=BLACK, width=1)

    blocks = [
        (1, 1, 2, 2),
        (4, 1, 6, 2),
        (2, 3, 3, 4),
        (5, 3, 7, 4),
    ]
    cell_w = (dright - dleft) / cols
    cell_h = (dbottom - dtop) / rows
    for c1, r1, c2, r2 in blocks:
        x1 = dleft + c1 * cell_w + 9
        y1 = dtop + r1 * cell_h + 8
        x2 = dleft + c2 * cell_w - 9
        y2 = dtop + r2 * cell_h - 8
        draw.rectangle((x1, y1, x2, y2), outline=BLACK, width=2)

    pad = 5
    for x in range(left + 38, right - 35, 38):
        draw.rectangle((x - pad / 2, top + 12, x + pad / 2, top + 17), fill=BLACK)
        draw.rectangle((x - pad / 2, bottom - 17, x + pad / 2, bottom - 12), fill=BLACK)
    for y in range(top + 38, bottom - 35, 38):
        draw.rectangle((left + 12, y - pad / 2, left + 17, y + pad / 2), fill=BLACK)
        draw.rectangle((right - 17, y - pad / 2, right - 12, y + pad / 2), fill=BLACK)


def main():
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)

    heading_font = get_font(96, bold=True)
    sub_font = get_font(31, bold=False)
    sub2_font = get_font(28, bold=False)

    centered_text(draw, 54, "Jalapeño", heading_font, GREEN)
    centered_text(draw, 157, "OpenAI x Broadcom", sub_font, BLACK)
    centered_text(draw, 202, "AI Inference Chip · TSMC 3nm · 50% Cost Reduction", sub2_font, BLACK)

    draw_chip(draw)

    img.save(SAVE_PATH, "PNG", optimize=True)
    print(SAVE_PATH)
    print(os.path.exists(SAVE_PATH))
    print(os.path.getsize(SAVE_PATH))


if __name__ == "__main__":
    main()
