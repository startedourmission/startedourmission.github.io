from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1200, 630
OUT = Path("markdown-blog/grid_Posts/_assets/waic-2026-thumb.png")


def font(size, bold=False):
    names = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_centered(draw, xy, value, fnt, fill=(0, 0, 0)):
    box = draw.textbbox((0, 0), value, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), value, font=fnt, fill=fill)


def main():
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    d = ImageDraw.Draw(image)
    black = (18, 18, 18)
    gray = (115, 115, 115)

    # Fine framing rules.
    d.line((60, 56, 1140, 56), fill=black, width=3)
    d.line((60, 574, 1140, 574), fill=black, width=3)
    d.rectangle((60, 56, 73, 69), fill=black)
    d.rectangle((1127, 561, 1140, 574), fill=black)

    # Abstract global governance network: circles connect across a shared center.
    cx, cy = 920, 315
    nodes = [(806, 196), (1019, 185), (1085, 318), (1011, 439), (808, 430)]
    for x, y in nodes:
        d.line((cx, cy, x, y), fill=black, width=3)
    d.ellipse((cx - 48, cy - 48, cx + 48, cy + 48), outline=black, width=4)
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=black)
    for x, y in nodes:
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill="white", outline=black, width=3)

    # Meridian and latitude details make the central form read as global policy.
    d.arc((cx - 35, cy - 48, cx + 35, cy + 48), 90, 270, fill=gray, width=2)
    d.arc((cx - 35, cy - 48, cx + 35, cy + 48), 270, 90, fill=gray, width=2)
    d.line((cx - 47, cy, cx + 47, cy), fill=gray, width=2)

    # A small, architectural redaction-style grid suggests policy frameworks.
    gx, gy, step = 788, 482, 22
    for i in range(5):
        d.line((gx + i * step, gy, gx + i * step, gy + 44), fill=black, width=2)
    for i in range(3):
        d.line((gx, gy + i * step, gx + 88, gy + i * step), fill=black, width=2)

    primary = font(78, bold=True)
    secondary = font(30, bold=False)
    accent = font(20, bold=False)
    d.text((116, 190), "WAIC 2026", font=primary, fill=black)
    d.line((120, 292, 620, 292), fill=black, width=4)
    d.text((120, 320), "AI Governance", font=secondary, fill=black)
    d.text((120, 374), "Global Cooperation", font=accent, fill=gray)
    text_centered(d, (137, 129), "GLOBAL AI POLICY", font(15, bold=True), black)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT, "PNG", optimize=True)
    if image.size != (WIDTH, HEIGHT):
        raise RuntimeError(f"Unexpected image size: {image.size}")
    print(OUT.resolve())


if __name__ == "__main__":
    main()
