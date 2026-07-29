from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1200
HEIGHT = 630
BG = "white"
FG = "black"
OUTPUT = Path(
    "/Users/chajinwoo/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/블로그/markdown-blog/Knowledge Management System/_assets/kms-selection-guide.png"
)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def center_text(draw: ImageDraw.ImageDraw, text: str, font, y: int):
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (WIDTH - (bbox[2] - bbox[0])) / 2
    draw.text((x, y), text, fill=FG, font=font)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    heading_font = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 72)
    subtitle_font = load_font("/System/Library/Fonts/Supplemental/Arial.ttf", 36)
    node_font = load_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
    label_font = load_font("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
    caption_font = load_font("/System/Library/Fonts/Supplemental/Arial.ttf", 22)

    center_text(draw, "KMS Selection Guide", heading_font, 44)
    center_text(draw, "LLM Wiki to Ontology", subtitle_font, 130)

    x_center = 600
    node_radius = 9
    line_top = 240
    line_bottom = 470
    draw.line((x_center, line_top, x_center, line_bottom), fill=FG, width=3)

    steps = [
        ("Enterprise", "Ontology", 240),
        ("Organization", "GraphRAG", 317),
        ("Team", "Agent Memory", 394),
        ("Individual", "LLM Wiki", 470),
    ]

    for node_text, branch_text, y in steps:
        draw.ellipse(
            (x_center - node_radius, y - node_radius, x_center + node_radius, y + node_radius),
            outline=FG,
            fill=FG,
        )

        branch_x1 = x_center + 18
        branch_x2 = x_center + 115
        draw.line((branch_x1, y, branch_x2, y), fill=FG, width=2)

        node_bbox = draw.textbbox((0, 0), node_text, font=node_font)
        node_w = node_bbox[2] - node_bbox[0]
        draw.text((x_center - 40 - node_w, y - 22), node_text, fill=FG, font=node_font)

        draw.text((branch_x2 + 14, y - 14), branch_text, fill=FG, font=label_font)

    rule_y = 560
    draw.line((120, rule_y, 1080, rule_y), fill=FG, width=1)
    center_text(draw, "Choose by scale · complexity · update frequency", caption_font, 578)

    image.save(OUTPUT, format="PNG")


if __name__ == "__main__":
    main()
