#!/usr/bin/env python3
"""comparar.py — genera comparar.html con los p*.html de la carpeta y las fichas del dado.

Uso: python3 comparar.py   (en la carpeta de los prototipos, después de dado.py)

Los iframes se escalan con `zoom` sobre un viewport fijo, nunca con transform: scale():
con transform el iframe se maqueta al ancho de la tarjeta y enseña la versión móvil.
"""
import glob, html, json, os

try:
    datos = json.load(open("fichas.json", encoding="utf-8"))
except Exception:
    datos = {"tipo": "landing", "encargo": "", "fichas": []}
fichas = datos.get("fichas", [])
tipo = datos.get("tipo", "landing")
VW, VH = (1440, 900) if tipo == "panel" else (1280, 1000)

protos = sorted(glob.glob("p[0-9].html"))
if not protos:
    raise SystemExit("no hay p1.html … p6.html en esta carpeta")

tarjetas = []
for i, ruta in enumerate(protos):
    f = fichas[i] if i < len(fichas) else {}
    pal = f.get("paleta") or []
    filas = [("Concepto", f.get("concepto")), ("Estructura", f.get("estructura")),
             ("Voz", f.get("voz")), ("Estilo", f.get("estilo")),
             ("Hero", f.get("hero") or f.get("composicion")), ("Nav", f.get("nav")),
             ("Movimiento", f.get("movimiento")),
             ("Paleta", " · ".join("<code>%s</code>" % html.escape(c) for c in pal[:3]) if pal else None)]
    ing = "".join('<div class="fila"><span>%s</span><b>%s</b></div>' % (k, v if k == "Paleta" else html.escape(str(v)))
                  for k, v in filas if v)
    tarjetas.append("""
  <article class="tarjeta">
    <header><span class="n">P%d</span><span class="nombre">%s</span>
      <a href="%s" target="_blank">Abrir ↗</a>
      <button class="tema" onclick="tema(%d)" aria-label="Cambiar tema">◐</button></header>
    <div class="marco"><iframe src="%s" loading="lazy" scrolling="no" title="P%d"></iframe></div>
    <div class="ing">%s</div>
  </article>""" % (i + 1, html.escape(f.get("nombre") or os.path.splitext(ruta)[0]), ruta, i, ruta, i + 1, ing))

pagina = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prototipos · %(encargo)s</title>
<style>
  :root { --fondo:#f4f4f2; --tinta:#111; --gris:#6b6b6b; }
  * { box-sizing:border-box }
  body { margin:0; background:var(--fondo); color:var(--tinta); font:14px/1.5 system-ui, sans-serif; }
  .cab { display:flex; align-items:center; gap:16px; padding:24px 28px 8px; }
  .cab h1 { font-size:18px; font-weight:600; margin:0; letter-spacing:-.01em; }
  .cab p { margin:0; color:var(--gris); flex:1; }
  .cab button, .tema { border:0; background:#111; color:#fff; border-radius:999px; padding:8px 14px; cursor:pointer; font:inherit; }
  .rejilla { display:grid; gap:20px; padding:16px 28px 40px; grid-template-columns:repeat(3, minmax(0,1fr)); }
  @media (max-width:1350px) { .rejilla { grid-template-columns:repeat(2, minmax(0,1fr)); } }
  @media (max-width:760px) { .rejilla { grid-template-columns:1fr; padding:12px; } }
  .tarjeta { background:#fff; border-radius:20px; overflow:hidden; box-shadow:0 1px 3px rgb(0 0 0 / .06), 0 24px 48px -24px rgb(0 0 0 / .12); }
  .tarjeta header { display:flex; align-items:center; gap:10px; padding:12px 14px; }
  .n { font-weight:600; } .nombre { flex:1; color:var(--gris); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .tarjeta a { color:var(--tinta); text-decoration:none; white-space:nowrap; }
  .tema { width:32px; height:32px; padding:0; font-size:17px; line-height:1; }
  .marco { width:100%%; overflow:hidden; background:#fff; }
  .marco iframe { display:block; width:%(vw)dpx; height:%(vh)dpx; border:0; zoom:var(--z,1); pointer-events:none; }
  .ing { display:grid; grid-template-columns:1fr 1fr; gap:4px 12px; padding:12px 14px 16px; font-size:12px; }
  .fila { display:flex; justify-content:space-between; gap:8px; border-top:1px solid #eee; padding-top:4px; }
  .fila span { color:var(--gris); } .fila b { font-weight:500; text-align:right; }
  code { font-size:11px; }
</style></head>
<body>
<div class="cab"><h1>Seis direcciones</h1><p>%(encargo)s</p><button onclick="todos()">◐ Cambiar tema a los seis</button></div>
<main class="rejilla">%(tarjetas)s
</main>
<script>
  const VW = %(vw)d, VH = %(vh)d;
  function escala() {
    document.querySelectorAll('.marco').forEach(m => {
      const z = m.clientWidth / VW;
      m.style.setProperty('--z', z);
      m.style.height = Math.round(VH * z) + 'px';
    });
  }
  escala(); addEventListener('load', escala); addEventListener('resize', escala);
  new ResizeObserver(escala).observe(document.documentElement);
  function tema(i) {
    try { document.querySelectorAll('iframe')[i].contentWindow.toggleTheme(); } catch (e) { console.warn('P' + (i+1) + ' sin toggleTheme()'); }
  }
  function todos() { document.querySelectorAll('iframe').forEach((_, i) => tema(i)); }
</script>
</body></html>
""" % {"encargo": html.escape(datos.get("encargo") or ""), "tarjetas": "".join(tarjetas), "vw": VW, "vh": VH}

open("comparar.html", "w", encoding="utf-8").write(pagina)
print("comparar.html con %d prototipos (viewport %dx%d)" % (len(protos), VW, VH))
