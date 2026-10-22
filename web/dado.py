#!/usr/bin/env python3
"""Dado de la skill web: una maquetacion de hero, una firma y una pareja tipografica.
Existe porque, si eliges tu, sale siempre la mediana (crema + serif + hero partido,
o titular centrado sobre fondo liso con la foto debajo)."""
import json, os, random, sys, tempfile

ESTILOS = [
    # (peso, descripcion). `suave` pesa mas: es el gusto del usuario. Mismas familias que prototypes.
    (3, "Suave: fondo de un solo tono muy claro, tarjetas blancas de radio 28, sombras amplias y tenues del mismo tono, botones pildora negros con flecha en circulo, titulares de peso 500"),
    (2, "Minimal: blanco o gris 98 %, tinta casi negra y ningun acento; widgets blancos y titulares de peso 500; el catalogo, muy limpio"),
    (2, "Lienzo enmarcado: la pagina dentro de un lienzo de radio 36 separado 16px del borde sobre un fondo de color apagado; la foto del hero va dentro del lienzo"),
    (2, "Fotografico: una foto enorme manda; texto blanco encima y un widget de vidrio con datos reales"),
    (1, "Liquid glass: foto viva detras y paneles de vidrio translucido con brillo especular arriba; monocromo encima, sin glows"),
    (1, "Nothing (como la app Nothing X): negro con tarjetas #1b1b1b de radio 20, titulares finos, cifras finas con barra (7/40), etiquetas en mono mayusculas; sin fuente de puntos y el rojo en un solo detalle"),
    (1, "Estudio oscuro: foto o render oscuro con luz de estudio de fondo, secciones en negro plano, titulares blancos; la luz la pone la imagen, nunca el CSS"),
]
HEROS = [
    # Todos con la foto DE FONDO y la informacion en widgets encima (Kumo, Ranty, Golfair).
    # Ninguno es mitad texto / mitad imagen ni texto sobre un fondo liso.
    "Lienzo redondeado con margen y la foto de fondo dentro; objeto del negocio en el centro, 3-4 fichas cuadradas de vidrio flotando a sus lados (variantes, sabores, modelos) y el titular abajo, pisando la foto",
    "Foto de paisaje o del sitio a pantalla completa; titular grande arriba a la izquierda; a la derecha una tarjeta blanca con una miniatura, dos chips y una frase; abajo a la izquierda una tarjeta con foto pequena y abajo a la derecha un dato grande (12 m², 9 meses) con su etiqueta",
    "Foto a sangre de 100svh con velo solo abajo; titular abajo a la izquierda y, abajo a la derecha, un widget de vidrio con el producto destacado (foto, nombre, precio, boton)",
    "Foto de fondo con una barra de busqueda o de filtros de vidrio centrada (3 selectores reales del catalogo y un boton) y el titular encima; dos tarjetitas en las esquinas",
    "Foto de fondo en lienzo con margen; nav de vidrio dentro; un control segmentado de vidrio arriba que cambia la foto de fondo (3-4 opciones reales) y el titular centrado abajo",
    "Foto de fondo con el producto; 3 etiquetas finas con linea que senalan partes del producto (material, medida, detalle) y el titular grande abajo a la izquierda",
]
FIRMAS = [
    "Cinta (marquee) lenta con nombres de servicios o piezas del negocio, nunca cifras",
    "Imagen que se revela con clip-path al entrar en pantalla (animation-timeline: view())",
    "La imagen del hero empieza como tarjeta con margen y se expande a sangre al hacer scroll",
    "Un parrafo grande que se enciende palabra a palabra con el scroll",
    "Seccion sticky: la imagen se queda fija mientras el texto pasa a su lado",
    "Fila horizontal con scroll-snap para la carta, el catalogo o los proyectos",
    "Fuente variable que cambia de peso o anchura al pasar el raton o con el scroll",
    "Cada seccion cambia el color de fondo de toda la pagina al entrar en ella",
    "Lista (carta, servicios) que al pasar el raton muestra una imagen flotante",
    "Reticula visible de lineas finas como elemento grafico de toda la pagina",
    "Grano de papel SVG muy sutil sobre fondos planos y un color de acento saturado",
]
TIPOS = [
    "General Sans (Fontshare) 300 en titulares grandes + 400 en texto",
    "Satoshi (Fontshare) 300-500",
    "Urbanist 300 en titulares + Manrope en texto",
    "Switzer (Fontshare) 300 en titulares + Geist Mono en datos",
    "Bricolage Grotesque (titulares) + Instrument Sans (texto)",
    "Instrument Serif (titulares muy grandes) + Geist (texto)",
    "Archivo con anchura expandida (wdth 125) para titulares + Archivo normal",
    "Big Shoulders Display (titulares) + IBM Plex Sans (texto)",
    "Familjen Grotesk (titulares) + Fragment Mono (datos y etiquetas)",
    "Gloock (titulares) + Figtree (texto)",
    "Young Serif (titulares) + Onest (texto)",
    "Schibsted Grotesk (titulares) + Libre Caslon Text (texto)",
    "Unbounded (titulares) + Manrope (texto)",
    "Syne (titulares) + Space Mono (datos y etiquetas)",
]

hist = os.path.join(tempfile.gettempdir(), "web-frontend-dado.json")
try:
    ultimo = json.load(open(hist))
except Exception:
    ultimo = {}
elegido = {"estilo": random.choices([e for _, e in ESTILOS], [w for w, _ in ESTILOS])[0]}
for clave, lista in (("hero", HEROS), ("firma", FIRMAS), ("tipos", TIPOS)):
    opciones = [x for x in lista if x != ultimo.get(clave)] or lista
    elegido[clave] = random.choice(opciones)
try:
    json.dump(elegido, open(hist, "w"))
except Exception:
    pass
print("ESTILO: " + elegido["estilo"])
print("HERO:  " + elegido["hero"])
print("FIRMA: " + elegido["firma"])
print("TIPOS: " + elegido["tipos"])
