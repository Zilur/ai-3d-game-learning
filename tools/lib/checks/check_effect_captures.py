"""Read actual Godot RGB8/RGBA8 PNG captures and compare only scene pixels, not UI.
Standard library only; deliberately rejects other image encodings rather than guessing.
Pixel change is evidence of rendering, not evidence of attractiveness or learning.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import struct
import zlib


def png(path: Path) -> tuple[int, int, list[bytes]]:
    data = path.read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Not a PNG')
    i = 8
    compressed = bytearray()
    width = height = 0
    channels = 0
    while i < len(data):
        size, kind = struct.unpack('>I4s', data[i:i+8])
        body = data[i+8:i+8+size]
        if kind == b'IHDR':
            width, height, depth, color, cm, fm, interlace = struct.unpack('>IIBBBBB', body)
            if (depth, cm, fm, interlace) != (8, 0, 0, 0) or color not in (2, 6) or not 0 < width*height <= 4_000_000:
                raise ValueError('Expected bounded Godot RGB8 or RGBA8 image')
            channels = 3 if color == 2 else 4
        if kind == b'IDAT':
            compressed.extend(body)
        i += size + 12
    raw = zlib.decompress(compressed)
    if channels == 0:
        raise ValueError('Missing PNG header')
    stride = width * channels
    if len(raw) != height * (stride + 1):
        raise ValueError('Wrong PNG scanline length')
    rows: list[bytes] = []
    prior = bytearray(stride)
    for y in range(height):
        at = y * (stride+1)
        kind = raw[at]
        if kind > 4:
            raise ValueError('Unsupported PNG scanline filter')
        row = bytearray(raw[at+1:at+1+stride])
        for x in range(stride):
            a = row[x-channels] if x >= channels else 0
            b = prior[x]
            c = prior[x-channels] if x >= channels else 0
            p = a+b-c
            pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
            paeth = a if pa <= pb and pa <= pc else b if pb <= pc else c
            add = (0, a, b, (a+b)//2, paeth)[kind]
            row[x] = (row[x] + add) & 255
        if channels == 4:
            rows.append(bytes(row))
        else:
            rgba = bytearray(width*4)
            for pixel in range(width):
                rgba[pixel*4:pixel*4+3] = row[pixel*3:pixel*3+3]
                rgba[pixel*4+3] = 255
            rows.append(bytes(rgba))
        prior = row
    return width, height, rows


def compare(base: Path, changed: Path) -> dict:
    width, height, rows = png(base)
    w2, h2, other = png(changed)
    if (width, height) != (w2, h2):
        raise ValueError('Capture sizes differ')
    # Lab side panel is left of 445 px. Exclude it and all edges.
    count = total = magnitude = 0
    for y in range(70, min(height-60, 650)):
        for x in range(470, width-25):
            at = x*4
            delta = sum(abs(rows[y][at+c] - other[y][at+c]) for c in range(3))
            count += delta > 9
            magnitude += delta
            total += 1
    return {'changed_scene_pixels': count, 'sampled_pixels': total, 'rgb_absolute_difference': magnitude}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--require-dof', action='store_true')
    args = parser.parse_args()
    report = {name: compare(args.folder / 'effects-baseline.png', args.folder / ('effects-'+name+'.png'))
              for name in ('fog', 'glow', 'dof')}
    for name in ('fog', 'glow', 'dof') if args.require_dof else ('fog', 'glow'):
        if report[name]['changed_scene_pixels'] < 80:
            raise RuntimeError('No adequate scene-only pixel evidence for ' + name + ': ' + str(report[name]))
    (args.folder / 'pixel-evidence.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('EFFECT PIXEL PASS:', report)


if __name__ == '__main__':
    main()
