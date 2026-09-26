---
name: web-frontend
description: >-
  Use whenever writing or changing anything that renders in a browser: page, landing,
  website, HTML, CSS, form, component, modal, menu, interface, styles, animation,
  portfolio, shop (also "página", "landing", "web"). Art direction so it looks modern
  and not AI-made, modern CSS, accessibility, and how to check it.
---

# Web: modern, opinionated, not AI-looking

Read this BEFORE writing: redoing a whole page is the most expensive thing.
If you're touching an existing site, respect its style and jump to §6.
`dado.py`, `foto.py` and `revisa.py` are run, not read: their usage is here and reading them wastes steps.

## 1. Direction before code (new page)
Roll the die once, without reading the script: `python3 ~/.gemini/config/skills/web-frontend/dado.py`.
It gives you style, hero, signature and typefaces (Fontshare ones load with
`https://api.fontshare.com/v2/css?f[]=general-sans@300,400,500&display=swap`).
If one piece truly clashes with the brief, reroll once. If the user already set a style,
don't roll.

Then decide three things, one line each:
- **Concept:** an object, gesture or place from THIS business. "Cozy café" is not a
  concept; "the chalkboard where they write today's roast every morning" is.
- **Palette:** one background, one ink, one accent. The sector's obvious palette is banned:
  coffee → cream and brown, eco → sage green, tech → blue or purple, spa → beige,
  lawyers → navy and gold.
- **Signature:** the die's, applied to that concept. It's what people will remember.

## 2. Images
This is what most separates a Dribbble landing from an AI one: the image leads. Every
landing or portfolio gets at least one, big, in the hero. Use `generate_image` once or
twice at most (~25 s each), and never in apps or dashboards.
- The prompt is an art director's, not a stock site's: a concrete object, a framing
  (top-down, extreme close-up, medium shot), a concrete light and "35mm film, natural
  grain" for photos, or "soft 3D render, glass, studio light" for something abstract or
  tech. Banned: "8k", "cozy", "hyperrealistic", "stunning", people looking at the camera.
- Never a portrait of a real named person (the lawyer, the owner): it would be fake.
  Show their place, their tools, their hands instead.
- The tool saves a 750-900 KB JPEG in its own folder. Don't copy it as is:
  `python3 ~/.gemini/config/skills/web-frontend/foto.py <source> hero.jpg` brings it down
  to ~130 KB and prints `width` and `height`. Give it a real `alt` and `object-fit: cover`.
- If text sits on the photo, the overlay stays under 50 %: a gradient only on the text's
  side, or the text inside a glass widget. A photo covered at 85 % is a page with no image.

## 3. Banned, because it gives the AI away (unless asked for)
- **What users call "so AI"** (overrides everything else): split hero, half text and half
  image; one word of the headline in another color, colored italics or a gradient; a
  horizontal row of stats ("10x · 65 % · 24/7"), also as a carousel or moving ticker;
  glows that do nothing (offsetless shadows, blurred blobs, neon); many colors;
  maximalism. Background, ink and one accent at most.
- **2023 template:** emoji pill above the H1, 3 made-up stats, 3 emoji cards, purple
  gradients, `0 20px 60px` shadows, an "Open today" card.
- **2026 template, what you produce if you don't think:** cream background + high-contrast
  serif H1 + split hero with a beige info card on the right; spaced uppercase label above
  every heading; a page of only text and boxes, no image; every section the same width
  and rhythm.
- **Default fonts:** Inter, DM Sans, Plus Jakarta Sans, Poppins, Montserrat, Fraunces,
  Playfair Display, Newsreader. Use the die's.
- **Made-up "live" data:** "open now" with a green dot, "12 bikes in progress",
  "4 slots left", "status:", GPS coordinates. A static page doesn't know that.
- **Ad adjectives:** relentless, no-nonsense, next level, premium.
- **Stock phrases:** "unhurried", "honest", "artisanal", "from farm to cup", "you
  deserve", "unique experience", "passion for", "discover", "elevate". Write like the
  owner: prices, services, hours, proper names.
- **Made-up contact details that look real.** If the user didn't give you a phone,
  street or email, don't invent plausible ones (a "982 24 18 90" looks real and someone
  will call it). Use `000 000 000`, `Street, no.` and `hello@example.com`, and list them at
  the end of the report as **Missing details**. Sample prices and hours are fine, but put
  them on that list too.

## 4. Scope: a landing, not an app
4-5 sections and under 30 KB. No calculators, forms, bookings or features nobody asked
for: contact goes through phone, email or a map link. Menu with 4 links at most,
`white-space: nowrap`.

## 5. What makes it surprising: the signature plus at least two of these
- What the best Dribbble pages repeat: the page inside a rounded canvas with margin; a
  centered hero object or render; micro-cards with real data floating on top; a centered
  weight-500 headline with negative tracking; segmented tabs that switch a demo; a
  carousel of photos in rounded cards; one radius scale; pill buttons.
- Extreme type scale: headline at `clamp(2.5rem, 10vw, 10rem)` with negative
  `letter-spacing`, next to small text. Contrast of sizes.
- One section that breaks the grid: full-bleed, overlapping, sticky or horizontal scroll.
- Uneven rhythm: sections of different heights and widths, not everything centered at 1200px.
- Scroll-linked motion in CSS (`animation-timeline: view()`) inside `@supports` and
  `prefers-reduced-motion: no-preference`.
- Craft: `text-wrap: balance` on headings, `tabular-nums` on prices, `::selection` with the
  accent, hover with intent.

## 6. CSS and accessibility
- Mobile from the start, so you don't fix it later: headings with
  `clamp(2.5rem, 10vw, 10rem)` and `overflow-wrap: anywhere`; grids with
  `repeat(auto-fit, minmax(min(100%, 16rem), 1fr))`; nothing with a fixed px width.
- No orphans in grids: with 3 items, 3 columns or one featured plus two below;
  never a lone item on the last row.
- `100dvh`, `gap`, `clamp()`. `line-height` 1.5-1.6 in paragraphs and ~1 in large headings.
  Never `transition: all`. Short shadows (`0 1px 3px`) or wide, very faint ones tinted
  with the hue (`0 24px 48px -12px rgb(30 60 150 / .12)`); never 30% grey.
- `<button>` for actions, `<a>` to navigate. `<nav>`, `<main>`, a single `<h1>`,
  `<label>` on every input. Visible `:focus-visible`, AA contrast, touch targets ≥ 44 px.
- Animate only `transform` and `opacity`: hover 150-250 ms, entrances 200-400 ms.

## 7. Check, one pass
In ONE call: `python3 ~/.gemini/config/skills/web-frontend/revisa.py index.html; agy-ver abrir index.html && agy-ver foto hero && agy-ver ve '#<2nd section>' && agy-ver movil && agy-ver logs && agy-ver cerrar`.
Fix every line from the linter, no arguing (the `;` is on purpose: the linter exits
with 1 when it warns, and this way the photos still get taken). Then look at the photos and ask yourself:
1. Hiding the name, could it belong to any business in the sector? If yes, it lacks a concept.
2. Does it look like the 2026 template from §3?
3. Can you see the signature without looking for it?

Fix with targeted edits (`replace_file_content`), never by rewriting the file.
`agy-ver` comes from [a-gemini-more-like-claude](https://github.com/iaguito22/a-gemini-more-like-claude).
