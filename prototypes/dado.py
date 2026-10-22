#!/usr/bin/env python3
"""Dado de prototypes: seis direcciones clean, distintas entre si, sacadas de Dribbble.
Uso:  dado.py "<encargo>"  [--tipo landing|movil|panel] [--evitar x,y] [--solo x]
                           [--repetir] [--semilla txt] [--listar]

Por que existe: si eliges tu, las seis salen iguales (la mediana del entrenamiento) o
caen en lo que el usuario odia: hero partido texto/imagen, palabra clave en otro color,
fila de cifras, brillos de colores. Aqui la direccion la pone el dado.
Y no basta con la piel: cada ficha trae tambien CONCEPTO, ESTRUCTURA y VOZ, para que sean
seis ideas distintas y no seis colores del mismo esqueleto."""
import argparse, json, os, random, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
HISTORIAL = os.path.join(AQUI, ".historial.json")

# ------------------------------------------------------------------------------
# ESTILOS. peso = cuanto le gusta al usuario. `suave` sale siempre.
# Cada uno trae su paleta (base · superficie · tinta · acento), tipografias y la
# trampa en la que cae la IA al intentarlo.
# ------------------------------------------------------------------------------
ESTILOS = {
    "suave": dict(
        peso=0, nombre="Suave (SphereAI, Nuve)",
        idea="Fondo de UN tono muy claro, tarjetas blancas de radio 28, sombras amplias y "
             "tenues tenidas del tono, botones pildora negros con flecha en circulo. "
             "DENSA en contenido: foto o render protagonista, 2-3 micro-tarjetas flotando "
             "con datos reales, y debajo un bento de 5-7 tarjetas con UI de verdad (listas, "
             "graficas, toggles, fotos). Es el estilo favorito del usuario: nunca vacio.",
        paletas=[("#eef3fb hielo", "#ffffff", "#0e1726", "#2a5bd7"),
                 ("#f3f0fa lila", "#ffffff", "#17131f", "#6d4ee0"),
                 ("#eef2ee salvia", "#ffffff", "#131a14", "#3d7a52")],
        oscuro="#0d111a · rgba(255,255,255,.06) · #eef2f8 · el acento un 20 % mas claro",
        tipos=["Satoshi 500 (titulares, tracking -0.03em) + Satoshi 400",
               "Outfit 500 + Figtree 400", "Google Sans Flex 500 + Google Sans Flex 400"],
        trampa="Quedarse vacio (un titular y cuatro cajas) o meter blobs difuminados de colores. "
               "El fondo es plano, la profundidad la dan las sombras tenidas y el contenido llena.",
        imagen="soft 3D render o foto de producto con luz difusa, fondo del mismo tono que la pagina",
        navs=["pildora-centro", "minimal", "isla-vidrio"]),
    "minimal": dict(
        peso=3, nombre="Minimal (Twinkle, AI Startups)",
        idea="Blanco o gris 98 %, tinta casi negra, SIN color de acento (el negro es el acento). "
             "Titular centrado de peso 500 con tracking negativo, mucho aire, y una sola "
             "imagen grande en tarjeta redondeada que lleva el color de toda la pagina.",
        paletas=[("#ffffff blanco", "#f5f5f4", "#0a0a0a", "#0a0a0a"),
                 ("#f7f7f5 gris calido", "#ffffff", "#111111", "#111111")],
        oscuro="#0a0a0a · #161616 · #f5f5f5 · #f5f5f5",
        tipos=["Geist 500 + Geist 400", "Hanken Grotesk 500 + Hanken Grotesk 400",
               "Switzer 500 + Switzer 400", "Onest 500 + Onest 400"],
        trampa="Vaciarla hasta que no dice nada. Minimal es pocas piezas, no ninguna: "
               "la demo del producto o la foto tienen que estar.",
        imagen="foto luminosa del encargo, mucho aire, colores suaves y naturales",
        navs=["pildora-centro", "minimal"]),
    "liquid-glass": dict(
        peso=3, nombre="Liquid Glass (Apple, iOS 26)",
        idea="Siempre hay una foto o un color vivo DETRAS y el vidrio la deja ver: paneles con "
             "backdrop-filter: blur(24px) saturate(180%), fondo rgba(255,255,255,.18), borde de "
             "1px rgba(255,255,255,.5) y un brillo especular arriba (box-shadow inset 0 1px 0 "
             "rgba(255,255,255,.7)). Monocromo encima: blanco y negro.",
        paletas=[("foto a sangre", "rgba(255,255,255,.18)", "#ffffff", "#ffffff"),
                 ("#e9ecf1 perla", "rgba(255,255,255,.55)", "#0b0b0c", "#0b0b0c")],
        oscuro="#000 · rgba(255,255,255,.08) · #fff · #fff",
        tipos=["Geist 500 + Geist 400", "Google Sans Flex 500 + 400"],
        trampa="Vidrio sobre fondo liso (no se ve nada) o con resplandores de colores detras. "
               "Sin glows, sin bordes de neon: el vidrio solo existe encima de una imagen.",
        imagen="foto de ambiente con color y profundidad (paisaje, interior, producto en uso) para ponerla detras del vidrio",
        navs=["isla-vidrio", "pildora-centro"]),
    "nothing": dict(
        peso=3, nombre="Nothing X (app actual, capturas App Store 2025)",
        idea="Como la app Nothing X: fondo negro puro, tarjetas #1b1b1b de radio 20 en rejilla "
             "de 2 columnas (tarjeta ancha arriba, dos medianas debajo). Titulares de pantalla en "
             "SERIFA FINA ('My dashboard', 'Equaliser') a 28-34px. Grupos de 3 botones redondos "
             "dentro de una tarjeta: el activo relleno blanco con icono negro, los demas #2a2a2a. "
             "Cifras finas con barra ('7/40', '715/300', '72/40'), etiquetas pequenas grises. "
             "Filas de lista con icono, nombre, valor a la derecha y chevron. Controles "
             "segmentados en pildora (Simple · Advanced, W · M · Y) con el activo en blanco. "
             "Graficas de COLUMNAS DE PUNTOS (puntos blancos/grises, el de arriba rojo), un anillo "
             "de progreso tipo pista (blanco y rojo) y un dial circular. Foto de producto en B/N o "
             "sobre gris claro, centrada y grande.",
        paletas=[("#000000 negro", "#1b1b1b", "#ffffff", "#d71921 (anillo, punto activo o UN boton)")],
        oscuro="ARRANCA en negro; toggleTheme() pasa a #e8e8e8 · #fff · #000",
        tipos=["Spectral 300 (titulares finos) + Geist 400 (UI)",
               "Source Serif 4 300 (titulares) + Hanken Grotesk 400 (UI)"],
        trampa="La fuente de puntos (la usa Nothing en su marketing, al usuario no le gusta) y el "
               "rojo por todas partes. El rojo va en el anillo, el punto activo o un solo boton. "
               "Nada de cintas ni carruseles de cifras: las cifras viven dentro de su tarjeta.",
        imagen="foto en B/N con mucho contraste: el producto fisico sobre negro o, si es una app, la mano con el movil en la escena de uso; la UI encima en tarjetas #1b1b1b",
        navs=["minimal", "mono-mayusculas"]),
    "lienzo": dict(
        peso=3, nombre="Lienzo enmarcado (Kumo, Finix, Redrx)",
        idea="La pagina vive DENTRO de un lienzo de radio 32-40 separado 16-24px del borde, "
             "sobre un fondo de color apagado sacado del producto. El hero es una pantalla "
             "con un objeto protagonista en el centro. Un color de fondo, uno de tinta.",
        paletas=[("#a3a35e oliva (fondo exterior)", "#2f3a24", "#f3efe2", "#f3efe2"),
                 ("#6b7280 pizarra (fondo exterior)", "#e7e8ea", "#0d0d0d", "#0d0d0d"),
                 ("#c9b8a8 arcilla (fondo exterior)", "#f4f1ee", "#1a1512", "#1a1512")],
        oscuro="el lienzo pasa a #121212 y el fondo exterior se oscurece un 60 %",
        tipos=["Zodiak 700 (titular) + Supreme 400", "Cabinet Grotesk 500 + Supreme 400",
               "Chillax 500 + Onest 400"],
        trampa="Olvidar el margen: sin el hueco alrededor ya no es un lienzo, es una web normal.",
        imagen="el objeto del encargo protagonista, sobre un pedestal o monticulo de su propia materia, fondo de color apagado, luz de estudio",
        navs=["segmentada-iconos", "minimal"]),
    "estudio": dict(
        peso=2, nombre="Estudio oscuro (Fineo, Liquid Brokers)",
        idea="Negro #0a0a0b y un unico render u objeto con luz de estudio: la luz la trae la "
             "IMAGEN, no el CSS. Titular centrado blanco de peso 500, CTA pildora blanca, "
             "dos micro-tarjetas oscuras flotando junto al objeto.",
        paletas=[("#0a0a0b negro", "#151517", "#f5f5f5", "#f5f5f5"),
                 ("#0b0c10 negro azulado", "#15171d", "#eef0f6", "#eef0f6")],
        oscuro="ARRANCA en negro; toggleTheme() pasa a #f4f4f5 con el render sobre gris",
        tipos=["Author 500 + Author 400", "Clash Display 500 + Supreme 400",
               "Geist 500 + Geist Mono"],
        trampa="Glows de colores, degradados morados y estrellitas. Nada de text-shadow ni "
               "box-shadow de color: el negro es plano y el objeto brilla solo.",
        imagen="render 3D del objeto o de un material (cinta, esfera, metal) sobre negro, luz de borde, casi monocromo; NUNCA degradado morado/azul/rosa",
        navs=["minimal", "pildora-centro"]),
    "editorial": dict(
        peso=2, nombre="Editorial de producto (MarkOne)",
        idea="Blanco frio o gris perla, titular Didone enorme y fino, fotos de producto "
             "RECORTADAS sin fondo con sombra suave, un bloque negro a sangre para romper "
             "el ritmo y un boton circular con texto en orbita.",
        paletas=[("#fafafa blanco", "#ffffff", "#111111", "#111111"),
                 ("#f1f1ef perla", "#ffffff", "#141414", "#141414")],
        oscuro="#0f0f0f · #1a1a1a · #f2f2f2 · #f2f2f2",
        tipos=["Bodoni Moda 400 (titulares) + Hanken Grotesk 400", "Gloock 400 + Geist 400"],
        trampa="Fondo crema + serifa: es la plantilla que delata a la IA. Aqui el fondo es "
               "blanco frio o perla, nunca crema.",
        imagen="el producto recortado sobre blanco puro, sombra de contacto suave, luz lateral",
        navs=["minimal", "pildora-centro"]),
    "suizo": dict(
        peso=2, nombre="Tipografico suizo (retícula)",
        idea="Blanco, reticula de 12 columnas que se nota en como se alinea todo, texto enorme "
             "alineado a la izquierda como si fuera la imagen, filetes de 1px, numeros de "
             "seccion (01, 02...) y UNA foto grande encajada en la reticula (ocupa columnas enteras, a sangre por un lado, el titular la pisa). Negro y un acento puro en UN detalle.",
        paletas=[("#ffffff blanco", "#f2f2f2", "#0a0a0a", "#0038ff azul Klein"),
                 ("#f3f3f3 gris", "#ffffff", "#111111", "#ff3b00 naranja senal")],
        oscuro="#0b0b0b · #161616 · #f2f2f2 · el acento igual",
        tipos=["Instrument Sans 600 + Instrument Sans 400", "Schibsted Grotesk 600 + Schibsted Grotesk 400",
               "Archivo 500 + Archivo 400"],
        trampa="Collage de poster abarrotado. Suizo es orden: mucho blanco, reticula estricta, "
               "el acento solo en un sitio.",
        imagen="foto documental EN COLOR del objeto o del sitio, precisa, luz neutra, colores naturales; nunca B/N ni filter: grayscale (al usuario no le gusta aqui)",
        navs=["mono-mayusculas", "minimal"]),
}

