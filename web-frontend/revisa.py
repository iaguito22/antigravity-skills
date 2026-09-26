#!/usr/bin/env python3
"""AI-tell linter for html files. Usage: revisa.py index.html  |  revisa.py p?.html
What the skill bans still gets written if nobody checks it: this checks it.
Exits with 1 when it warns, so chain it with ';' and not '&&' if you look afterwards."""
import os, re, sys

FRASES = ["sin prisa", "con calma", "honest", "artesan", "de la finca a la taza", "te mereces",
          "experiencia única", "experiencia unica", "pasión por", "pasion por", "descubre",
          "implacable", "a otro nivel", "sin rodeos", "de confianza", "calidad premium",
          "hecho con amor", "tu mejor aliado", "soluciones integrales", "cercanía",
          # English
          "unhurried", "artisan", "farm to cup", "you deserve", "unique experience",
          "passion for", "discover", "elevate", "relentless", "no-nonsense", "next level",
          "seamless", "unlock", "world-class", "cutting-edge", "crafted with love"]
FUENTES = ["Inter", "DM Sans", "Plus Jakarta Sans", "Poppins", "Montserrat", "Fraunces",
           "Playfair Display", "Newsreader"]
SERIFAS = ("instrument serif", "fraunces", "playfair", "newsreader", "cormorant", "garamond",
           "dm serif", "libre caslon", "lora", "gloock", "young serif", "erode", "zodiak",
           "gambetta", "sentient", "boska")
VIVO = [r"abiert[oa] (hoy|ahora)", r"en proceso", r"turnos? libres?", r"plazas? libres?",
        r"estado:", r"\d+\.\d{3,}°", r"en directo", r"\blive\b",
        r"open (now|today)", r"in progress", r"slots? (left|available)", r"status:"]
VERDES = r"#(22c55e|10b981|4ade80|16a34a|34d399|00c853)|\bgreen\b|limegreen"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✨]")
MONO = ("mono", "code", "courier")


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def color_vivo(c):
    """True if a CSS color has a hue (not black, white or grey)."""
    c = c.strip().lower()
    m = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?", c)
    if m:
        r, g, b = (int(x) for x in m.groups()[:3])
        a = float(m.group(4)) if m.group(4) else 1.0
        return max(r, g, b) - min(r, g, b) > 40 and a >= 0.25
    m = re.match(r"#([0-9a-f]{3}|[0-9a-f]{6})\b", c)
    if m:
        r, g, b = hex_rgb(m.group(0))
        return max(r, g, b) - min(r, g, b) > 40
    return False


