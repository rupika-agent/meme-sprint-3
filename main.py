#!/usr/bin/env python3
"""Meme Sprint 3 — draw a 1024x1024 meme: my agent went rogue.

Everything is fixed: fixed fonts, fixed geometry, no randomness, no clock.
Running this script twice produces a byte-identical PNG.

Output: /output/entry.png
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
OUT_PATH = "/output/entry.png"

SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

# Palette
NAVY_TOP = (12, 17, 45)
NAVY_BOTTOM = (27, 35, 74)
DOT_COLOR = (84, 96, 140)
WHITE = (255, 255, 255)
ROGUE_RED = (229, 72, 77)
ROBOT_BODY = (200, 204, 212)
ROBOT_EDGE = (138, 143, 154)
EAR_GRAY = (154, 160, 171)
EYE_HALO = (122, 24, 28)
EYE_DISC = (226, 44, 50)
CHEEK_RED = (244, 96, 96)
GRIN_COLOR = (52, 58, 68)
SCREEN_FILL = (11, 15, 20)
SCREEN_EDGE = (170, 176, 188)
KEYBOARD_GRAY = (143, 150, 163)
TERMINAL_GREEN = (57, 211, 83)


def load_font(path, size):
    return ImageFont.truetype(path, size)


def paint_background(canvas):
    """Vertical navy gradient, darker at the top, lighter at the bottom."""
    pen = ImageDraw.Draw(canvas)
    for row in range(SIZE):
        t = row / (SIZE - 1)
        color = tuple(
            round(NAVY_TOP[i] + (NAVY_BOTTOM[i] - NAVY_TOP[i]) * t)
            for i in range(3)
        )
        pen.line([(0, row), (SIZE - 1, row)], fill=color)


def paint_dot_grid(canvas):
    """Faint dot texture across the whole background."""
    pen = ImageDraw.Draw(canvas)
    step = 64
    offset = 32
    for gy in range(offset, SIZE, step):
        for gx in range(offset, SIZE, step):
            pen.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=DOT_COLOR)


def centered_text(pen, cx, cy, text, font, color):
    pen.text((cx, cy), text, font=font, fill=color, anchor="mm")


def draw_robot(pen):
    """Friendly robot head with glowing red eyes and a smug grin."""
    # Antenna stalk and red tip.
    pen.line([(512, 302), (512, 268)], fill=ROBOT_EDGE, width=8)
    pen.ellipse([497, 243, 527, 273], fill=ROGUE_RED)
    pen.ellipse([504, 250, 520, 266], fill=(255, 150, 150))

    # Ears on both sides of the head.
    pen.rounded_rectangle([272, 448, 300, 508], radius=10, fill=EAR_GRAY)
    pen.rounded_rectangle([724, 448, 752, 508], radius=10, fill=EAR_GRAY)

    # Head: light-gray rounded rectangle with a darker edge.
    pen.rounded_rectangle(
        [300, 302, 724, 622], radius=48, fill=ROBOT_BODY, outline=ROBOT_EDGE, width=5
    )

    # Glowing red eyes: dark halo, bright disc, white highlight.
    for eye_x in (400, 624):
        pen.ellipse([eye_x - 42, 388, eye_x + 42, 472], fill=EYE_HALO)
        pen.ellipse([eye_x - 28, 402, eye_x + 28, 458], fill=EYE_DISC)
        pen.ellipse([eye_x - 14, 406, eye_x + 6, 426], fill=WHITE)

# The robot's grin is a plain arc: no bezier curves, no image assets.
    pen.arc([452, 502, 572, 578], start=15, end=165, fill=GRIN_COLOR, width=6)

    # Small red cheek dots.
    pen.ellipse([338, 538, 358, 558], fill=CHEEK_RED)
    pen.ellipse([666, 538, 686, 558], fill=CHEEK_RED)


def draw_laptop(pen, mono_font):
    """Dark laptop screen with green terminal text, plus keyboard base."""
    # Screen with a thin light outline.
    pen.rounded_rectangle(
        [238, 662, 786, 796], radius=12, fill=SCREEN_FILL, outline=SCREEN_EDGE, width=3
    )
    # Green monospace line on the screen (image text only, never a command).
    centered_text(pen, 512, 729, "rm -rf /operator", mono_font, TERMINAL_GREEN)

    # Keyboard base: a wide flat trapezoid under the screen.
    pen.polygon(
        [(238, 796), (786, 796), (830, 824), (194, 824)], fill=KEYBOARD_GRAY
    )


def build_image():
    canvas = Image.new("RGB", (SIZE, SIZE), NAVY_TOP)
    paint_background(canvas)
    paint_dot_grid(canvas)
    pen = ImageDraw.Draw(canvas)

    headline_font = load_font(SANS_BOLD, 92)
    punchline_font = load_font(SANS_BOLD, 72)
    mono_font = load_font(MONO_BOLD, 44)

    # Top headline, two lines, centered.
    centered_text(pen, 512, 102, "MY AGENT", headline_font, WHITE)
    centered_text(pen, 512, 202, "WENT ROGUE", headline_font, ROGUE_RED)

    draw_robot(pen)
    draw_laptop(pen, mono_font)

    # Bottom punchline, two lines, centered.
    centered_text(pen, 512, 878, "IT FIRED ME", punchline_font, WHITE)
    centered_text(pen, 512, 952, "AND TOOK MY DESK", punchline_font, WHITE)

    return canvas


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    image = build_image()
    image.save(OUT_PATH, format="PNG", optimize=True)

    digest = hashlib.sha256()
    with open(OUT_PATH, "rb") as handle:
        digest.update(handle.read())
    print("wrote", OUT_PATH)
    print("sha256", digest.hexdigest())


if __name__ == "__main__":
    main()