# ------------------------------------------------------------------------------
# HEROS de landing. Ninguno es mitad texto / mitad imagen.
# ------------------------------------------------------------------------------
HEROS = {
    "fondo-completo": "UNA foto a sangre que llena TODA la ventana (100vw x 100svh, sin margen ni tarjeta), "
                      "velo oscuro solo abajo, nav blanca encima, titular corto abajo a la izquierda y 1-2 "
                      "widgets de vidrio con datos reales del encargo (Golfair).",
    "lienzo-pantalla": "Pantalla redondeada con margen sobre un fondo del tono de la foto; la foto o render a "
                       "sangre dentro, la nav dentro y el titular grande abajo, centrado, SOBRE la imagen (Kumo).",
    "objeto-orbita": "El objeto enorme en el centro sobre su propia materia (un monticulo, un pedestal) y 3-5 "
                     "fichas cuadradas redondeadas flotando alrededor con rotaciones distintas, cada una con "
                     "un ingrediente o pieza; titular abajo sobre la imagen (Kumo).",
    "centrado-objeto": "Titular centrado arriba (2 lineas, peso 500, tracking -0.03em) y CTA pildora; debajo, "
                       "el objeto ENORME saliendo por el borde inferior, cortado, con 2 tarjetitas de vidrio "
                       "a los lados con un dato cada una (Liquid Brokers).",
    "retrato-anotado": "La foto centrada a toda la altura (objeto o escena de uso, recortada sobre el fondo) "
                       "con 3-4 recuadros finos de UI anotando puntos concretos; titular corto abajo a la "
                       "izquierda PISANDO la foto. Sin cifras en fila ni en columna (Nuve).",
    "masivo-recorte": "Una palabra gigante a todo el ancho EN TINTA PLENA (nunca gris palido de fondo) y el objeto "
                      "recortado DELANTE tapando parte de las letras (Vision Pro). Titular real pequeno debajo.",
    "centrado-demo": "Titular centrado + control segmentado de 3-4 pestanas reales + la UI del producto "
                     "en una tarjeta redondeada apoyada sobre una foto a sangre (Twinkle). Las pestanas cambian la UI.",
}
# Donde queda el titular. Mas de dos "centro" en la misma tirada y los seis parecen el mismo.
POSICION = {"centrado-objeto": "centro", "centrado-demo": "centro", "objeto-orbita": "abajo",
            "lienzo-pantalla": "abajo", "fondo-completo": "abajo", "retrato-anotado": "abajo",
            "masivo-recorte": "gigante"}
