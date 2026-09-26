#!/usr/bin/env python3
"""Copies a generate_image output next to the html, already compressed.
Usage: foto.py <source> <dest.jpg> [width=1600]
generate_image delivers 750-900 KB JPEGs: a landing with two weighed 1.6 MB."""
import os, sys

orig, dest = sys.argv[1], sys.argv[2]
ancho = int(sys.argv[3]) if len(sys.argv) > 3 else 1600
try:
    from PIL import Image
    im = Image.open(orig)
    im.thumbnail((ancho, ancho))
    im.convert("RGB").save(dest, "JPEG", quality=78, optimize=True, progressive=True)
    w, h = im.size
except ImportError:
    import subprocess
    subprocess.run(["vips", "thumbnail", orig, dest + "[Q=78,strip,interlace]", str(ancho)], check=True)
    w = h = None
kb = os.path.getsize(dest) // 1000
print("%s -> %s · %d KB%s" % (os.path.basename(orig), dest, kb,
                              " · width=%d height=%d" % (w, h) if w else ""))
