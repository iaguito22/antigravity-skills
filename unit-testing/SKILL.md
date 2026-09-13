---
name: unit-testing
description: >-
  Writes unit tests that actually catch bugs. Activate when the user asks
  to write tests, "add tests", "cover this", or wants to verify a new function.
  Not for integration/E2E tests: for fast tests that fail if code is broken.
---

# Unit Tests that Catch Bugs

A test that cannot fail is not a test.

## Value Order (Start with the most valuable)

1. **Error cases**: invalid input, null, empty, negative, wrong type → what does it raise/return?
2. **Boundaries**: min, max, single-element list, first/last iteration.
3. **Happy path**: do this last. Testing only what works adds zero value.

## Rules

- Name = documentation: `test_remove_missing_raises_keyerror` > `test_remove`.
- One assertion per test when possible.
- Do not mock what you are testing; only external dependencies (DB in `:memory:`, `unittest.mock` for network/time).
- Minimal fixture: if DB is needed, use `sqlite3.connect(":memory:")`.

## Execute ONCE and report

```sh
python -m pytest test_file.py -v
```

Report exactly:
```
Tests: N | Pass: N | Fail: N
· test_name — what bug or case it verifies
```

If something fails unexpectedly: paste the full traceback, do not summarize it.