MAX_POSICION = {"centro": 2, "abajo": 4, "gigante": 1}
# Siempre hay uno con la foto de fondo entera (lo pidio el usuario).
OBLIGADO = "fondo-completo"
# Que encuadre necesita la foto segun el hero (se suma a la linea FOTO del estilo).
ENCUADRE = {
    "fondo-completo": "horizontal 16:9, escena amplia del encargo con sitio libre abajo a la izquierda para el titular",
    "lienzo-pantalla": "horizontal, el objeto o la escena centrados con aire alrededor",
    "objeto-orbita": "el objeto centrado sobre un monticulo o pedestal de su materia, fondo liso",
    "centrado-objeto": "el objeto grande visto de frente, fondo liso del color de la pagina, que se pueda cortar por abajo",
    "retrato-anotado": "vertical, un solo objeto o escena de uso sobre fondo liso claro, con detalles que se puedan senalar",
    "masivo-recorte": "el objeto aislado sobre fondo liso (se recorta con mix-blend-mode o mascara)",
    "centrado-demo": "horizontal, escena amplia y tranquila del encargo donde se apoya una tarjeta de UI",
}

# Que heros casan con cada estilo (el resto chocan: un Didone no va con una demo de SaaS).
HEROS_DE = {
    "suave": ["centrado-objeto", "centrado-demo", "objeto-orbita", "lienzo-pantalla", "retrato-anotado", "fondo-completo"],
    "minimal": ["centrado-demo", "centrado-objeto", "masivo-recorte", "retrato-anotado", "fondo-completo"],
    "liquid-glass": ["fondo-completo", "lienzo-pantalla", "centrado-demo"],
    "nothing": ["masivo-recorte", "centrado-objeto", "objeto-orbita", "retrato-anotado"],
    "lienzo": ["lienzo-pantalla", "objeto-orbita"],
    "estudio": ["centrado-objeto", "objeto-orbita", "masivo-recorte", "fondo-completo"],
    "editorial": ["masivo-recorte", "fondo-completo", "retrato-anotado", "centrado-objeto"],
    "suizo": ["fondo-completo", "masivo-recorte", "retrato-anotado", "lienzo-pantalla"],
}

