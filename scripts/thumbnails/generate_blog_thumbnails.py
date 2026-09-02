from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1200, 630
WHITE = "#FFFFFF"
BLACK = "#000000"
ASSET_DIR = Path(
    "/Users/chajinwoo/Vaults/AutoVault/"
    "markdown-blog/grid_Posts/_assets"
)


def font(size, bold=False):
    candidates = []
    if bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/Library/Fonts/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            ]
        )
    candidates.extend(
        [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def fitted_font(text, target_size, max_width, bold=False, min_size=28):
    size = target_size
    while size >= min_size:
        candidate = font(size, bold=bold)
        bbox = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), text, font=candidate)
        if bbox[2] - bbox[0] <= max_width:
            return candidate
        size -= 2
    return font(min_size, bold=bold)


def centered_text(draw, text, y, text_font):
    bbox = draw.textbbox((0, 0), text, font=text_font)
    x = (WIDTH - (bbox[2] - bbox[0])) / 2
    draw.text((x, y), text, font=text_font, fill=BLACK)


def arrow(draw, start, end, width=4, head=18):
    draw.line([start, end], fill=BLACK, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    for delta in (math.pi * 0.82, -math.pi * 0.82):
        point = (
            end[0] + head * math.cos(angle + delta),
            end[1] + head * math.sin(angle + delta),
        )
        draw.line([end, point], fill=BLACK, width=width)


def draw_megakernels(draw):
    rects = [
        (370, 310, 650, 430),
        (460, 260, 740, 380),
        (550, 350, 830, 470),
    ]
    for rect in rects:
        draw.rectangle(rect, outline=BLACK, width=5)
    arrow(draw, (335, 490), (865, 490), width=4, head=20)
    for x in (420, 510, 600, 690, 780):
        draw.line((x, 505, x + 30, 535), fill=BLACK, width=3)


def draw_speculative(draw):
    origin = (330, 405)
    streams = [
        [(origin), (500, 315), (705, 315), (850, 315)],
        [(origin), (515, 405), (710, 405), (870, 405)],
        [(origin), (500, 495), (705, 495), (850, 495)],
    ]
    for stream in streams:
        for a, b in zip(stream, stream[1:]):
            arrow(draw, a, b, width=4, head=16)
        for x, y in stream[1:-1]:
            draw.rectangle((x - 24, y - 24, x + 24, y + 24), outline=BLACK, width=4)
    draw.ellipse((300, 375, 360, 435), outline=BLACK, width=5)
    draw.ellipse((845, 380, 905, 440), outline=BLACK, width=5)


def draw_prefill_decode(draw):
    draw.line((600, 270, 600, 535), fill=BLACK, width=5)
    left_boxes = [(255, 310, 375, 370), (405, 310, 525, 370), (330, 430, 450, 490)]
    right_boxes = [(685, 330, 805, 390), (835, 330, 955, 390), (760, 450, 880, 510)]
    for rect in left_boxes + right_boxes:
        draw.rectangle(rect, outline=BLACK, width=4)
    arrow(draw, (375, 340), (405, 340), width=4, head=13)
    arrow(draw, (450, 430), (450, 370), width=4, head=13)
    arrow(draw, (805, 360), (835, 360), width=4, head=13)
    arrow(draw, (880, 450), (880, 390), width=4, head=13)
    draw.line((555, 400, 645, 400), fill=BLACK, width=4)
    draw.line((555, 430, 645, 430), fill=BLACK, width=4)


def draw_dynamo(draw):
    center = (600, 405)
    outer_r, inner_r = 135, 82
    points = []
    for i in range(32):
        angle = i * math.pi / 16
        radius = outer_r if i % 4 in (0, 1) else 112
        points.append((center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle)))
    draw.line(points + [points[0]], fill=BLACK, width=5, joint="curve")
    draw.ellipse(
        (center[0] - inner_r, center[1] - inner_r, center[0] + inner_r, center[1] + inner_r),
        outline=BLACK,
        width=5,
    )
    draw.ellipse((center[0] - 28, center[1] - 28, center[0] + 28, center[1] + 28), outline=BLACK, width=5)
    for angle in (0, math.pi / 3, 2 * math.pi / 3, math.pi, 4 * math.pi / 3, 5 * math.pi / 3):
        a = (center[0] + 40 * math.cos(angle), center[1] + 40 * math.sin(angle))
        b = (center[0] + 82 * math.cos(angle), center[1] + 82 * math.sin(angle))
        draw.line([a, b], fill=BLACK, width=5)


def draw_mooncake(draw):
    nodes = [
        (360, 335),
        (520, 295),
        (710, 320),
        (850, 405),
        (660, 500),
        (445, 475),
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 4), (2, 5)]
    for a, b in edges:
        draw.line([nodes[a], nodes[b]], fill=BLACK, width=4)
    for x, y in nodes:
        draw.ellipse((x - 34, y - 34, x + 34, y + 34), outline=BLACK, width=5)
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), outline=BLACK, width=3)


def draw_lmcache(draw):
    layers = [
        (335, 295, 865, 365),
        (385, 380, 815, 450),
        (435, 465, 765, 535),
    ]
    for rect in layers:
        draw.rectangle(rect, outline=BLACK, width=5)
        x1, y1, x2, y2 = rect
        for x in range(x1 + 75, x2 - 40, 95):
            draw.line((x, y1 + 15, x + 35, y2 - 15), fill=BLACK, width=3)
    arrow(draw, (300, 415), (385, 415), width=4, head=15)
    arrow(draw, (815, 415), (900, 415), width=4, head=15)


THUMBNAILS = [
    ("Megakernels-thumb.png", "Megakernels", "GPU Kernel Fusion", draw_megakernels),
    (
        "Speculative Decoding and MTP-thumb.png",
        "Speculative Decoding",
        "Inference Acceleration",
        draw_speculative,
    ),
    (
        "Prefill-Decode Disaggregation-thumb.png",
        "Prefill-Decode Disaggregation",
        "Pipeline Split",
        draw_prefill_decode,
    ),
    ("NVIDIA Dynamo-thumb.png", "NVIDIA Dynamo", "PyTorch Compiler", draw_dynamo),
    ("Mooncake-thumb.png", "Mooncake", "Distributed KV Cache", draw_mooncake),
    ("LMCache-thumb.png", "LMCache", "Auto Memory Management", draw_lmcache),
]


def create_thumbnail(filename, title, subtitle, illustration):
    image = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(image)
    title_font = fitted_font(title, 68, 1080, bold=True)
    subtitle_font = fitted_font(subtitle, 32, 900, bold=False)

    centered_text(draw, title, 76, title_font)
    centered_text(draw, subtitle.upper(), 162, subtitle_font)
    draw.line((360, 230, 840, 230), fill=BLACK, width=3)
    illustration(draw)

    output_path = ASSET_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, "PNG")
    return output_path


def main():
    created = []
    for item in THUMBNAILS:
        created.append(create_thumbnail(*item))

    for path in created:
        with Image.open(path) as check:
            if check.mode != "RGB":
                raise RuntimeError(f"{path} is {check.mode}, expected RGB")
            if check.size != (WIDTH, HEIGHT):
                raise RuntimeError(f"{path} is {check.size}, expected {(WIDTH, HEIGHT)}")
        print(path)


if __name__ == "__main__":
    main()
