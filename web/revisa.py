#!/usr/bin/env python3
"""Revisor de delatores de IA en un html. Uso: revisa.py index.html  |  revisa.py p?.html
Lo que la skill prohibe se escribe igual si nadie lo comprueba: esto lo comprueba.
Sale con 1 si hay avisos, asi que encadenalo con ';' y no con '&&' si luego vas a mirar."""
import os, re, sys

FRASES = ["sin prisa", "con calma", "honest", "artesan", "de la finca a la taza", "te mereces",
          "experiencia única", "experiencia unica", "pasión por", "pasion por", "descubre",
          "implacable", "a otro nivel", "sin rodeos", "de confianza", "calidad premium",
          "hecho con amor", "tu mejor aliado", "soluciones integrales", "cercanía"]
FUENTES = ["Inter", "DM Sans", "Plus Jakarta Sans", "Poppins", "Montserrat", "Fraunces",
           "Playfair Display", "Newsreader", "Cormorant"]
SERIFAS = ("instrument serif", "fraunces", "playfair", "newsreader", "cormorant", "garamond",
           "dm serif", "libre caslon", "lora", "gloock", "young serif", "erode", "zodiak",
           "gambetta", "sentient", "boska")
VIVO = [r"abiert[oa] (hoy|ahora)", r"en proceso", r"turnos? libres?", r"plazas? libres?",
        r"estado:", r"\d+\.\d{3,}°", r"en directo", r"\blive\b"]
VERDES = r"#(22c55e|10b981|4ade80|16a34a|34d399|00c853)|\bgreen\b|limegreen"
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✨]")
MONO = ("mono", "code", "courier")


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def color_vivo(c):
    """True si un color CSS tiene tono (no es negro, blanco ni gris)."""
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
    """Lo que el usuario llama 'muy IA': hero partido, palabra en color, fila de cifras, brillos."""
    mal = []
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", bajo, flags=re.S))
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    # 1. Palabra clave del titular en otro color / cursiva de color / degradado.
    for h1_attrs, h1 in re.findall(r"<h1\b([^>]*)>(.*?)</h1>", bajo, flags=re.S)[:1]:
        h1_clases = re.findall(r'class="([^"]+)"', h1_attrs)
        h1_clases = h1_clases[0].split() if h1_clases else []
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
            sel = "(?:h1" + "".join(r"|\." + re.escape(c) for c in h1_clases) + ")"
            if re.search(sel + r"\s+" + tag + r"\b[^{]*\{[^}]*((?<!background-)(?<!-)color\s*:|gradient|text-fill)", css):
                coloreado = True
            if coloreado:
                mal.append("palabra del titular en otro color/cursiva de color: el H1 va en una sola tinta")
                break
    # 2. Fila horizontal de cifras (10x · 65 % · 24/7).
    cifras = [m.start() for m in re.finditer(
        r">\s*[<]?\s*(\d[\d.,]*\s*(%|x|×|\+|k\+?|m\+?|/7)|24/7)\s*<", bajo)]
    for i in range(len(cifras) - 2):
        if cifras[i + 2] - cifras[i] < 1500:
            mal.append("fila de cifras (3 o mas seguidas): metelas de una en una en tarjetas, o fuera")
            break
    # 2b. Cinta o carrusel de cifras (lo vio en un prototipo y tampoco lo quiere).
    for bloque in re.findall(r"<(?:div|section|ul)[^>]*class=\"[^\"]*(?:marquee|marquesina|cinta|ticker)[^\"]*\"[^>]*>(.*?)</(?:div|section|ul)>", bajo, flags=re.S):
        if len(re.findall(r"\d", re.sub(r"<[^>]+>", " ", bloque))) >= 4:
            mal.append("cinta o carrusel con cifras: fuera; si hay cinta, que lleve nombres, no datos")
            break
    # 3. Brillos: sombras de color sin desplazamiento, text-shadow de color, blobs difuminados.
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
        mal.append("brillo de color (sombra sin desplazamiento): quitalo, la luz la pone la imagen")
    if any(float(n) >= 40 for n in re.findall(r"(?<!backdrop-)filter\s*:\s*blur\(\s*([\d.]+)px", bajo)):
        mal.append("blob difuminado (filter: blur grande): fuera, el fondo va plano")
    # 4. Hero partido: la regla del hero reparte en dos columnas.
    for sel, cuerpo in re.findall(r"([^{}]*hero[^{}]*)\{([^}]*)\}", css):
        # Solo el contenedor del hero; una rejilla de tarjetas o widgets dentro no es un hero partido.
        if re.search(r"card|widget|stat|row|chip|list|metric|tab|item|badge|pill|grid-item|nav", sel):
            continue
        m = re.search(r"grid-template-columns\s*:\s*([^;]+)", cuerpo)
        if not m:
            continue
        cols = m.group(1).strip()
        n = 2 if re.match(r"repeat\(\s*2\s*,", cols) else len(re.findall(r"[\w.%()-]+(?:\([^)]*\))?", re.sub(r"\[[^\]]*\]", "", cols)))
        if n == 2:
            mal.append("hero en dos columnas (%s): si es texto|imagen, es el hero partido que no quiere" % sel.strip()[:40])
            break
    # 4b. El mismo truco dentro de un bento: la tarjeta del hero ocupa 5-9 de 12 columnas y
    # al lado va la foto. A la vista es otra vez mitad texto, mitad imagen.
    for sel, cuerpo in re.findall(r"([^{}]*hero[^{}]*)\{([^}]*)\}", css):
        m = re.search(r"grid-column\s*:\s*span\s+(\d+)", cuerpo)
        if m and 5 <= int(m.group(1)) <= 9 and not re.search(r"@media|max-width", sel):
            mal.append("la tarjeta del hero (%s) ocupa %s de 12 columnas: con una foto al lado es el "
                       "hero partido; hazla de ancho completo" % (sel.strip()[:40], m.group(1)))
            break
    return mal