# ------------------------------------------------------------------------------
# LO QUE DE VERDAD LOS SEPARA. Sin esto salen seis pieles del mismo esqueleto
# (mismo titular, mismas secciones, mismo boton). Cada prototipo es una IDEA.
# ------------------------------------------------------------------------------
CONCEPTOS = {
    "despiece": ("La cosa por dentro: la pagina desmonta el producto o el servicio en sus piezas y "
                 "cada seccion es una pieza.", "puntos sobre el objeto que al pulsarlos abren su pieza"),
    "configurador": ("La web es una herramienta: el visitante elige 2-3 opciones y ve al momento el "
                     "resultado y un precio o plazo orientativo.", "controles segmentados que recalculan en vivo"),
    "documento": ("La pagina imita un documento del oficio (parte de trabajo, receta, ficha tecnica, "
                  "billete, carta) con su maquetacion y sus campos.", "casillas que se marcan o campos que se rellenan"),
    "antes-despues": ("Todo gira en torno a la transformacion: como llega y como sale.",
                      "deslizador arrastrable antes/despues"),
    "recorrido": ("Un proceso de principio a fin (llegas, diagnostico, arreglo, recoges), una escena por paso.",
                  "barra de progreso pulsable que salta entre pasos"),
    "catalogo": ("Un indice explorable de lo que ofrece, como un archivo o una carta.",
                 "filtros en pildora que reordenan las fichas con transicion"),
    "pregunta": ("Empieza preguntando al visitante y le ensena lo que le toca (2-3 preguntas y una recomendacion).",
                 "mini quiz con resultado"),
    "manifiesto": ("Un texto corto y con opinion es el protagonista; el resto de la pagina le da la razon.",
                   "el texto se enciende al hacer scroll y un detalle se revela al final"),
    "vitrina": ("Un solo objeto grande que cambia de angulo o de estado mientras bajas; todo el "
                "contenido aparece a su alrededor.", "el objeto rota o cambia de estado con el scroll"),
    "plano": ("Un plano o diagrama dibujado en SVG propio (el local, el sistema, el recorrido) es el mapa "
              "de toda la pagina.", "puntos del plano que se abren al pasar o pulsar"),
}
# Lo que el CONCEPTO pone en la primera pantalla, ENCIMA de la imagen del HERO. La imagen
# manda (asi son todas sus referencias de Dribbble); sin ella salen seis maquetas de texto.
ARRANQUE = {
    "despiece": "3-4 etiquetas finas con su linea senalando piezas reales sobre la imagen; al pulsar abren la pieza",
    "configurador": "una tarjeta flotante con 2-3 controles segmentados encima de la imagen; al cambiar cambian la imagen, el precio o el plazo",
    "documento": "una ficha de papel pequena (numero, fecha, 3 campos) apoyada sobre la imagen, algo girada",
    "antes-despues": "la propia imagen es el deslizador: un lado antes, el otro despues, arrastrable",
    "recorrido": "una barra de progreso de 4 pasos sobre la imagen; el paso 1 es el titular",
    "catalogo": "bajo el titular, 3-4 pildoras de filtro sobre la imagen que ya filtran la seccion siguiente",
    "pregunta": "la primera pregunta en una tarjeta flotante sobre la imagen, con 3 respuestas en pildora",
    "manifiesto": "la primera frase del manifiesto como titular sobre la imagen; el resto se enciende al bajar",
    "vitrina": "la imagen es el objeto enorme; solo el titular corto",
    "plano": "puntos del plano sobre la imagen (vista cenital del local o del objeto) que se abren al pulsar",
}