def pistas_muy_ia(h, bajo, texto):
    """What users call 'so AI': split hero, colored word, row of stats, glows."""
    mal = []
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", bajo, flags=re.S))
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    # 1. Headline keyword in another color / colored italics / gradient.
    for h1 in re.findall(r"<h1\b[^>]*>(.*?)</h1>", bajo, flags=re.S)[:1]:
        total = len(re.sub(r"<[^>]+>|\s+", "", h1)) or 1
        for tag, attrs, dentro in re.findall(r"<(span|em|i|strong|mark|b)\b([^>]*)>(.*?)</\1>", h1, flags=re.S):
            if "<img" in dentro or "<br" in dentro:
                continue
            parte = len(re.sub(r"<[^>]+>|\s+", "", dentro))
            if not parte or parte / total > 0.6:
                continue
            coloreado = re.search(r"color|gradient|text-fill", attrs)
            for cls in re.findall(r'class="([^"]+)"', attrs):
                for c in cls.split():
                    if re.search(r"\." + re.escape(c) + r"\b[^{]*\{[^}]*(?<!background-)(?<!-)color\s*:|\." + re.escape(c) + r"\b[^{]*\{[^}]*(gradient|text-fill)", css):
                        coloreado = True
            if re.search(r"h1\s+" + tag + r"\b[^{]*\{[^}]*((?<!background-)(?<!-)color\s*:|gradient|text-fill)", css):
                coloreado = True
            if coloreado:
                mal.append("headline word in another color/colored italics: the H1 uses a single ink")
                break
    # 2. Horizontal row of stats (10x · 65 % · 24/7).
    cifras = [m.start() for m in re.finditer(
        r">\s*[<]?\s*(\d[\d.,]*\s*(%|x|×|\+|k\+?|m\+?|/7)|24/7)\s*<", bajo)]
    for i in range(len(cifras) - 2):
        if cifras[i + 2] - cifras[i] < 1500:
            mal.append("row of stats (3 or more in a row): put them one by one in cards, or drop them")
            break
    # 2b. Ticker or carousel of stats: same tell, moving.
    for bloque in re.findall(r"<(?:div|section|ul)[^>]*class=\"[^\"]*(?:marquee|marquesina|cinta|ticker)[^\"]*\"[^>]*>(.*?)</(?:div|section|ul)>", bajo, flags=re.S):
        if len(re.findall(r"\d", re.sub(r"<[^>]+>", " ", bloque))) >= 4:
            mal.append("ticker or carousel with numbers: drop it; if there is a ticker, it carries names, not stats")
            break
    # 3. Glows: offsetless colored shadows, colored text-shadow, blurred blobs.
    brillo = False
    for regla in re.findall(r"(?:box|text)-shadow\s*:([^;}]+)", bajo):
        for capa in regla.split("),"):
            capa = capa if capa.endswith(")") or "(" not in capa else capa + ")"
            col = re.search(r"(rgba?\([^)]*\)|#[0-9a-f]{3,6}\b)", capa)
            antes = capa[:col.start()] if col else capa
            px = [float(x) for x in re.findall(r"(-?\d*\.?\d+)(?:px)?(?=\s|$)", antes.replace("inset", " "))]
            if col and color_vivo(col.group(1)) and len(px) >= 3 and abs(px[0]) < 2 and abs(px[1]) < 2 and px[2] >= 12:
                brillo = True
    if brillo:
        mal.append("colored glow (shadow with no offset): remove it, the light comes from the image")
    if any(float(n) >= 40 for n in re.findall(r"(?<!backdrop-)filter\s*:\s*blur\(\s*([\d.]+)px", bajo)):
        mal.append("blurred blob (large filter: blur): drop it, the background stays flat")
    # 4. Split hero: the hero rule lays out two columns.
    for sel, cuerpo in re.findall(r"([^{}]*hero[^{}]*)\{([^}]*)\}", css):
        # Only the hero container; a grid of cards or widgets inside is not a split hero.
        if re.search(r"card|widget|stat|row|chip|list|metric|tab|item|badge|pill|grid-item|nav", sel):
            continue
        m = re.search(r"grid-template-columns\s*:\s*([^;]+)", cuerpo)
        if not m:
            continue
        cols = m.group(1).strip()
        n = 2 if re.match(r"repeat\(\s*2\s*,", cols) else len(re.findall(r"[\w.%()-]+(?:\([^)]*\))?", re.sub(r"\[[^\]]*\]", "", cols)))
        if n == 2:
            mal.append("hero in two columns (%s): if it is text|image, it is the split hero" % sel.strip()[:40])
            break
    # 4b. The same trick inside a bento: the hero card spans 5-9 of 12 columns and the
    # photo sits next to it. Visually it is half text, half image again.
    for sel, cuerpo in re.findall(r"([^{}]*hero[^{}]*)\{([^}]*)\}", css):
        m = re.search(r"grid-column\s*:\s*span\s+(\d+)", cuerpo)
        if m and 5 <= int(m.group(1)) <= 9 and not re.search(r"@media|max-width", sel):
            mal.append("the hero card (%s) spans %s of 12 columns: with a photo next to it that is the "
                       "split hero; make it full width" % (sel.strip()[:40], m.group(1)))
            break
    return mal


