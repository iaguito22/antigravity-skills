#!/usr/bin/env python3
"""web-frontend die: a style, a hero layout, a signature and a type pairing.
It exists because when the model chooses, it always lands on the median
(cream + serif + split hero)."""
import json, os, random, tempfile

STYLES = [
    # (weight, description)
    (3, "Soft: 24-32px radii, light single-hue background, frosted glass, pill buttons with an arrow in a circle, wide and very faint shadows in the same hue, thin headlines"),
    (2, "Photographic: one huge photo leads; white text on top and glass widgets with real data"),
    (1, "Expressive editorial: huge type, saturated color, images framed like objects"),
    (1, "Cinematic dark: near-black background, photo or render with dramatic light, thin and large headline"),
]
HEROS = [
    "Hero inside a 28px-radius card set 16-20px from the edge, photo full-bleed inside, headline on top",
    "Large headline with a small pill-shaped image set between two words",
    "Huge photo with a glass widget on top carrying real data (price, hours, directions)",
    "Two-tone headline (one line in light grey) bottom-left, over the photo",
    "Monumental full-width headline; the cropped photo peeks out underneath",
    "Full-screen full-bleed photo with the headline inside, bottom-left",
    "Narrow text column on the left and a huge vertical photo overflowing on the right",
    "Collage: two or three overlapping images at different scales, headline crossing them",
    "A giant sentence and below it a wide cropped photo, with a ribbon of real data",
    "Asymmetric thirds: 2/3 flat color with the headline, 1/3 photo; nothing centered",
    "The information as a printed object: ticket, label, menu or stamp, at large scale",
    "Vertical headline, rotated 90 degrees, against the edge next to a tall photo",
]
SIGNATURES = [
    "Slow marquee with the business's real data: prices, hours, names",
    "Giant section numbers overlapping the content",
    "Image revealed with clip-path as it enters the screen (animation-timeline: view())",
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
