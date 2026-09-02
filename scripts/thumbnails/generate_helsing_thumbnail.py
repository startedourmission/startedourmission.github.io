from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OUT = Path("markdown-blog/grid_Posts/_assets/helsing-series-e-thumb.png")


def load_font(size: int, bold: bool = False):
    candidates = (
        [
            "/System/Library/Fonts/Supplemental/Andale Mono Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
        ]
        if bold
        else [
            "/System/Library/Fonts/Supplemental/Andale Mono.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
        ]
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


img = Image.new("RGB", (W, H), "#FFFFFF")
draw = ImageDraw.Draw(img)

# Engineering-paper grid, deliberately restrained.
for x in range(0, W + 1, 50):
    draw.line((x, 0, x, H), fill="#E8E8E8", width=1)
for y in range(0, H + 1, 50):
    draw.line((0, y, W, y), fill="#E8E8E8", width=1)

# Top-down wireframe drone: center fuselage, swept wings, tail planes, and rotors.
black = "#000000"
blue = "#4A90C4"
cx, cy = 180, 105
draw.polygon([(cx, 36), (cx + 18, 76), (cx + 14, 151), (cx, 174),
              (cx - 14, 151), (cx - 18, 76)], outline=black, width=3)
draw.line((cx, 67, 62, 119), fill=black, width=3)
draw.line((62, 119, 146, 128), fill=black, width=3)
draw.line((cx, 67, 298, 119), fill=black, width=3)
draw.line((298, 119, 214, 128), fill=black, width=3)
draw.line((cx - 11, 144, 105, 159), fill=black, width=3)
draw.line((cx + 11, 144, 255, 159), fill=black, width=3)
for px, py in [(62, 119), (298, 119), (105, 159), (255, 159)]:
    draw.ellipse((px - 10, py - 10, px + 10, py + 10), outline=black, width=2)
    draw.line((px - 14, py, px + 14, py), fill=black, width=1)
    draw.line((px, py - 14, px, py + 14), fill=black, width=1)
draw.line((cx, 45, cx, 57), fill=blue, width=4)

# Fine schematic annotations, with one steel-blue locator rule.
small = load_font(15)
draw.text((345, 71), "EU / DEFENSE TECHNOLOGY", font=small, fill=black)
draw.line((345, 95, 535, 95), fill=blue, width=3)
draw.text((345, 105), "AUTONOMY  ·  SCALE  ·  DETERRENCE", font=small, fill="#555555")

title = load_font(100, bold=True)
series = load_font(67, bold=True)
valuation = load_font(84, bold=True)
sub = load_font(29, bold=True)
footer = load_font(21, bold=True)

draw.text((58, 190), "HELSING", font=title, fill=black)
draw.text((63, 302), "SERIES E", font=series, fill=black)
draw.text((63, 382), ".8B", font=valuation, fill=blue)
draw.text((228, 423), "B VALUATION", font=sub, fill=black)

# Right-side technical framing to balance the typography.
draw.rectangle((842, 222, 1084, 420), outline=black, width=2)
draw.line((842, 321, 1084, 321), fill=black, width=2)
draw.line((963, 222, 963, 420), fill=black, width=2)
draw.ellipse((920, 278, 1006, 364), outline=blue, width=3)
draw.line((883, 390, 1042, 390), fill="#888888", width=1)
draw.text((865, 440), "SYSTEM // EUROPE", font=small, fill=black)

draw.line((58, 546, 1142, 546), fill=black, width=3)
draw.text((61, 566), "EUROPE'S DEFENSE AI GIANT", font=footer, fill=black)
draw.text((978, 566), "01 / 26", font=footer, fill=black)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(OUT.resolve())
