"""Generate placeholder ModHub icon assets (ModIcon, StoreIcon, BrandIcon).

Produces source PNGs under icons/ and BC1/DXT1-compressed DDS files under
FS25_UK_Commodity_Prices/icons/modhub/, per the spec in docs/PUBLISHING.md.

These are simple procedurally-drawn placeholders, not final branding. Rerun
this script after editing the drawing code below to regenerate all assets.

Usage: python scripts/generate_icons.py
"""

import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
PNG_DIR = REPO_ROOT / "icons"
DDS_DIR = REPO_ROOT / "FS25_UK_Commodity_Prices" / "icons" / "modhub"

# UK flag palette (Pantone 280C / 186C approximations).
NAVY = (12, 33, 72)
RED = (200, 16, 46)
WHITE = (255, 255, 255)
GOLD = (218, 165, 32)
MATTE_BG = (28, 30, 33)

FONT_BOLD = Path("C:/Windows/Fonts/segoeuib.ttf")


def load_font(size):
    if FONT_BOLD.exists():
        return ImageFont.truetype(str(FONT_BOLD), size)
    return ImageFont.load_default()


def draw_flag_band(draw, x0, y0, x1, y1):
    """Horizontal navy/white/red stripe band, evoking the Union flag palette."""
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    height = y1 - y0
    third = height / 3
    draw.rectangle([x0, y0, x1, int(y0 + third)], fill=NAVY)
    draw.rectangle([x0, int(y0 + third), x1, int(y0 + 2 * third)], fill=WHITE)
    draw.rectangle([x0, int(y0 + 2 * third), x1, y1], fill=RED)


