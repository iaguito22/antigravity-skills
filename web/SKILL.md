---
name: web
description: >-
  Taste and process for any new or redesigned web page: landing, business site, portfolio,
  shop, html/css (also "web", "página", "landing"). Use it before writing the first line.
---

# A web page that doesn't look AI-made

The scripts in this folder are run, not read.

## 1. Direction (one call)
`python3 ~/.gemini/config/skills/web/dado.py` → style, hero, signature and typefaces. Use
it as given; if the user already chose a style, skip it. Write three lines before coding:
- **Concept:** an object, gesture or place of THIS business ("the chalkboard where they
  write today's batch"), not an adjective.
- **Palette:** background, ink and one accent, away from the sector's obvious one
  (coffee ≠ cream and brown).
- **Signature:** the die's one, applied to the concept.

## 2. What it should look like
Minimal, soft and rounded, liquid glass, Nothing, lots of air. The image leads:
- **Hero** = a full-screen photo (`100svh`, or inside a rounded canvas with 12-16 px of
  margin) with the headline on top and 2-4 small glass or 90 % white widgets
  (240-340 px) spread over the corners: a product card, chips, one real fact.
- **Cards** with the photo on top (4:5 or 4:3, radius 20-24), name and price on one line,
  one grey line of 2-3 facts joined with `·`.
- Extreme type scale (`clamp(2.5rem, 10vw, 10rem)`, negative tracking) next to small
  text; pill buttons; a single radius scale.
- Scroll-linked motion (`animation-timeline: view()` inside `@supports` and
  `prefers-reduced-motion: no-preference`).

## 3. What reads as "so AI" (always out)
Split hero text | image · one H1 word in another color, colored italics or gradient (the
H1 is one ink) · a row or ribbon of stats ("10x · 24/7") · glows, blobs and neon · cream
background + serif H1 · spaced uppercase label above every title · "live" data or GPS
coordinates · stock phrases ("artisanal", "passion for", "unique experience") · default
fonts (Inter, DM Sans, Plus Jakarta, Poppins, Montserrat, Fraunces, Playfair, Cormorant).
Write like the owner: prices, hours, proper names.

## 4. Build
- By default a small site: `index.html` + at most two pages the business needs
  (`menu.html`, `contact.html`), with shared `css/styles.css` and `js/main.js` and the
  catalog in `js/data.js`. Write `index.html` in full; the others by copying it and
  changing `<main>`.
- Photos: the hero is generated. In the CLI, with `invoke_subagent` (one subagent with an
  art-director prompt: object, framing, light, "35mm film, natural grain"; it returns the
  path). The rest from Unsplash (`https://images.unsplash.com/photo-<id>?w=900&q=70`),
  without guessing IDs: if you doubt one, generate it. `foto.py <source> img/hero.jpg`
  compresses what you generate. Every `img` with `alt`, `width` and `height`.
- Interactive parts are the ones that help choose (filters, gallery, mobile menu) and they
  really work. Calculators, bookings, carts or client areas only if asked: they cost a lot
  and nobody asked. Plain HTML without dependencies unless the project already uses a
  framework.
- Data you were not given (phone, address, email, people's names): `000 000 000`,
  `Street, No.`, `hello@example.com`, and a **Missing data** bullet in the report.

## 5. Check (done = linter clean and screenshots looked at)
`python3 ~/.gemini/config/skills/web/revisa.py *.html; agy-ver abrir index.html && agy-ver foto && agy-ver ve 900 && agy-ver movil && agy-ver logs`
Fix every linter line and every console error. Open the screenshots and hunt the detail:
menu on one line, nothing overflowing the canvas or the screen, no cut-off text, mobile,
contrast. Fix everything you saw in one batch of targeted edits and check it with a single
extra pass (linter + a screenshot of what you changed); don't repeat the whole round.
