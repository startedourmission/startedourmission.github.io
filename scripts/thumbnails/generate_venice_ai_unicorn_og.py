from pathlib import Path
import os

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1200, 630
BLACK = "#000000"
WHITE = "#FFFFFF"
OUTPUT_PATH = Path(
    "/Users/chajinwoo/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/"
    "markdown-blog/grid_Posts/_assets/venice-ai-unicorn.png"
)


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def centered_text(draw, y, text, text_font, fill=BLACK):
    bbox = draw.textbbox((0, 0), text, font=text_font)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2
    draw.text((x, y), text, font=text_font, fill=fill)
    return x, y, text_width, bbox[3] - bbox[1]


def draw_shield(draw):
    # Shield outline.
    shield = [(600, 112), (674, 138), (666, 218), (600, 274), (534, 218), (526, 138), (600, 112)]
    draw.line(shield, fill=BLACK, width=6, joint="curve")

    # Lock outline inside the shield.
    draw.arc((570, 148, 630, 208), 200, 340, fill=BLACK, width=5)
    draw.line((570, 178, 570, 212), fill=BLACK, width=5)
    draw.line((630, 178, 630, 212), fill=BLACK, width=5)
    draw.rectangle((558, 190, 642, 234), outline=BLACK, width=5)
    draw.line((600, 207, 600, 224), fill=BLACK, width=4)
    draw.ellipse((595, 202, 605, 212), outline=BLACK, width=3)


def draw_canal_and_gondola(draw):
    # Minimal bridge/canal arch.
    draw.arc((318, 182, 882, 394), 181, 359, fill=BLACK, width=6)
    draw.line((332, 289, 868, 289), fill=BLACK, width=4)
    draw.line((388, 314, 812, 314), fill=BLACK, width=3)

    # Water strokes.
    for x1, x2, y in [(386, 512, 360), (544, 656, 374), (705, 820, 360)]:
        draw.arc((x1, y - 24, x2, y + 24), 18, 162, fill=BLACK, width=3)

    # Abstract gondola silhouette made only from strokes.
    draw.arc((418, 292, 782, 420), 16, 164, fill=BLACK, width=7)
    draw.line((452, 352, 742, 352), fill=BLACK, width=5)
    draw.arc((394, 274, 500, 392), 285, 42, fill=BLACK, width=5)
    draw.arc((702, 274, 808, 392), 138, 255, fill=BLACK, width=5)
    draw.line((520, 332, 680, 332), fill=BLACK, width=4)
    draw.line((495, 282, 560, 350), fill=BLACK, width=4)
    draw.line((705, 282, 640, 350), fill=BLACK, width=4)


def draw_ai_sparks(draw):
    # Small abstract model/network marks, kept sparse and black-only.
    nodes = [(438, 132), (476, 166), (430, 204), (762, 132), (724, 166), (770, 204)]
    lines = [((438, 132), (476, 166)), ((476, 166), (430, 204)), ((762, 132), (724, 166)), ((724, 166), (770, 204))]
    for start, end in lines:
        draw.line((*start, *end), fill=BLACK, width=3)
    for x, y in nodes:
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), outline=BLACK, width=3)


def draw_tag(draw, label, y, label_font):
    bbox = draw.textbbox((0, 0), label, font=label_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    pad_x, pad_y = 26, 13
    box_width = text_width + pad_x * 2
    box_height = text_height + pad_y * 2
    x = (WIDTH - box_width) // 2
    draw.rectangle((x, y, x + box_width, y + box_height), outline=BLACK, width=3)
    draw.text((x + pad_x, y + pad_y - 2), label, font=label_font, fill=BLACK)


def main():
    if not OUTPUT_PATH.parent.exists():
        raise FileNotFoundError(f"Output directory does not exist: {OUTPUT_PATH.parent}")

    image = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(image)

    draw_ai_sparks(draw)
    draw_canal_and_gondola(draw)
    draw_shield(draw)

    title_font = font(84, bold=True)
    subtitle_font = font(32)
    tag_font = font(30, bold=True)

    centered_text(draw, 410, "Venice AI", title_font)
    centered_text(draw, 504, "Privacy-First AI — M Series A", subtitle_font)
    draw_tag(draw, "$2B Unicorn", 558, tag_font)

    image.save(OUTPUT_PATH, "PNG")

    absolute_path = str(OUTPUT_PATH.resolve())
    if not os.path.exists(absolute_path):
        raise FileNotFoundError(absolute_path)
    print(absolute_path)


if __name__ == "__main__":
    main()
