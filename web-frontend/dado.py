#!/usr/bin/env python3
"""web-frontend die: a style, a hero layout, a signature and a type pairing.
It exists because when the model chooses, it always lands on the median
(cream + serif + split hero)."""
import json, os, random, tempfile

STYLES = [
    # (weight, description). Same families as prototypes.
    (3, "Soft: very light single-hue background, white 28-radius cards, wide faint shadows in the same hue, black pill buttons with an arrow in a circle, weight-500 headlines"),
    (2, "Minimal: white or 98 % grey, near-black ink and no accent; centered weight-500 headline and a single big image in a rounded card"),
    (2, "Framed canvas: the page inside a 36-radius canvas set 16px from the edge on a muted colored background; hero object in the center"),
    (2, "Photographic: one huge photo leads; white text on top and one glass widget with real data"),
    (1, "Liquid glass: a live photo behind and translucent glass panels with a specular highlight on top; monochrome on top, no glows"),
    (1, "Nothing (like the Nothing X app): black with #1b1b1b 20-radius cards, thin headlines, thin numbers with a slash (7/40), mono uppercase labels; no dot-matrix font and red on a single detail"),
    (1, "Dark studio: flat black and a render with studio light; centered white headline; the light comes from the image, never the CSS"),
]
HEROS = [
    # None is half text / half image: users find it the most "AI" thing there is.
    "Centered headline (weight 500, tracking -0.03em) and below it the hero object or photo, big and centered",
    "Centered headline + a segmented control with 3-4 real tabs + the UI or the service in a rounded card over a landscape photo",
    "The hero is a rounded screen with margin: full-bleed photo inside, nav inside and a large headline at the bottom, over the image",
    "Central object with 3-5 micro-cards of real data floating around it, each slightly rotated",
    "Full-screen photo or render and a large headline anchored bottom-left, one sentence and nothing else",
    "A giant word across the full width with the cut-out object in front covering part of the letters",
    "Large centered headline with a small pill-shaped image set between two words",
    "Huge photo with ONE glass widget on top carrying real data (hours, next appointment, directions)",
    "Hero inside a 28-radius card set 16-20px from the edge, photo full-bleed and the headline centered on top",
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