def draw_wheat_coin(draw, cx, cy, radius):
    """A coin-like disc with a wheat-sheaf glyph, standing in for 'commodity price'."""
    cx, cy, radius = int(cx), int(cy), int(radius)
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=GOLD,
        outline=WHITE,
        width=max(2, radius // 20),
    )
    stem_bottom = int(cy + radius * 0.55)
    stem_top = int(cy - radius * 0.55)
    draw.line([cx, stem_bottom, cx, stem_top], fill=NAVY, width=max(3, radius // 12))
    n_leaves = 4
    for i in range(n_leaves):
        t = i / (n_leaves - 1)
        ly = int(stem_top + t * (stem_bottom - stem_top) * 0.7)
        spread = radius * 0.32 * (0.4 + 0.6 * t)
        draw.line(
            [cx, ly, int(cx - spread), int(ly - spread * 0.5)],
            fill=NAVY,
            width=max(2, radius // 18),
        )
        draw.line(
            [cx, ly, int(cx + spread), int(ly - spread * 0.5)],
            fill=NAVY,
            width=max(2, radius // 18),
        )


def wordmark(size):
    """'UK COMMODITY PRICES' lockup on a matte background, sized to (w, h)."""
    w, h = size
    img = Image.new("RGB", (w, h), MATTE_BG)
    draw = ImageDraw.Draw(img)
    band_h = h * 0.18
    draw_flag_band(draw, 0, 0, w, band_h)
    draw_flag_band(draw, 0, h - band_h, w, h)

    coin_r = h * 0.22
    coin_cx = coin_r * 1.6
    coin_cy = h / 2
    draw_wheat_coin(draw, coin_cx, coin_cy, coin_r)

    title_font = load_font(int(h * 0.16))
    sub_font = load_font(int(h * 0.09))
    text_x = int(coin_cx + coin_r * 1.6)
    draw.text((text_x, int(h * 0.32)), "UK COMMODITY", font=title_font, fill=WHITE)
    draw.text((text_x, int(h * 0.58)), "PRICES", font=sub_font, fill=GOLD)
    return img


def mod_icon(size=512):
    """512x512, design centred, matte background."""
    img = Image.new("RGB", (size, size), MATTE_BG)
    draw = ImageDraw.Draw(img)
    band_h = size * 0.14
    draw_flag_band(draw, 0, 0, size, band_h)
    draw_flag_band(draw, 0, size - band_h, size, size)

    draw_wheat_coin(draw, size / 2, size * 0.44, size * 0.26)

    font = load_font(int(size * 0.075))
    text = "UK COMMODITY\nPRICES"
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(
        (int((size - tw) / 2), int(size * 0.76 - th / 2)),
        text,
        font=font,
        fill=WHITE,
        align="center",
    )
    return img


def store_icon(size=512):
    """512x512, design bottom-aligned, matte background (no true alpha in BC1)."""
    img = Image.new("RGB", (size, size), MATTE_BG)
    draw = ImageDraw.Draw(img)

    coin_bottom = size * 0.52 + size * 0.2

    font = load_font(int(size * 0.07))
    text = "UK COMMODITY\nPRICES"
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    tw = bbox[2] - bbox[0]
    text_y = int(coin_bottom + size * 0.04)
    draw_wheat_coin(draw, size / 2, size * 0.52, size * 0.2)
    draw.multiline_text(
        (int((size - tw) / 2), text_y),
        text,
        font=font,
        fill=WHITE,
        align="center",
    )

    band_h = size * 0.06
    draw_flag_band(draw, 0, size - band_h, size, size)
    return img


def brand_icon(size=(512, 256)):
    return wordmark(size)


# --- Minimal BC1 (DXT1) DDS encoder -----------------------------------------

DDS_MAGIC = b"DDS "
DDSD_CAPS = 0x1
DDSD_HEIGHT = 0x2
DDSD_WIDTH = 0x4
DDSD_PIXELFORMAT = 0x1000
DDSD_LINEARSIZE = 0x80000
DDPF_FOURCC = 0x4
DDSCAPS_TEXTURE = 0x1000


def _rgb_to_565(r, g, b):
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


def _565_to_rgb(c):
    r = (c >> 11) & 0x1F
    g = (c >> 5) & 0x3F
    b = c & 0x1F
    return (r << 3) | (r >> 2), (g << 2) | (g >> 4), (b << 3) | (b >> 2)


def _compress_block(pixels):
    """Compress a 4x4 block of (r,g,b) tuples into 8 bytes of BC1 data."""
    max_c = max(pixels)
    min_c = min(pixels)
    if max_c == min_c:
        c0 = c1 = _rgb_to_565(*max_c)
        indices = [0] * 16
    else:
        c0 = _rgb_to_565(*max_c)
        c1 = _rgb_to_565(*min_c)
        r0, g0, b0 = _565_to_rgb(c0)
        r1, g1, b1 = _565_to_rgb(c1)
        palette = [
            (r0, g0, b0),
            (r1, g1, b1),
            ((2 * r0 + r1) // 3, (2 * g0 + g1) // 3, (2 * b0 + b1) // 3),
            ((r0 + 2 * r1) // 3, (g0 + 2 * g1) // 3, (b0 + 2 * b1) // 3),
        ]
        indices = []
        for px in pixels:
            best_i, best_d = 0, None
            for i, pc in enumerate(palette):
                d = sum((a - b) ** 2 for a, b in zip(px, pc))
                if best_d is None or d < best_d:
                    best_i, best_d = i, d
            indices.append(best_i)

    packed_indices = 0
    for i, idx in enumerate(indices):
        packed_indices |= idx << (2 * i)

    return struct.pack("<HHI", c0, c1, packed_indices)


def encode_bc1(img):
    """Encode an RGB PIL Image to raw BC1/DXT1 block data. Dimensions must be multiples of 4."""
    w, h = img.size
    if w % 4 or h % 4:
        raise ValueError(f"BC1 encoding requires dimensions divisible by 4, got {w}x{h}")
    px = img.convert("RGB").load()
    out = bytearray()
    for by in range(0, h, 4):
        for bx in range(0, w, 4):
            block = [px[bx + dx, by + dy] for dy in range(4) for dx in range(4)]
            out += _compress_block(block)
    return bytes(out)


def write_dds_bc1(path, img):
    w, h = img.size
    data = encode_bc1(img)
    linear_size = len(data)

    header = bytearray(124)
    struct.pack_into(
        "<7I",
        header,
        0,
        124,  # header size
        DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PIXELFORMAT | DDSD_LINEARSIZE,
        h,
        w,
        linear_size,
        0,  # depth
        0,  # mipmap count
    )
    # pixel format sub-struct starts at offset 72, size 32
    pf_offset = 72
    struct.pack_into(
        "<2I4s5I",
        header,
        pf_offset,
        32,  # pixel format size
        DDPF_FOURCC,
        b"DXT1",
        0, 0, 0, 0, 0,  # bit counts / masks, unused for fourcc formats
    )
    struct.pack_into("<I", header, pf_offset + 32, DDSCAPS_TEXTURE)  # caps

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(DDS_MAGIC)
        f.write(header)
        f.write(data)


def main():
    PNG_DIR.mkdir(parents=True, exist_ok=True)

    assets = {
        "ModIcon": mod_icon(),
        "StoreIcon": store_icon(),
        "BrandIcon": brand_icon(),
    }

    for name, img in assets.items():
        png_path = PNG_DIR / f"{name}.png"
        img.save(png_path)
        print(f"wrote {png_path} ({img.size[0]}x{img.size[1]})")

        dds_path = DDS_DIR / f"{name}.dds"
        write_dds_bc1(dds_path, img)
        print(f"wrote {dds_path} ({dds_path.stat().st_size} bytes, BC1/DXT1)")


if __name__ == "__main__":
    sys.exit(main())
