---
name: code-review
description: >-
  Reviews code looking for real bugs before committing. Activate to review
  changes, find errors, or evaluate pull requests. Does not evaluate style:
  searches for logical flaws, silenced errors, and leftover debugging code.
---

# Code Review: Find Real Breakages

## 1. Context and Execution
- If the user reports a bug, **reproduce it** before reading code.
- Reading is not testing. **Execute** the function or script with a normal input and an edge case. If you cannot run it, say so.

## 2. Inspection
Review the entire function code, not just the partial diff. Search in this exact order:
1. **Logic**: What happens with empty, null, zero, or negative inputs?
2. **Silenced Errors** 🔴: `except: pass` hiding errors. Magic `default=` fallbacks.
3. **Lying Returns** 🔴: Returning `True` on DB updates without checking `rowcount > 0`.
4. **Broken Contracts**: Function signatures that changed and break callers.
5. **Leftovers** 🟡: Debugging prints, commented code, `# BUG`.

## 3. Reporting (Mandatory Format)
Write the failure concretely ("with X, Y happens"). Use this exact structure:

```
### 🔴 filename.py:10 — summary of severe bug
With [input], [problem] occurs. Fix: [solution].

### 🟡 filename.py:20 — leftover or risk
Residual print or generic exception.

### 🔵 filename.py:30 — simplification
Redundant code.
```