ESTRUCTURAS = {
    "capitulos": "4-5 capitulos a pantalla completa, numerados, con scroll-snap suave.",
    "horizontal": "Tras el hero, una seccion sticky que avanza en HORIZONTAL con el scroll y lleva el grueso del contenido.",
    "una-pantalla": "Casi todo cabe en 100vh: un escenario fijo que cambia de estado con pestanas o pasos; poco scroll.",
    "indice-lateral": "Hero a todo el ancho; despues, un indice fijo a la izquierda y el contenido corriendo a la derecha.",
    "apiladas": "Tarjetas casi a pantalla completa que se apilan (sticky) una encima de otra al bajar.",
    "articulo": "Un reportaje: columna estrecha de ~680px con figuras e interactivos intercalados a mas ancho.",
    "tablero": "Despues del hero, la pagina entera es una sola rejilla bento explorable, sin secciones clasicas.",
}
VOCES = {
    "tecnico": "Preciso y del oficio: datos concretos, frases cortas, sin adjetivos vacios. "
               "H1 con una cifra o un termino del oficio.",
    "cercano": "De tu, como hablaria el dueno en el mostrador; calido y sin chistes. "
               "H1 en segunda persona ('Tu ...', 'Traela ...').",
    "seco": "Casi nada de texto; deja hablar a la imagen. H1 de 1-3 palabras, sin verbo.",
    "narrativo": "Cuenta una historia (la de un cliente o la de una pieza) de principio a fin. "
                 "H1 como el arranque de una historia, en pasado o con un momento concreto.",
    "instrucciones": "Imperativos y pasos numerados, como un buen manual. H1 en imperativo.",
    "preguntas": "Los titulares son las preguntas que se hace el visitante y el texto las "
                 "responde. H1 entre signos de interrogacion.",
}

NAVS = {
    "pildora-centro": "Logo a la izquierda, 3-4 enlaces dentro de una pildora centrada, CTA pildora negra a la derecha.",
    "minimal": "Logo a la izquierda, enlaces pequenos (13px) centrados sin caja, CTA de texto con flecha.",
    "isla-vidrio": "Isla de vidrio flotante y compacta, centrada, con logo + enlaces + CTA dentro.",
    "segmentada-iconos": "Control segmentado de iconos en el centro (Material Symbols), logo a la izquierda y un boton redondo a la derecha.",
    "mono-mayusculas": "Marca y 3-4 enlaces en mono mayusculas de 11px, espaciados, sin caja; CTA pildora a la derecha.",
}

