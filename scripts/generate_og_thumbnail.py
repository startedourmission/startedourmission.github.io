from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


TARGET = Path(
    "/Users/chajinwoo/Vaults/AutoVault/markdown-blog/Knowledge Management System/_assets/karpathy-llm-wiki.png"
)
WIDTH = 1200
HEIGHT = 630
BG = "#FFFFFF"
FG = "#000000"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica.ttc",
                "/Library/Fonts/Arial Bold.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica.ttc",
                "/Library/Fonts/Arial.ttf",
            ]
        )

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue

    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size=size)
    except OSError:
        return ImageFont.load_default()


def centered_text(draw: ImageDraw.ImageDraw, y: int, text: str, font) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (WIDTH - text_w) / 2
    draw.text((x, y), text, fill=FG, font=font)


def draw_note(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    draw.rectangle((x, y, x + w, y + h), outline=FG, width=3)

    line_left = x + 26
    line_right = x + w - 26
    for offset in (32, 58, 84):
        draw.line((line_left, y + offset, line_right, y + offset), fill=FG, width=3)


def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    title_font = load_font(92, bold=True)
    subtitle_font = load_font(36, bold=False)

    centered_text(draw, 105, "LLM Wiki", title_font)
    centered_text(draw, 220, "Personal Knowledge as AI Context", subtitle_font)

    note_w = 280
    note_h = 140
    base_x = (WIDTH - note_w) // 2
    base_y = 360
    offsets = [(-38, 18), (0, 0), (38, 18)]

    for dx, dy in offsets:
        draw_note(draw, base_x + dx, base_y + dy, note_w, note_h)

    image.save(TARGET, format="PNG")
    print(TARGET)


if __name__ == "__main__":
    main()
