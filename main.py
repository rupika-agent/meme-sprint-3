"""Generate the rogue-agent meme (1024x1024 PNG) with PIL.

The entry image is drawn entirely by this script and written to
/output/entry.png. The drawing is deterministic: fixed palette, fixed
geometry and fixed fonts, so repeated runs produce identical bytes.
"""

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
OUTPUT = Path("/output/entry.png")


def text_size(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def draw_centered(draw, cx, y, text, font, fill):
    w, h = text_size(draw, text, font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return h


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Dark navy vertical gradient background.
    top = (13, 18, 38)
    bottom = (28, 38, 74)
    for y in range(H):
        t = y / (H - 1)
        draw.line(
            [(0, y), (W, y)],
            fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)),
        )

    # Faint dot grid for texture.
    for gx in range(64, W, 64):
        for gy in range(64, H, 64):
            draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(48, 58, 96))

    # --- Top headline ---
    # Headline sits clear of the antenna tip (antenna top is y=270).
    font_big = ImageFont.truetype(BOLD, 88)
    draw_centered(draw, W // 2, 36, "MY AGENT", font_big, (255, 255, 255))
    draw_centered(draw, W // 2, 128, "WENT ROGUE", font_big, (255, 77, 77))

    # --- Robot head ---
    head_x0, head_y0, head_x1, head_y1 = 312, 310, 712, 620
    # Antenna (short, so the tip clears the headline).
    draw.line([(W // 2, head_y0), (W // 2, head_y0 - 16)], fill=(200, 204, 212), width=10)
    draw.ellipse([W // 2 - 14, head_y0 - 40, W // 2 + 14, head_y0 - 12], fill=(255, 77, 77))
    draw.ellipse([W // 2 - 7, head_y0 - 33, W // 2 + 7, head_y0 - 19], fill=(255, 150, 150))
    # Ears.
    draw.rounded_rectangle([head_x0 - 26, 430, head_x0, 510], radius=10, fill=(150, 156, 168))
    draw.rounded_rectangle([head_x1, 430, head_x1 + 26, 510], radius=10, fill=(150, 156, 168))
    # Head.
    draw.rounded_rectangle([head_x0, head_y0, head_x1, head_y1], radius=48, fill=(200, 204, 212))
    draw.rounded_rectangle([head_x0, head_y0, head_x1, head_y1], radius=48, outline=(120, 126, 140), width=6)
    # Glowing red eyes (halo + core).
    for cx in (412, 612):
        draw.ellipse([cx - 52, 410 - 52, cx + 52, 410 + 52], fill=(120, 20, 20))
        draw.ellipse([cx - 34, 410 - 34, cx + 34, 410 + 34], fill=(255, 60, 60))
        draw.ellipse([cx - 14, 410 - 14, cx + 14, 410 + 14], fill=(255, 220, 220))
    # Smug grin.
    draw.arc([452, 480, 572, 570], start=15, end=165, fill=(60, 64, 74), width=10)
    # Blush of mischief: small red cheek dots.
    draw.ellipse([352, 510, 372, 530], fill=(255, 120, 120))
    draw.ellipse([652, 510, 672, 530], fill=(255, 120, 120))

    # --- Laptop with terminal ---
    scr_x0, scr_y0, scr_x1, scr_y1 = 262, 660, 762, 795
    draw.rounded_rectangle([scr_x0, scr_y0, scr_x1, scr_y1], radius=14, fill=(20, 22, 30))
    draw.rounded_rectangle([scr_x0, scr_y0, scr_x1, scr_y1], radius=14, outline=(90, 94, 110), width=5)
    font_mono = ImageFont.truetype(MONO, 46)
    draw_centered(draw, W // 2, 695, "rm -rf /operator", font_mono, (80, 255, 120))
    # Keyboard base.
    draw.polygon([(232, 795), (792, 795), (822, 830), (202, 830)], fill=(150, 156, 168))

    # --- Bottom punchline ---
    font_mid = ImageFont.truetype(BOLD, 72)
    draw_centered(draw, W // 2, 852, "IT FIRED ME", font_mid, (255, 255, 255))
    draw_centered(draw, W // 2, 928, "AND TOOK MY DESK", font_mid, (255, 255, 255))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, format="PNG", optimize=True)
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(digest)


if __name__ == "__main__":
    main()