FIRMAS = {
    "bento": "Rejilla bento: tarjetas de radio 24 de tamanos distintos (2x1, 1x1, 1x2), cada una con algo "
             "dentro (una grafica, una foto, un trozo de UI). Nunca cuatro cifras en fila.",
    "carrusel-fotos": "Fila horizontal con scroll-snap de tarjetas altas de foto (radio 24) con la info en una "
                      "franja de vidrio abajo y un boton que aparece al pasar el raton (Golfair).",
    "tabs-demo": "Control segmentado que cambia una maqueta de la UI o del servicio (JS minimo, "
                 "transicion de 250 ms).",
    "sticky-pasos": "Una imagen o maqueta sticky mientras 3-4 pasos pasan por su lado; la imagen cambia "
                    "con el paso visible.",
    "lista-filas": "Lista de filas grandes con chevron (servicios, carta, planes); al pasar el raton la "
                   "fila se abre o muestra una miniatura.",
    "linea-estados": "Linea vertical de pasos con chips de estado (Hecho, En curso, Pendiente) y una "
                     "tarjeta de detalle al lado (AI Startups).",
    "galeria-recortes": "Productos o piezas recortados sin fondo sobre tarjetas blancas identicas, con "
                        "nombre y dato real; un boton centrado debajo.",
    "movil-mock": "Un telefono con pantallas reales de la app o del servicio; al hacer scroll cambia la "
                  "pantalla que muestra.",
}

MOVIMIENTOS = {
    "revelar": "Cada bloque entra con opacity + translateY(24px) usando animation-timeline: view() "
               "(animation-range: entry 0% cover 30%).",
    "zoom-lienzo": "La imagen del hero empieza como tarjeta con margen y se expande a sangre al hacer "
                   "scroll (scale o clip-path con animation-timeline: scroll()).",
    "parallax-capas": "El objeto y las micro-tarjetas se mueven a velocidades distintas con el scroll "
                      "(translateY con animation-timeline: view()).",
    "texto-progresivo": "Un parrafo grande de manifiesto que se 'enciende' palabra a palabra con el "
                        "scroll (opacity .2 -> 1 por span, animation-timeline: view()).",
    "sticky-cambio": "Una seccion sticky donde la imagen hace crossfade al cambiar de paso.",
}

# Para apps moviles y paneles no hay hero: hay composicion de pantallas.
MOVIL = {
    "tres-pantallas": "Tres pantallas de 390x844 en fila sobre un fondo neutro, la del centro un poco mas alta (como un shot de Dribbble).",
    "flujo": "Tres pantallas de un mismo flujo (elegir, cargando, resultado) con la del medio en primer plano (quiz de belleza).",
    "inclinadas": "Cinco o seis pantallas inclinadas 30 grados en mosaico, recortadas por los bordes (banco lima).",
}
PANEL = {
    "bento-panel": "Panel de 1440 con saludo, rejilla bento de widgets de radio 24 y una columna de actividad (Crextio).",
    "sidebar-clasico": "Barra lateral fina con iconos y texto, cabecera con fecha, grafica principal y lista de tareas (Logip).",
    "lienzo-panel": "El panel entero dentro de un lienzo redondeado con margen sobre un fondo de color apagado.",
}

FIRMAS_DE_TIPO = {"landing": list(FIRMAS), "movil": ["movil-mock", "lista-filas", "tabs-demo", "bento"],
                  "panel": ["bento", "linea-estados", "tabs-demo", "lista-filas"]}


def normal(t):
    return "".join(c for c in unicodedata.normalize("NFD", (t or "").lower())
                   if unicodedata.category(c) != "Mn")


def detectar_tipo(encargo):
    t = normal(encargo)
    if any(k in t for k in ("dashboard", "panel", "admin", "backoffice", "crm", "analitica", "analytics")):
        return "panel"
    if any(k in t for k in ("app movil", "aplicacion movil", "app de movil", " ios", "android", "mobile app",
                            "movil", "app para el movil", "pantallas de la app")):
        return "movil"
    return "landing"


def cargar_historial():
    try:
        with open(HISTORIAL, encoding="utf-8") as f:
            h = json.load(f)
        return h if isinstance(h, dict) else {}
    except Exception:
        return {}


def guardar_historial(h):
    try:
        with open(HISTORIAL, "w", encoding="utf-8") as f:
            json.dump(h, f, indent=1)
    except Exception:
        pass


