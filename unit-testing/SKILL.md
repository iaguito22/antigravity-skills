---
name: unit-testing
description: >-
  Use when asked to write tests: "add tests", "write tests", "cover this", "test X"
  (also "añade tests", "haz tests"), or to verify a new function. Fast unit tests that
  fail when the code is broken.
---

# Tests that catch bugs

A test that can't fail is not a test.

## Order (most to least valuable)
1. **Errors**: invalid input, `None`, empty, negative, wrong type → what it raises/returns.
2. **Limits**: minimum, maximum, a single element, first/last iteration.
3. **Happy path**, last.

## Rules
- The name is the documentation: `test_remove_missing_raises_valueerror`, not `test_remove`.
- Mocks only for external things (network, time, disk). DB: `sqlite3.connect(":memory:")`.
- A test that fails because of a real bug in the code: **don't touch the code or the test**,
  report it.

## Run once
`python3 -m pytest -q <file>`; if pytest isn't installed, `python3 -m unittest -v <file>`.
JS: whatever runner the project already uses (`package.json`).

```
Tests: N | Pass: N | Fail: N
· test_name — which case it covers
```
If something fails: paste the whole traceback.
