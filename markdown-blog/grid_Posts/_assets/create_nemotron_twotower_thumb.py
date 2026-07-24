from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path(
    "/Users/chajinwoo/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/"
    "블로그/markdown-blog/grid_Posts/_assets/nemotron-twotower-thumb.png"
)
WIDTH, HEIGHT = 1200, 630
BLACK, WHITE = "#000000", "#FFFFFF"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/ArialHB.ttc"]
        if bold
        else ["/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"]
    )
    for candidate in candidates:
        if Path(candidate).exists():
            try:
                return ImageFont.truetype(candidate, size)
            except OSError:
                pass
    return ImageFont.load_default()


def centered_text(draw: ImageDraw.ImageDraw, y: int, text: str, typeface, **kwargs) -> None:
    box = draw.textbbox((0, 0), text, font=typeface, **kwargs)
    draw.text(((WIDTH - (box[2] - box[0])) / 2, y), text, font=typeface, fill=BLACK, **kwargs)


def arrowhead(draw: ImageDraw.ImageDraw, x: int, y: int, direction: int) -> None:
    # direction: 1 points right, -1 points left
    length, half_height = 18, 10
    draw.line((x, y, x - direction * length, y - half_height), fill=BLACK, width=4)
    draw.line((x, y, x - direction * length, y + half_height), fill=BLACK, width=4)


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(image)

    title = font(78, bold=True)
    tower_label = font(33, bold=True)
    sub_label = font(23)
    bridge_label = font(23, bold=True)
    speed_label = font(31, bold=True)
    subtitle = font(28)

    draw.rectangle((10, 10, WIDTH - 10, HEIGHT - 10), outline=BLACK, width=4)
    centered_text(draw, 48, "TwoTower", title)

    left = (260, 195, 500, 455)
    right = (700, 195, 940, 455)
    draw.rectangle(left, outline=BLACK, width=5)
    draw.rectangle(right, outline=BLACK, width=5)

    # Tower labels sit inside the white outlined structures.
    for y, text, face in ((260, "Diffusion Tower", tower_label), (304, "Trainable", sub_label)):
        box = draw.textbbox((0, 0), text, font=face)
        draw.text((820 - (box[2] - box[0]) / 2, y), text, font=face, fill=BLACK)
    for y, text, face in ((260, "AR Tower", tower_label), (304, "Frozen", sub_label)):
        box = draw.textbbox((0, 0), text, font=face)
        draw.text((380 - (box[2] - box[0]) / 2, y), text, font=face, fill=BLACK)

    connector_y = 385
    draw.line((520, connector_y, 680, connector_y), fill=BLACK, width=4)
    arrowhead(draw, 520, connector_y, -1)
    arrowhead(draw, 680, connector_y, 1)
    label_box = draw.textbbox((0, 0), "Cross-Attention", font=bridge_label)
    label_w = label_box[2] - label_box[0]
    draw.rectangle((600 - label_w / 2 - 7, 345, 600 + label_w / 2 + 7, 375), fill=WHITE)
    draw.text((600 - label_w / 2, 347), "Cross-Attention", font=bridge_label, fill=BLACK)

    centered_text(draw, 475, "2.42x Faster", speed_label)
    # Hyphen is intentionally used instead of an em or en dash.
    centered_text(draw, 568, "AR context + Diffusion denoiser - NVIDIA Nemotron", subtitle)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG")
    with Image.open(OUTPUT) as verified:
        verified.verify()
    print(OUTPUT)


if __name__ == "__main__":
    main()