def anatomia(bajo):
    """La anatomia por defecto (skill, «Lo que le gusta»): foto DE FONDO en el hero y foto en cada card."""
    mal = []
    cuerpo = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", bajo, flags=re.S)
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", bajo, flags=re.S))
    # 1. Hero: si la primera imagen de la pagina va despues del H1 y nada la pone de fondo,
    # el hero es un bloque de texto sobre fondo liso con la foto debajo.
    i_h1 = cuerpo.find("<h1")
    if i_h1 >= 0:
        imgs = [x for x in (cuerpo.find("<img"), cuerpo.find("<video"), cuerpo.find("url(")) if x >= 0]
        fondo_css = re.search(r"[^{}]*(hero|bg|fondo|backdrop|cover|stage)[^{}]*\{[^}]*background(-image)?\s*:[^;]*url\(", css)
        if not fondo_css and (not imgs or min(imgs) > i_h1):
            mal.append("hero sin foto de fondo: el titular va encima de una foto a pantalla completa, no sobre fondo liso con la foto debajo")
    # 2. Cards de producto sin foto.
    bloques = re.split(r"(?=<article\b)|(?=<(?:div|li|a)\b[^>]*class=\"(?:[^\"]*\s)?(?:card|product|producto|modelo|model|item|[a-z]+-card)(?:\s[^\"]*)?\")", cuerpo)
    cards = [b for b in bloques[1:] if not re.match(r"<[^>]*(micro|widget|chip|stat|tech|visit|hero)", b)
             and re.search(r"\d[\d.,]*\s*(€|eur\b|\$)|\$\s*\d", b[:2500])]
    sin = [b for b in cards if not re.search(r"<img|<picture|url\(", b[:2500])]
    if len(cards) >= 3 and len(sin) * 2 > len(cards):
        mal.append("%d de %d cards de producto sin foto: la card es foto primero" % (len(sin), len(cards)))
    return mal