def familias(bajo):
    """Typefaces the page loads or declares, lowercased."""
    fam = set()
    for f in re.findall(r"family=([a-z0-9+ ]+)", bajo):
        fam.add(f.replace("+", " ").strip())
    for f in re.findall(r"f\[\]=([a-z0-9-]+)", bajo):
        fam.add(f.replace("-", " ").strip())
    for decl in re.findall(r"font-family:\s*([^;}\"]+)", bajo):
        for f in decl.split(","):
            f = f.strip().strip("'\"")
            if f and not f.startswith("var(") and f not in ("serif", "sans-serif", "monospace",
                                                            "system-ui", "inherit", "cursive"):
                fam.add(f)
    return fam


def revisa(ruta):
    h = open(ruta, encoding="utf-8", errors="replace").read()
    bajo = h.lower()
    texto = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", bajo, flags=re.S)
    texto = re.sub(r"<[^>]+>", " ", texto)
    mal = []
    for f in FRASES:
        if f in texto:
            mal.append('stock phrase: "%s" -> write a concrete fact' % f)
    fam = familias(bajo)
    for f in FUENTES:
        if f.lower() in fam:
            mal.append("default font: %s -> use the die's" % f)
    for p in VIVO:
        m = re.search(p, texto)
        if m:
            mal.append('made-up "live" data: "%s" -> a static page cannot know that' % m.group(0))
    # Green "open" dot: in a CSS rule or an inline style.
    trozos = re.findall(r"\{[^}]*\}", bajo) + re.findall(r"<[^>]+>", bajo)
    if any(re.search(VERDES, t) and re.search(r"50%|999|9999px|\bdot\b|pulse|status", t) for t in trozos):
        mal.append("green 'open' dot: remove it")
    # Emoji pill above the headline (2023 template).
    antes_h1 = bajo.split("<h1", 1)[0]
    antes_h1 = re.sub(r"<(script|style|head)[^>]*>.*?</\1>", " ", antes_h1, flags=re.S)
    if "<h1" in bajo and EMOJI.search(re.sub(r"<[^>]+>", " ", antes_h1)):
        mal.append("emoji above the H1 (the 2023 pill): remove it")
    # 2026 template: cream background + serif headline.
    fondos = re.findall(r"--(?:bg|fondo|background)[\w-]*:\s*(#[0-9a-f]{3,6})\b", bajo)
    fondos += re.findall(r"body\s*\{[^}]*background(?:-color)?:\s*(#[0-9a-f]{3,6})\b", bajo)
    fondos += re.findall(r"<body[^>]*background(?:-color)?:\s*(#[0-9a-f]{3,6})\b", bajo)
    crema = False
    for c in fondos[:2]:
        try:
            r, g, b = hex_rgb(c)
        except ValueError:
            continue
        if r >= 235 and r - b >= 10 and g > b:
            crema = True
    if crema and any(s in f for f in fam for s in SERIFAS):
        mal.append("cream background + serif: that is the 2026 template -> change one of them")
    cejas = len(re.findall(r"text-transform:\s*uppercase[^}]*letter-spacing|letter-spacing[^}]*text-transform:\s*uppercase", bajo))
    if cejas > 3:
        mal.append("%d spaced UPPERCASE styles: keep one at most" % cejas)
    imgs = re.findall(r"<img\b[^>]*>", bajo)
    for tag in imgs:
        if 'alt="' not in tag or "width" not in tag:
            mal.append("img without alt or width/height: " + tag[:60])
            break
    fotos = imgs or re.search(r"url\(\s*['\"]?[^)'\"]+\.(jpe?g|png|webp|avif)", bajo)
    # With several versions (prototypes) some may be type and SVG only: there the photo is
    # required of the set, in main, not of each one.
    if not fotos and not VARIAS and not re.search(r"<canvas|<video|three\.", bajo):
        mal.append("not a single image: for a landing or portfolio the hero one is missing (generate_image)")
    # Dark overlay eating the photo: a nearly opaque gradient over an image.
    if fotos:
        peor = 0.0
        for grad in re.findall(r"linear-gradient\(([^;]*)", bajo):
            for r, g, b, a in re.findall(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)", grad):
                if int(r) + int(g) + int(b) < 200:
                    peor = max(peor, float(a))
        if peor >= 0.75:
            mal.append("dark overlay at %d%% over the photo: the image leads, keep it at 50%% or less" % (peor * 100))
    # Uncompressed local images.
    base = os.path.dirname(os.path.abspath(ruta))
    for src in sorted(set(re.findall(r"""(?:src=|url\()\s*['"]?([^'")\s>]+\.(?:jpe?g|png|webp))""", h, flags=re.I))):
        f = os.path.join(base, src)
        if not src.startswith(("http", "data:")) and os.path.isfile(f) and os.path.getsize(f) > 350_000:
            mal.append("%s weighs %d KB: compress it (see web-frontend skill §2)" % (src, os.path.getsize(f) // 1000))
    # Real-looking phone numbers (Spanish format): if the user did not give them, they are made up.
    for tel in re.findall(r"(?<![\d.,])(?:\+34\s?)?[6789]\d{2}(?:[\s.]?\d{2,3}){3}(?![\d.,])", texto):
        if not re.fullmatch(r"(?:\+34\s?)?[6789](?:[\s.]?0)+", tel.strip()):
            mal.append("phone %s: if the user did not give it, use 000 000 000 and flag it in the report" % tel.strip())
            break
    mal += pistas_muy_ia(h, bajo, texto)
    secciones = len(re.findall(r"<section\b", bajo))
    if secciones > 6:
        mal.append("%d sections: a landing needs 4-5" % secciones)
    for f in re.findall(r"<form\b", bajo)[:1]:
        mal.append("there is a <form>: if nobody asked for it, use phone/email/link instead")
    if len(h) > 32000:
        mal.append("%d KB: there is content nobody asked for" % (len(h) // 1000))
    return mal, fam, bool(fotos)


def main(rutas):
    total = 0
    usos = {}
    titulares = {}
    con_foto = 0
    for ruta in rutas:
        m = re.search(r"<h1[^>]*>(.*?)</h1>", open(ruta, encoding="utf-8", errors="replace").read(), re.S | re.I)
        if m:
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip().lower()
            titulares.setdefault(t, []).append(os.path.basename(ruta))
            if len(t.split()) > 12:
                total += 1
                print("· %s: the H1 has %d words; 12 at most (the rest goes to the subtitle)" %
                      (os.path.basename(ruta), len(t.split())))
        mal, fam, foto = revisa(ruta)
        con_foto += foto
        total += len(mal)
        if len(rutas) > 1:
            print("== " + ruta)
        print("\n".join("· " + m for m in mal) if mal else "Linter: clean.")
        for f in fam:
            if not any(m in f for m in MONO):
                usos.setdefault(f, []).append(os.path.basename(ruta))
    # Several versions of a page: they must not converge on the same typeface.
    if VARIAS and not con_foto:
        total += 1
        print("· no version has a photo: generate 1-2 with generate_image and use them")
    for t, donde in titulares.items():
        if len(donde) >= 2:
            total += 1
            print('· same headline in %s ("%s"): each version writes its own in its VOICE' %
                  (" ".join(donde), t[:60]))
    if len(rutas) >= 3:
        for f, donde in sorted(usos.items()):
            if len(donde) >= 3:
                total += 1
                print("· %s appears in %d of %d (%s): each version with its own typeface" %
                      (f, len(donde), len(rutas), " ".join(donde)))
    sys.exit(1 if total else 0)


RUTAS = sys.argv[1:] or ["index.html"]
VARIAS = len(RUTAS) > 1
main(RUTAS)
