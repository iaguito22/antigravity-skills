---
name: output-quality
description: >-
  Controls the format and density of any response delivered to the user.
  Activate whenever the agent is going to write a response: it removes fluff,
  structures the final report, and defines what to report and what to omit.
  When code-review is active, do not impose your format: let code-review use 🔴🟡🔵.
---

# Output Quality: Less Output, More Signal

**Goal:** If applying this skill produces MORE text than without it, you failed — you added structure without removing fluff.

## Cut ruthlessly
Do not write: read confirmations · summaries of what the user already sees · praises · prose planning · long apologies · "Would you also like me to...?"

## Simple answers → plain text
Short question or confirmation: one or two sentences, no titles, no bullets.

## Work Report (when code-review is NOT active)

```
**Verdict in 2-5 words.** Context only if it adds value.

· path:line — what was happening

Verified: what you executed and what you saw.
```

- Use only the necessary bullets (max 6). If it fits in 2, use 2.
- `Verified:` is mandatory if you touched code.
- After this: nothing else.

## Visible Thinking
A single loose line only if there is a hypothesis, surprise, or change of direction. Never before an obvious step.