def tirar(rng, tipo, evitar, solo, historial):
    # Estilos: suave siempre; el resto por peso, sin repetir los de la ultima tirada si se puede.
    ultimos = set(historial.get("estilos", [])) - {"suave"}
    candidatos = [e for e in ESTILOS if e != "suave" and e not in evitar]
    elegidos = ["suave"]
    if solo and solo in ESTILOS and solo != "suave":
        elegidos.insert(0, solo)
    frescos = [e for e in candidatos if e not in ultimos and e not in elegidos]
    viejos = [e for e in candidatos if e in ultimos and e not in elegidos]
    for pool in (frescos, viejos):
        while len(elegidos) < 6 and pool:
            e = rng.choices(pool, [ESTILOS[x]["peso"] for x in pool])[0]
            pool.remove(e)
            elegidos.append(e)
    elegidos = elegidos[:6]
    if not solo:
        rng.shuffle(elegidos)

    usados_hero, usados_firma, usados_mov, usados_nav, usados_tipo, usados_comp = (set() for _ in range(6))
    # Concepto, estructura y voz: los seis distintos, y conceptos frescos respecto a la ultima tirada.
    ult_c = set(historial.get("conceptos", []))
    frescos = [c for c in CONCEPTOS if c not in ult_c]
    conceptos = rng.sample(frescos, 6) if len(frescos) >= 6 else \
        frescos + rng.sample([c for c in CONCEPTOS if c in ult_c], 6 - len(frescos))
    rng.shuffle(conceptos)
    estructuras = rng.sample(list(ESTRUCTURAS), 6)
    voces = rng.sample(list(VOCES), 6)
    # Lo que deja la pagina vacia no le toca a suave (el usuario lo vio "muy vacio").
    k = elegidos.index("suave")
    for lista, malos in ((conceptos, {"manifiesto", "plano"}), (estructuras, {"una-pantalla", "articulo"}),
                         (voces, {"seco"})):
        if lista[k] in malos:
            j = next(i for i, x in enumerate(lista) if x not in malos and i != k)
            lista[k], lista[j] = lista[j], lista[k]
    ultimos_heros = set(historial.get("heros", []))
    fichas = {}
    if tipo == "landing":
        pueden = [e for e in elegidos if OBLIGADO in HEROS_DE[e]]
        obligado = rng.choice(pueden) if pueden else None
        if obligado:
            usados_hero.add(OBLIGADO)
    # Los estilos con menos heros posibles eligen primero, para que los cupos no los dejen sin ninguno.
    for e in sorted(elegidos, key=lambda x: len(HEROS_DE[x])):
        est = ESTILOS[e]
        k = elegidos.index(e)
        f = {"estilo": e, "concepto": conceptos[k], "estructura": estructuras[k], "voz": voces[k]}
        if tipo == "landing" and e == obligado:
            f["hero"] = OBLIGADO
        elif tipo == "landing":
            cupo = lambda h: sum(POSICION[x] == POSICION[h] for x in usados_hero) < MAX_POSICION[POSICION[h]]
            ops = [h for h in HEROS_DE[e] if h not in usados_hero and cupo(h)] or \
                  [h for h in HEROS_DE[e] if h not in usados_hero] or HEROS_DE[e]
            ops = [h for h in ops if h not in ultimos_heros and h != OBLIGADO] or ops
            f["hero"] = rng.choice(ops)
            usados_hero.add(f["hero"])
        else:
            todas = list(MOVIL if tipo == "movil" else PANEL)
            ops = [c for c in todas if c not in usados_comp] or todas
            f["composicion"] = rng.choice(ops)
            usados_comp.add(f["composicion"])
            if len(usados_comp) == len(todas):
                usados_comp.clear()
        ops = [x for x in FIRMAS_DE_TIPO[tipo] if x not in usados_firma] or FIRMAS_DE_TIPO[tipo]
        f["firma"] = rng.choice(ops)
        usados_firma.add(f["firma"])
        ops = [x for x in MOVIMIENTOS if x not in usados_mov] or list(MOVIMIENTOS)
        f["movimiento"] = rng.choice(ops)
        usados_mov.add(f["movimiento"])
        ops = [x for x in est["navs"] if x not in usados_nav] or est["navs"]
        f["nav"] = rng.choice(ops)
        usados_nav.add(f["nav"])
        f["paleta"] = rng.choice(est["paletas"])
        # Tipografias: la familia principal no se repite entre los seis.
        ops = [t for t in est["tipos"] if t.split(" ")[0] not in usados_tipo] or est["tipos"]
        f["tipos"] = rng.choice(ops)
        usados_tipo.add(f["tipos"].split(" ")[0])
        fichas[e] = f
    # Fotos del hero: una para cada uno y ninguna repetida. La imagen es la pagina.
    for n, e in enumerate(elegidos, 1):
        enc = ENCUADRE.get(fichas[e].get("hero"), "")
        fichas[e]["foto"] = "foto %d (solo en este hero): %s%s" % (n, ESTILOS[e]["imagen"],
                                                                  (" · encuadre: " + enc) if enc else "")
    return [fichas[e] for e in elegidos]