def familias(bajo):
    """Tipografias que carga o declara la pagina, en minusculas."""
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
    h = h0 = open(ruta, encoding="utf-8", errors="replace").read()
    # Las hojas enlazadas cuentan como si estuvieran dentro: si no, una palabra en
    # color definida en styles.css pasaba sin aviso.
    base = os.path.dirname(os.path.abspath(ruta))
    for href in re.findall(r'<link[^>]+href="([^"#?]+\.css)"', h, flags=re.I):
        p = os.path.join(base, href)
        if os.path.isfile(p):
            h += "<style>" + open(p, encoding="utf-8", errors="replace").read() + "</style>"
    bajo = h.lower()
    texto = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", bajo, flags=re.S)
    texto = re.sub(r"<[^>]+>", " ", texto)
    mal = []
    for f in FRASES:
        if f in texto:
            mal.append('frase hecha: "%s" -> escribe un dato concreto' % f)
    fam = familias(bajo)
    for f in FUENTES:
        if any(x == f.lower() or x.startswith(f.lower() + " ") for x in fam):
            mal.append("fuente por defecto: %s -> usa las del dado" % f)
    for p in VIVO:
        m = re.search(p, texto)
        if m:
            mal.append('dato "en vivo" inventado: "%s" -> una web estatica no sabe eso' % m.group(0))
    # Punto verde de "abierto": en una regla CSS o en un style en linea.
    trozos = re.findall(r"\{[^}]*\}", bajo) + re.findall(r"<[^>]+>", bajo)
    if any(re.search(VERDES, t) and re.search(r"50%|999|9999px|\bdot\b|pulse|status", t) for t in trozos):
        mal.append("punto verde de 'abierto': quitalo")
    # Pastilla con emoji encima del titular (plantilla 2023).
    antes_h1 = bajo.split("<h1", 1)[0]
    antes_h1 = re.sub(r"<(script|style|head)[^>]*>.*?</\1>", " ", antes_h1, flags=re.S)
    if "<h1" in bajo and EMOJI.search(re.sub(r"<[^>]+>", " ", antes_h1)):
        mal.append("emoji encima del H1 (la pastilla de 2023): quitalo")
    # Plantilla 2026: fondo crema + titular con serifa.
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
        mal.append("fondo crema + serifa: es la plantilla 2026 -> cambia uno de los dos")
    cejas = len(re.findall(r"text-transform:\s*uppercase[^}]*letter-spacing|letter-spacing[^}]*text-transform:\s*uppercase", bajo))
    if cejas > 3:
        mal.append("%d estilos en MAYUSCULAS espaciadas: deja uno como mucho" % cejas)
    imgs = re.findall(r"<img\b[^>]*>", bajo)
    for tag in imgs:
        if 'alt="' not in tag or "width" not in tag:
            mal.append("img sin alt o sin width/height: " + tag[:60])
            break
    fotos = imgs or re.search(r"url\(\s*['\"]?[^)'\"]+\.(jpe?g|png|webp|avif)", bajo)
    # Con varias versiones (prototypes) algunas van solo con tipografia y SVG: alli se
    # exige la foto al conjunto, en main, no a cada una.
    if not fotos and not VARIAS and not re.search(r"<canvas|<video|three\.", bajo):
        mal.append("ni una imagen: si es landing o portfolio, falta la del hero (genérala con invoke_subagent)")
    # Velo oscuro que se come la foto: gradiente casi opaco sobre una imagen.
    if fotos:
        peor = 0.0
        for grad in re.findall(r"linear-gradient\(([^;]*)", bajo):
            for r, g, b, a in re.findall(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)", grad):
                if int(r) + int(g) + int(b) < 200:
                    peor = max(peor, float(a))
        if peor >= 0.75:
            mal.append("velo oscuro al %d%% sobre la foto: la imagen manda, dejalo en 50%% o menos" % (peor * 100))
    # Imagenes locales sin comprimir.
    base = os.path.dirname(os.path.abspath(ruta))
    for src in sorted(set(re.findall(r"""(?:src=|url\()\s*['"]?([^'")\s>]+\.(?:jpe?g|png|webp))""", h, flags=re.I))):
        f = os.path.join(base, src)
        if not src.startswith(("http", "data:")) and os.path.isfile(f) and os.path.getsize(f) > 350_000:
            mal.append("%s pesa %d KB: comprimela (foto.py de la skill web)" % (src, os.path.getsize(f) // 1000))
    # Telefonos con pinta de reales: si no los dio el usuario, son inventados.
    for tel in re.findall(r"(?<![\d.,])(?:\+34\s?)?[6789]\d{2}(?:[\s.]?\d{2,3}){3}(?![\d.,])", texto):
        if not re.fullmatch(r"(?:\+34\s?)?[6789](?:[\s.]?0)+", tel.strip()):
            mal.append("telefono %s: si el usuario no lo dio, pon 000 000 000 y avisalo en el informe" % tel.strip())
            break
    # Datos que una web estática no puede saber, y direcciones con pinta de reales.
    if re.search(r"\d{1,3}\s*°\s*\d{1,2}\s*[′']\s*\d{0,2}", texto):
        mal.append("coordenadas GPS: fuera, son decorado")
    vivo = re.search(r"\b(abierto ahora|abierto hoy|cerrado ahora|en vivo|en directo|live|pechad[ao] agora|aberto agora)\b", texto)
    if vivo:
        mal.append('dato "en vivo" inventado ("%s"): una web estática no lo sabe' % vivo.group(1))
    dire = re.search(r"\b(calle|c/|rúa|rua|avenida|avda\.?|plaza|praza|paseo)\s+(de\s+|da\s+|do\s+|del\s+|la\s+|a\s+|o\s+)*[a-záéíóúñ]+[a-záéíóúñ ]{0,25},?\s+(n[ºo°]\s*)?\d{1,3}\b", texto)
    if dire and "calle, n" not in texto:
        mal.append('dirección "%s": si no te la dio, pon "Calle, nº" y avísalo en Datos que faltan' % dire.group(0).strip())
    mal += pistas_muy_ia(h, bajo, texto)
    if not VARIAS and PORTADA(ruta):  # prototypes tiene su propia anatomia por ficha
        mal += anatomia(bajo)
    # CSS o JS gigante metido en el html: en un sitio va en css/ y js/ compartidos.
    dentro = sum(len(x) for x in re.findall(r"<(?:style|script)(?![^>]*\bsrc=)[^>]*>(.*?)</(?:style|script)>", h0, flags=re.S))
    if not VARIAS and dentro > 12000:
        mal.append("%d KB de CSS/JS dentro del html: sacalo a css/styles.css y js/main.js" % (dentro // 1000))
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
                print("· %s: el H1 tiene %d palabras; 12 como mucho (el resto va al subtitulo)" %
                      (os.path.basename(ruta), len(t.split())))
        mal, fam, foto = revisa(ruta)
        con_foto += foto
        total += len(mal)
        if len(rutas) > 1:
            print("== " + ruta)
        print("\n".join("· " + m for m in mal) if mal else "Revisor: limpio.")
        for f in fam:
            if not any(m in f for m in MONO):
                usos.setdefault(f, []).append(os.path.basename(ruta))
    # Varias versiones de una pagina: que no converjan en la misma letra.
    if VARIAS and not con_foto:
        total += 1
        print("· ninguna version lleva foto: genera 1-2 con invoke_subagent y usalas en alguna")
    for t, donde in (titulares.items() if VARIAS else []):
        if len(donde) >= 2:
            total += 1
            print('· mismo titular en %s ("%s"): cada version escribe el suyo con su VOZ' %
                  (" ".join(donde), t[:60]))
    if VARIAS and len(rutas) >= 3:
        for f, donde in sorted(usos.items()):
            if len(donde) >= 3:
                total += 1
                print("· %s sale en %d de %d (%s): cada version con su tipografia" %
                      (f, len(donde), len(rutas), " ".join(donde)))
    sys.exit(1 if total else 0)


RUTAS = sys.argv[1:] or ["index.html"]
# Varias VERSIONES de una pagina (prototypes: p1.html … p6.html) frente a varias PAGINAS de
# un mismo sitio (index, catalogo, ficha…), que si deben compartir tipografia.
VARIAS = len(RUTAS) > 1 and all(re.fullmatch(r"p\d+\.html", os.path.basename(r)) for r in RUTAS)
PORTADA = lambda r: len(RUTAS) == 1 or os.path.basename(r) == "index.html"
main(RUTAS)
