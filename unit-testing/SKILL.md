---
name: unit-testing
description: >-
  Use when asked to write tests: "add tests", "write tests", "cover this", "test X"
  (also "añade tests", "haz tests"), or to verify a new function. Fast unit tests that
  fail when the code is broken.
---

# Tests that catch bugs

A test that can't fail is not a test.

## First: what it SHOULD do, not what it does
Before writing a test, read the code as a reviewer and write down the correct behavior of
each function (from its name, its docstring and common sense). The test asserts THAT. If
the code does something else, the test fails: that's its job.
- Never assert a bug as if it were expected. A test called
  `..._returns_true_because_except_swallows` or one checking that a balance goes negative
  is locking the bug in, not catching it.
- If you spot a security flaw while reading (SQL or command injection, secrets, path
  traversal), write the test that proves it (e.g. `user = "x' OR 1=1 --"` must not touch
  other rows) and report it even if nobody asked.
- If you don't know the correct behavior, ask in the report; don't infer it from what the
  code returns today.

## Order (most to least valuable)
1. **Errors**: invalid input, `None`, empty, negative, wrong type → what it raises/returns.
2. **Limits**: minimum, maximum, a single element, first/last iteration.
3. **Happy path**, last.

## Rules
- The name is the documentation: `test_remove_missing_raises_valueerror`, not `test_remove`.
- Mocks only for external things (network, time, disk). DB: `sqlite3.connect(":memory:")`.
- A test that fails because of a real bug in the code: **don't touch the code or the test**,
  report it.
  All passing on the first run over code that has bugs means the tests are wrong:
  review them before handing in.

## Run once
`python3 -m pytest -q <file>`; if pytest isn't installed, `python3 -m unittest -v <file>`.
JS: whatever runner the project already uses (`package.json`).

```
Tests: N | Pass: N | Fail: N
· test_name — which case it covers
🔴 Bugs found: file:line — with <input>, <failure> happens (test that proves it)
```
If something fails: paste the whole traceback.
