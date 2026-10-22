#!/usr/bin/env python3
"""Copia imagenes de generate_image junto al html, ya comprimidas. Varias en UNA llamada:
Uso: foto.py <origen> <destino.jpg> [<origen2> <destino2.jpg> ...] [--ancho 1600]
generate_image entrega JPEG de 750-900 KB: una landing con dos pesaba 1,6 MB."""
import os, sys

args = sys.argv[1:]
ancho = 1600
if "--ancho" in args:
    i = args.index("--ancho"); ancho = int(args[i + 1]); del args[i:i + 2]
if not args or len(args) % 2:
    sys.exit(__doc__)
for orig, dest in zip(args[::2], args[1::2]):
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
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
