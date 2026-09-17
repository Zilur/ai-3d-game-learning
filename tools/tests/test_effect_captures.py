"""Test RGB/RGBA normalization and PNG filter handling used by real-renderer checks."""
import struct
import tempfile
import unittest
from pathlib import Path
import zlib
from lib.checks.check_effect_captures import png


def fixture(channels, filter_id=0):
    rows = [bytes([8, 20, 30, 255, 40, 50, 60, 255]), bytes([70, 80, 90, 255, 100, 110, 120, 255])]
    pixels = rows if channels == 4 else [bytes(v for i, v in enumerate(row) if i % 4 != 3) for row in rows]
    raw = bytearray()
    previous = bytes(2 * channels)
    for row in pixels:
        raw.append(filter_id)
        for i, value in enumerate(row):
            a = row[i-channels] if i >= channels else 0
            b = previous[i]
            c = previous[i-channels] if i >= channels else 0
            p = a + b - c
            distances = [abs(p-a), abs(p-b), abs(p-c)]
            paeth = (a,b,c)[distances.index(min(distances))]
            raw.append((value - (0,a,b,(a+b)//2,paeth)[filter_id]) & 255)
        previous = row
    def chunk(kind, data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',2,2,8,6 if channels == 4 else 2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''), rows


class CaptureImages(unittest.TestCase):
    def test_rgb_and_rgba_with_every_filter(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'probe.png'
            for channels in (3,4):
                for filter_id in range(5):
                    with self.subTest(channels=channels, filter=filter_id):
                        data, expected = fixture(channels, filter_id)
                        path.write_bytes(data)
                        w,h,rows = png(path)
                        self.assertEqual((w,h,rows),(2,2,expected))

    def test_non_png_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'not.png'
            path.write_bytes(b'not a PNG image')
            with self.assertRaises(ValueError):
                png(path)

    def test_unsupported_color_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'indexed.png'
            data,_=fixture(3)
            raw=bytearray(data);raw[25]=3
            path.write_bytes(raw)
            with self.assertRaises(ValueError):
                png(path)


if __name__ == '__main__':
    unittest.main()