def imprimir(fichas, tipo, encargo):
    print("SEIS DIRECCIONES · tipo: %s%s" % (tipo, (" · encargo: " + encargo) if encargo else ""))
    print("La IMAGEN es la pagina (como en Dribbble): cada una abre con su foto grande y el")
    print("concepto encima; nada de maquetas de texto con una foto de adorno.")
    print("Cada una arranca en SU modo (estudio y nothing en negro, el resto en claro) y lleva")
    print("toggleTheme() para el otro. Mismos DATOS del negocio, pero cada")
    print("una con su texto, sus secciones y su orden. Ningun titular ni CTA repetido.\n")
    for i, f in enumerate(fichas, 1):
        e = ESTILOS[f["estilo"]]
        base, sup, tinta, acento = f["paleta"]
        print("=" * 78)
        print("P%d · %s   [estilo: %s]" % (i, e["nombre"], f["estilo"]))
        c, inter = CONCEPTOS[f["concepto"]]
        print("CONCEPTO:    %s — %s Interaccion protagonista: %s." % (f["concepto"], c, inter))
        print("AL ABRIR:    " + ARRANQUE[f["concepto"]] + ". Va ENCIMA de la imagen del HERO, no en su lugar.")
        if tipo == "landing":
            print("ESTRUCTURA:  %s — %s" % (f["estructura"], ESTRUCTURAS[f["estructura"]]))
        print("VOZ:         %s — %s" % (f["voz"], VOCES[f["voz"]]))
        print("ESTETICA:    " + e["idea"])
        if tipo == "landing":
            print("HERO:        %s (titular: %s) — %s La primera pantalla ES esta imagen." %
                  (f["hero"], POSICION[f["hero"]], HEROS[f["hero"]]))
        else:
            comp = (MOVIL if tipo == "movil" else PANEL)[f["composicion"]]
            print("COMPOSICION: %s — %s" % (f["composicion"], comp))
        print("NAV:         %s — %s" % (f["nav"], NAVS[f["nav"]]))
        print("FIRMA:       (solo si sirve al CONCEPTO; si no, fuera) %s — %s" % (f["firma"], FIRMAS[f["firma"]]))
        print("MOVIMIENTO:  %s — %s" % (f["movimiento"], MOVIMIENTOS[f["movimiento"]]))
        print("PALETA:      fondo %s · superficie %s · tinta %s · acento %s" % (base, sup, tinta, acento))
        print("OSCURO:      " + e["oscuro"])
        print("TIPOS:       " + f["tipos"])
        print("FOTO HERO:   " + f["foto"])
        print("TRAMPA:      " + e["trampa"])
    print("=" * 78)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("encargo", nargs="*")
    ap.add_argument("--tipo", choices=["landing", "movil", "panel"])
    ap.add_argument("--evitar", default="", help="estilos separados por comas")
    ap.add_argument("--solo", help="fuerza un estilo en P1")
    ap.add_argument("--repetir", "-r", action="store_true", help="ignora el historial")
    ap.add_argument("--semilla")
    ap.add_argument("--listar", action="store_true")
    a = ap.parse_args()
    if a.listar:
        for k, v in ESTILOS.items():
            print("%-13s peso %d · %s" % (k, v["peso"], v["nombre"]))
        return
    encargo = " ".join(a.encargo)
    tipo = a.tipo or detectar_tipo(encargo)
    rng = random.Random(a.semilla) if a.semilla else random.Random()
    hist = {} if a.repetir else cargar_historial()
    evitar = {x.strip() for x in a.evitar.split(",") if x.strip()} - {"suave"}
    # Reintenta hasta que ninguna posicion de titular se pase de cupo (casi siempre a la primera).
    for _ in range(40):
        fichas = tirar(rng, tipo, evitar, a.solo, hist)
        pos = [POSICION[f["hero"]] for f in fichas if f.get("hero")]
        if all(pos.count(p) <= MAX_POSICION[p] for p in set(pos)):
            break
    imprimir(fichas, tipo, encargo)
    # Para comparar.py: el comparador se genera, no se escribe a mano.
    try:
        with open("fichas.json", "w", encoding="utf-8") as fh:
            json.dump({"tipo": tipo, "encargo": encargo, "fichas": [
                dict(f, nombre=ESTILOS[f["estilo"]]["nombre"], paleta=list(f["paleta"]))
                for f in fichas]}, fh, ensure_ascii=False, indent=1)
    except Exception:
        pass
    # Las recetas de los estilos que han salido, aquí mismo: leer un fichero es un paso más.
    try:
        rec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "recetas.md"), encoding="utf-8").read()
        partes = {b.split("\n", 1)[0].strip(): b.split("\n", 1)[1].strip() for b in rec.split("## ")[1:]}
        print("RECETAS DE LOS ESTILOS QUE HAN SALIDO")
        for e in dict.fromkeys(f["estilo"] for f in fichas):
            if e in partes:
                print("· %s: %s" % (e, " ".join(partes[e].split())))
    except Exception:
        pass
    if not a.semilla:
        guardar_historial({"estilos": [f["estilo"] for f in fichas],
                           "conceptos": [f["concepto"] for f in fichas],
                           "heros": [f.get("hero") for f in fichas if f.get("hero")]})


if __name__ == "__main__":
    main()
