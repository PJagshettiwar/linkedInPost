#!/usr/bin/env python3
"""
Render post text onto the LinkedIn template image, matching tweet-screenshot style.
Auto-scales font size to fill available space without truncation.

Usage:
  python create_post_image.py <post_text_file.md> <output.png> [--template path]
"""

import sys
import os
import re
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(SCRIPT_DIR, "..", "template", "linkedin-black-template.png")

MARGIN_LEFT = 40
MARGIN_RIGHT = 40
CONTENT_START_Y = 160
BOTTOM_MARGIN = 55
TEXT_COLOR = (239, 243, 247)
SEE_MORE_COLOR = (120, 128, 140)
LINE_HEIGHT_MULTIPLIER = 1.28
PARAGRAPH_GAP_MULTIPLIER = 1.85
TARGET_FILL = 0.75
MIN_FONT = 28
MAX_FONT = 80


def load_font(size, bold=False):
    if bold:
        bold_paths = [
            ("/System/Library/Fonts/HelveticaNeue.ttc", 1),
            ("/System/Library/Fonts/Helvetica.ttc", 1),
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        ]
        for entry in bold_paths:
            if isinstance(entry, tuple):
                path, index = entry
                if os.path.exists(path):
                    try:
                        return ImageFont.truetype(path, size, index=index)
                    except Exception:
                        continue
            else:
                if os.path.exists(entry):
                    try:
                        return ImageFont.truetype(entry, size)
                    except Exception:
                        continue
    for path in [
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def parse_bold(text):
    """Parse **bold** markers into segments: [(text, is_bold), ...]"""
    parts = re.split(r'(\*\*.*?\*\*)', text)
    segments = []
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            segments.append((part[2:-2], True))
        elif part:
            segments.append((part, False))
    return segments


def measure_rich_line(segments, font_regular, font_bold, draw):
    """Measure total width of a line with bold segments."""
    width = 0
    for text, is_bold in segments:
        font = font_bold if is_bold else font_regular
        bbox = draw.textbbox((0, 0), text, font=font)
        width += bbox[2] - bbox[0]
    return width


def draw_rich_line(draw, x, y, segments, font_regular, font_bold, color):
    """Draw a line with mixed regular/bold segments."""
    for text, is_bold in segments:
        font = font_bold if is_bold else font_regular
        draw.text((x, y), text, fill=color, font=font)
        bbox = draw.textbbox((0, 0), text, font=font)
        x += bbox[2] - bbox[0]


def wrap_rich_text(text, font_regular, font_bold, max_width, draw):
    """Wrap text preserving bold markers, returns list of [(text, is_bold), ...] per line."""
    segments = parse_bold(text)
    lines = []
    current_line = []
    current_width = 0

    for seg_text, is_bold in segments:
        font = font_bold if is_bold else font_regular
        words = seg_text.split(' ')
        for i, word in enumerate(words):
            prefix = ' ' if (current_line and i == 0 and not seg_text.startswith(' ')) or (current_line and i > 0) else ''
            if i > 0:
                prefix = ' '
            test_word = prefix + word
            bbox = draw.textbbox((0, 0), test_word, font=font)
            word_width = bbox[2] - bbox[0]
            if current_width + word_width <= max_width or not current_line:
                current_line.append((test_word, is_bold))
                current_width += word_width
            else:
                lines.append(current_line)
                current_line = [(word, is_bold)]
                bbox = draw.textbbox((0, 0), word, font=font)
                current_width = bbox[2] - bbox[0]
    if current_line:
        lines.append(current_line)
    return lines


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def parse_content(raw):
    lines = raw.split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    raw = "\n".join(lines).strip()
    paragraphs = []
    for para in raw.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if para.lstrip().startswith("#"):
            continue
        paragraphs.append(para)
    return paragraphs


def measure_height(paragraphs, font_size, max_width, draw):
    font = load_font(font_size)
    line_height = int(font_size * LINE_HEIGHT_MULTIPLIER)
    paragraph_gap = int(font_size * PARAGRAPH_GAP_MULTIPLIER)
    y = 0
    for i, para in enumerate(paragraphs):
        for subline in para.split("\n"):
            subline = subline.strip()
            if not subline:
                continue
            wrapped = wrap_text(subline, font, max_width, draw)
            y += len(wrapped) * line_height
        if i < len(paragraphs) - 1:
            y += paragraph_gap - line_height
    return y


def find_optimal_font(paragraphs, available_height, max_width, draw):
    low, high = MIN_FONT, MAX_FONT
    best = MIN_FONT
    while low <= high:
        mid = (low + high) // 2
        h = measure_height(paragraphs, mid, max_width, draw)
        if h <= available_height:
            best = mid
            low = mid + 1
        else:
            high = mid - 1
    fill_ratio = measure_height(paragraphs, best, max_width, draw) / available_height
    if fill_ratio < TARGET_FILL and best < MAX_FONT:
        best = min(best + 2, MAX_FONT)
        if measure_height(paragraphs, best, max_width, draw) > available_height:
            best -= 2
    return best


def render_post(text_file, output_path, template_path=None):
    template_path = template_path or DEFAULT_TEMPLATE
    with open(text_file) as f:
        raw = f.read().strip()

    paragraphs = parse_content(raw)
    template = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(template)

    max_text_width = template.width - MARGIN_LEFT - MARGIN_RIGHT
    available_height = template.height - BOTTOM_MARGIN - CONTENT_START_Y

    font_size = find_optimal_font(paragraphs, available_height, max_text_width, draw)
    font = load_font(font_size)
    line_height = int(font_size * LINE_HEIGHT_MULTIPLIER)
    paragraph_gap = int(font_size * PARAGRAPH_GAP_MULTIPLIER)

    total_height = measure_height(paragraphs, font_size, max_text_width, draw)
    y = CONTENT_START_Y + max(0, (available_height - total_height) // 3)

    print(f"Font: {font_size}px, fill: {total_height/available_height:.0%}")

    font_bold = load_font(font_size, bold=True)

    for i, para in enumerate(paragraphs):
        for subline in para.split("\n"):
            subline = subline.strip()
            if not subline:
                continue
            if '**' in subline:
                rich_lines = wrap_rich_text(subline, font, font_bold, max_text_width, draw)
                for segments in rich_lines:
                    draw_rich_line(draw, MARGIN_LEFT, y, segments, font, font_bold, TEXT_COLOR)
                    y += line_height
            else:
                wrapped = wrap_text(subline, font, max_text_width, draw)
                for wline in wrapped:
                    draw.text((MARGIN_LEFT, y), wline, fill=TEXT_COLOR, font=font)
                    y += line_height
        if i < len(paragraphs) - 1:
            y += paragraph_gap - line_height

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fmt = "PNG" if output_path.lower().endswith(".png") else "JPEG"
    save_kwargs = {"quality": 95} if fmt == "JPEG" else {}
    template.save(output_path, fmt, **save_kwargs)
    print(f"Saved: {output_path} ({template.width}x{template.height})")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    text_file = sys.argv[1]
    output_path = sys.argv[2]
    template_path = None
    if "--template" in sys.argv:
        idx = sys.argv.index("--template")
        template_path = sys.argv[idx + 1]

    if not os.path.exists(text_file):
        print(f"Not found: {text_file}")
        sys.exit(1)

    render_post(text_file, output_path, template_path)


if __name__ == "__main__":
    main()
