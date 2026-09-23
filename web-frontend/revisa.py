#!/usr/bin/env python3
"""AI-tell linter for an html file. Usage: revisa.py index.html
What the skill bans still gets written if nobody checks it: this checks it."""
import re, sys

FRASES = ["sin prisa", "con calma", "honest", "artesan", "de la finca a la taza", "te mereces",
          "experiencia única", "experiencia unica", "pasión por", "pasion por", "descubre",
          "implacable", "a otro nivel", "sin rodeos", "de confianza", "calidad premium",
          "hecho con amor", "tu mejor aliado", "soluciones integrales", "cercanía",
          # English
          "unhurried", "artisan", "farm to cup", "you deserve", "unique experience",
          "passion for", "discover", "elevate", "relentless", "no-nonsense", "next level",
          "seamless", "unlock", "world-class", "cutting-edge", "crafted with love"]
FUENTES = ["Inter:", "Inter&", "DM+Sans", "Plus+Jakarta", "Poppins", "Montserrat", "Fraunces",
           "Playfair", "Newsreader"]
VIVO = [r"abiert[oa] (hoy|ahora)", r"en proceso", r"turnos? libres?", r"plazas? libres?",
        r"estado:", r"\d+\.\d{3,}°", r"en directo", r"\blive\b",
        r"open (now|today)", r"in progress", r"slots? (left|available)", r"status:"]

def main(ruta):
    h = open(ruta, encoding="utf-8", errors="replace").read()
    bajo = h.lower()
    texto = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", bajo, flags=re.S)
    texto = re.sub(r"<[^>]+>", " ", texto)
    mal = []
    for f in FRASES:
        if f in texto:
            mal.append('stock phrase: "%s" -> write a concrete fact' % f)
    for f in FUENTES:
        if f.lower() in bajo:
            mal.append("default font: %s -> use the die's" % f.strip(":&").replace("+", " "))
    for p in VIVO:
        m = re.search(p, texto)
        if m:
            mal.append('made-up "live" data: "%s" -> a static page cannot know that' % m.group(0))
    if re.search(r"(border-radius:\s*50%|rounded-full)[^}]*(#(22c55e|10b981|4ade80|16a34a)|green)", bajo):
        mal.append("green 'open' dot: remove it")
    cejas = len(re.findall(r"text-transform:\s*uppercase[^}]*letter-spacing|letter-spacing[^}]*text-transform:\s*uppercase", bajo))
    if cejas > 3:
        mal.append("%d spaced UPPERCASE styles: keep one at most" % cejas)
    for tag in re.findall(r"<img\b[^>]*>", bajo):
        if 'alt="' not in tag or "width" not in tag:
            mal.append("img without alt or width/height: " + tag[:60])
            break
    secciones = len(re.findall(r"<section\b", bajo))
    if secciones > 6:
        mal.append("%d sections: a landing needs 4-5" % secciones)
    for f in re.findall(r"<form\b", bajo)[:1]:
        mal.append("there is a <form>: if nobody asked for it, use phone/email/link instead")
    if len(h) > 32000:
        mal.append("%d KB: there is content nobody asked for" % (len(h) // 1000))
    print("\n".join("· " + m for m in mal) if mal else "Linter: clean.")

main(sys.argv[1] if len(sys.argv) > 1 else "index.html")
