from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1200
HEIGHT = 630
BACKGROUND = "white"
FOREGROUND = "black"
OUTPUT = Path(
    "/Users/chajinwoo/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/블로그/markdown-blog/grid_Posts/_assets/openai-deployment-simulation.png"
)


def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica.ttc",
            ]
        )
    else:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica.ttc",
            ]
        )

    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue

    return ImageFont.load_default()


def draw_centered_text(draw: ImageDraw.ImageDraw, box, text, font):
    left, top, right, bottom = box
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=4, align="center")
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = left + (right - left - text_width) / 2
    y = top + (bottom - top - text_height) / 2
    draw.multiline_text((x, y), text, fill=FOREGROUND, font=font, spacing=4, align="center")


def draw_arrow(draw: ImageDraw.ImageDraw, start, end, width=3):
    draw.line([start, end], fill=FOREGROUND, width=width)
    arrow_size = 8
    ex, ey = end
    draw.line([(ex - arrow_size, ey - arrow_size), (ex, ey)], fill=FOREGROUND, width=width)
    draw.line([(ex - arrow_size, ey + arrow_size), (ex, ey)], fill=FOREGROUND, width=width)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    title_font = load_font(54, bold=True)
    subtitle_font = load_font(24, bold=False)
    box_font = load_font(22, bold=False)
    small_font = load_font(18, bold=False)

    draw.text((84, 72), "Deployment Simulation", fill=FOREGROUND, font=title_font)
    draw.text((88, 142), "OpenAI Evaluation Methodology", fill=FOREGROUND, font=subtitle_font)

    diagram_top = 255
    box_width = 205
    box_height = 88
    gap = 28
    start_x = 70

    labels = [
        "Real\nConversations",
        "Replay",
        "Candidate\nModel",
        "Behavior\nDistribution",
    ]

    boxes = []
    for index, label in enumerate(labels):
        left = start_x + index * (box_width + gap)
        top = diagram_top
        right = left + box_width
        bottom = top + box_height
        boxes.append((left, top, right, bottom))
        draw.rounded_rectangle((left, top, right, bottom), radius=14, outline=FOREGROUND, width=3)
        draw_centered_text(draw, (left, top, right, bottom), label, box_font)

    for first, second in zip(boxes, boxes[1:]):
        start = (first[2] + 6, (first[1] + first[3]) // 2)
        end = (second[0] - 10, (second[1] + second[3]) // 2)
        draw_arrow(draw, start, end)

    draw.text((84, HEIGHT - 52), "OpenAI", fill=FOREGROUND, font=small_font)

    footer_text = "evaluation · replay · alignment"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=small_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text((WIDTH - 84 - footer_width, HEIGHT - 52), footer_text, fill=FOREGROUND, font=small_font)

    image.save(OUTPUT, format="PNG")
    print(OUTPUT)
    print(OUTPUT.stat().st_size)


if __name__ == "__main__":
    main()
