import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT_PATH = Path(
    "/Users/cha/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/"
    "블로그/markdown-blog/grid_Posts/_assets/fable5-export-control.png"
)

WIDTH, HEIGHT = 1200, 630
WHITE = "#FFFFFF"
BLACK = "#111111"
RED = "#CC0000"
GRAY = "#888888"


def load_font(size, bold=False):
    names = [
        "Arial Bold.ttf" if bold else "Arial.ttf",
        "Arial Bold" if bold else "Arial",
        "Helvetica-Bold.ttf" if bold else "Helvetica.ttf",
        "Helvetica Bold" if bold else "Helvetica",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "DejaVuSans-Bold" if bold else "DejaVuSans",
    ]
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/Library/Fonts/DejaVuSans-Bold.ttf" if bold else "/Library/Fonts/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for font_name in names:
        try:
            return ImageFont.truetype(font_name, size=size)
        except OSError:
            pass

    for font_path in paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size=size)
            except OSError:
                pass

    return ImageFont.load_default()


def text_size(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def draw_wire_cube(draw):
    y_shift = 40
    front = [(350, 315 + y_shift), (700, 315 + y_shift), (700, 500 + y_shift), (350, 500 + y_shift)]
    back = [(435, 255 + y_shift), (785, 255 + y_shift), (785, 440 + y_shift), (435, 440 + y_shift)]

    draw.line(front + [front[0]], fill=BLACK, width=4, joint="curve")
    draw.line(back + [back[0]], fill=BLACK, width=3, joint="curve")
    for i in range(4):
        draw.line([front[i], back[i]], fill=BLACK, width=3)

    for x in (420, 490, 560, 630):
        draw.line([(x, 315 + y_shift), (x + 85, 255 + y_shift)], fill=BLACK, width=2)
        draw.line([(x, 500 + y_shift), (x + 85, 440 + y_shift)], fill=BLACK, width=2)

    for y in (352, 389, 426, 463):
        draw.line([(350, y + y_shift), (700, y + y_shift)], fill=BLACK, width=2)
        draw.line([(435, y - 60 + y_shift), (785, y - 60 + y_shift)], fill=BLACK, width=2)

    for x in range(372, 704, 48):
        draw.line([(x, 505 + y_shift), (x, 525 + y_shift)], fill=BLACK, width=3)
    for x in range(455, 787, 48):
        draw.line([(x, 250 + y_shift), (x, 230 + y_shift)], fill=BLACK, width=3)
    for y in range(335, 493, 38):
        draw.line([(345, y + y_shift), (325, y + y_shift)], fill=BLACK, width=3)
        draw.line([(790, y - 60 + y_shift), (810, y - 60 + y_shift)], fill=BLACK, width=3)


def draw_restricted_stamp(draw, font):
    cx, cy = 720, 422
    outer_r = 112
    inner_r = 94
    bbox_outer = [cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r]
    bbox_inner = [cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r]

    draw.ellipse(bbox_outer, outline=RED, width=7)
    draw.ellipse(bbox_inner, outline=RED, width=3)

    angle = math.radians(-12)
    word = "RESTRICTED"
    tw, th = text_size(draw, word, font)
    stamp = Image.new("RGBA", (tw + 60, th + 36), (255, 255, 255, 0))
    stamp_draw = ImageDraw.Draw(stamp)
    stamp_draw.rectangle(
        [10, 9, tw + 50, th + 27],
        outline=RED,
        width=4,
    )
    stamp_draw.text((30, 15), word, font=font, fill=RED)
    stamp = stamp.rotate(math.degrees(angle), expand=True, resample=Image.Resampling.BICUBIC)
    image.alpha_composite(stamp, (cx - stamp.width // 2, cy - stamp.height // 2))

    x_span = 60
    y_span = 60
    draw.line([(cx - x_span, cy - y_span), (cx + x_span, cy + y_span)], fill=RED, width=8)
    draw.line([(cx + x_span, cy - y_span), (cx - x_span, cy + y_span)], fill=RED, width=8)


image = Image.new("RGBA", (WIDTH, HEIGHT), WHITE)
draw = ImageDraw.Draw(image)

title_font = load_font(76, bold=True)
subtitle_font = load_font(46, bold=True)
caption_font = load_font(24, bold=False)
stamp_font = load_font(31, bold=True)

draw.text((76, 66), "Fable 5", font=title_font, fill=BLACK)
draw.text((80, 155), "Export Control", font=subtitle_font, fill=BLACK)
draw.text(
    (82, 220),
    "U.S. Commerce Dept · Foreign National Access Prohibited",
    font=caption_font,
    fill=GRAY,
)

draw_wire_cube(draw)
draw_restricted_stamp(draw, stamp_font)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
image.convert("RGB").save(OUT_PATH, "PNG")

print(os.path.exists(OUT_PATH))
print(str(OUT_PATH))
