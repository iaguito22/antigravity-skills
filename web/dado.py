#!/usr/bin/env python3
"""Die for the web skill: a style, a hero layout, a signature and a type pairing.
It exists because when the model chooses, it always lands on the median
(cream + serif + split hero, or a centered headline on a flat background with the photo below)."""
import json, os, random, tempfile

STYLES = [
    # (weight, description). `soft` weighs more: it is the author's taste. Same families as prototypes.
    (3, "Soft: very light single-hue background, white 28-radius cards, wide faint shadows in the same hue, black pill buttons with an arrow in a circle, weight-500 headlines"),
    (2, "Minimal: white or 98 % grey, near-black ink and no accent; white widgets and weight-500 headlines; a very clean catalog"),
    (2, "Framed canvas: the page inside a 36-radius canvas set 16px from the edge on a muted colored background; the hero photo sits inside the canvas"),
    (2, "Photographic: one huge photo leads; white text on top and one glass widget with real data"),
    (1, "Liquid glass: a live photo behind and translucent glass panels with a specular highlight on top; monochrome on top, no glows"),
    (1, "Nothing (like the Nothing X app): black with #1b1b1b 20-radius cards, thin headlines, thin numbers with a slash (7/40), mono uppercase labels; no dot-matrix font and red on a single detail"),
    (1, "Dark studio: a dark photo or render with studio light as the background, sections in flat black, white headlines; the light comes from the image, never the CSS"),
]
HEROS = [
    # All with the photo AS BACKGROUND and the information in widgets on top (Kumo, Ranty, Golfair).
    # None is half text / half image, nor text on a flat background.
    "Rounded canvas with margin and the background photo inside; the business's object in the center, 3-4 square glass tiles floating at its sides (variants, flavors, models) and the headline at the bottom, over the photo",
    "Full-screen landscape or location photo; large headline top-left; on the right a white card with a thumbnail, two chips and a sentence; bottom-left a card with a small photo and bottom-right a big figure (12 m², 9 months) with its label",
    "Full-bleed 100svh photo with an overlay only at the bottom; headline bottom-left and, bottom-right, a glass widget with the featured product (photo, name, price, button)",
    "Background photo with a centered glass search or filter bar (3 real catalog selectors and a button) and the headline above it; two small cards in the corners",
    "Background photo in a canvas with margin; glass nav inside; a glass segmented control at the top that switches the background photo (3-4 real options) and the headline centered at the bottom",
    "Background photo with the product; 3 thin labels with a line pointing at parts of the product (material, size, detail) and the large headline bottom-left",
]
SIGNATURES = [
    "Slow marquee with the names of the business's services or pieces, never numbers",
    "Image revealed with clip-path as it enters the screen (animation-timeline: view())",
    "The hero image starts as a card with margin and expands to full-bleed on scroll",
    "A large paragraph that lights up word by word with the scroll",
    "Sticky section: the image stays put while the text scrolls past",
    "Horizontal scroll-snap row for the menu, catalog or projects",
    "Variable font that changes weight or width on hover or scroll",
    "Each section changes the whole page background color as it enters",
    "List (menu, services) that shows a floating image on hover",
    "Visible grid of thin lines as a graphic element across the page",
    "Very subtle SVG paper grain over flat backgrounds and one saturated accent",
]
TYPES = [
    "General Sans (Fontshare) 300 for large headlines + 400 for text",
    "Satoshi (Fontshare) 300-500",
    "Urbanist 300 for headlines + Manrope for text",
    "Switzer (Fontshare) 300 for headlines + Geist Mono for data",
    "Bricolage Grotesque (headlines) + Instrument Sans (text)",
    "Instrument Serif (very large headlines) + Geist (text)",
    "Archivo at expanded width (wdth 125) for headlines + regular Archivo",
    "Big Shoulders Display (headlines) + IBM Plex Sans (text)",
    "Familjen Grotesk (headlines) + Fragment Mono (data and labels)",
    "Gloock (headlines) + Figtree (text)",
    "Young Serif (headlines) + Onest (text)",
    "Schibsted Grotesk (headlines) + Libre Caslon Text (text)",
    "Unbounded (headlines) + Manrope (text)",
    "Syne (headlines) + Space Mono (data and labels)",
]

hist = os.path.join(tempfile.gettempdir(), "web-frontend-dado.json")
try:
    last = json.load(open(hist))
except Exception:
    last = {}
pick = {"style": random.choices([s for _, s in STYLES], [w for w, _ in STYLES])[0]}
for key, options in (("hero", HEROS), ("signature", SIGNATURES), ("types", TYPES)):
    pool = [x for x in options if x != last.get(key)] or options
    pick[key] = random.choice(pool)
try:
    json.dump(pick, open(hist, "w"))
except Exception:
    pass
print("STYLE:     " + pick["style"])
print("HERO:      " + pick["hero"])
print("SIGNATURE: " + pick["signature"])
print("TYPES:     " + pick["types"])
