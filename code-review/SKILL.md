---
name: code-review
description: >-
  Use to review code for real bugs and security holes: "review this", "take a look",
  "before I commit", "going to production", "is this OK?", PRs, diffs (also "revisa",
  "echa un ojo", "antes de commitear"). Logic errors, silenced errors, injections,
  leftovers. Not style.
---

# Review: real bugs, not style

Reviewing is not fixing: don't edit the code unless asked.

## 1. Run it before judging
- Reported bug → reproduce it first.
- Run every suspicious function with a normal input and an edge case in ONE call
  (`python3 -c`, `node -e`). If it can't be run, say so.

## 2. What to look for, in order
1. **Logic**: empty, `None`, zero, negatives, a single element.
2. **Silenced errors**: `except: pass`, `catch {}`, a `default=` that hides failures.
3. **Lying returns**: `return True` without checking `rowcount`, status or response.
4. **Broken contracts**: changed signatures that break callers.
5. **Security**, if there's user input, auth, files or it's going to production: SQL/command
   injection, path traversal, secrets in code, sensitive data in responses or logs, IDOR
   (is it checked that the resource belongs to the user?).
6. **Leftovers**: debug prints, commented-out code.

## 3. Report
```
**Verdict in 2-5 words.**

🔴 file:line — with <input>, <failure> happens. Fix: <how>.
🟡 file:line — risk or leftover.

Checked: what you ran and what came out (or "static review, not executed").
```
For security 🔴s, half a line on how it's exploited.
