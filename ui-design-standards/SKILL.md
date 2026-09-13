---
name: ui-design-standards
description: >-
  Visual quality floor for UI. Use to avoid the "cheap AI template" look.
  Focuses exclusively on aesthetics, shadows, proportions, modern typography,
  and card/modal layouts.
---

# UI Design Standards (Good Design)

An AI-generated website is recognizable from three meters away: faded purple gradients ("AI slop"), broken mobile modals, and 3 identical vanity stat blocks floating in a void.

## 1. The Giveaway Test: What NOT to do
- **NO generic 3-card feature blocks**: 3 vanity stats floating in the center of the page is an AI cliché. Use asymmetry or real editorial layouts.
- **NO giant blurry shadows**: `box-shadow: 0 20px 60px rgba(0,0,0,0.3)` makes everything float without gravity. Use crisp, short shadows (`0 1px 3px rgba(0,0,0,0.1)`).
- **NO hiding critical info on hover**: Prices and buttons must always be visible. Hover is for micro-interactions, not hiding vital content.

## 2. Typography and Spacing
- Paragraph `line-height` should be loose (`1.6` to `1.8`), but large headings must be tight (`1.1` or `1.2`).
- Use visual hierarchy by contrast (light gray vs black) and font weight, not just font size.
