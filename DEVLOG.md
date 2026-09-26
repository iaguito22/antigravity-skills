# DEVLOG: Empirical Benchmarks & Findings

This document tracks the iterative development, testing, and token-cost analysis of the Antigravity Skills. Over 6 sessions and multiple parallel benchmarks, we pushed the agents to their limits to understand how LLMs behave under stress and how to mechanically restrain them.

## Key Empirical Rules Discovered

1. **Size Matters (Context Overhead):** Every KB of a skill's content injects its full text into the model's system context. **1 KB of skill ≈ 250-400 input tokens *per turn*.** If a skill is larger than 2KB, its behavioral improvements must aggressively save output/thinking tokens (e.g., by preventing massive blind edits) to justify its own overhead. Keep skills under 1.5KB when possible.
2. **Shell > Tool Calls:** For massive multi-file edits (like renaming a function across 6 files), teaching the agent to use a shell command like `sed -i` proved to be roughly **3.5x cheaper** in total tokens than allowing it to execute the `replace_file_content` tool individually per file.
3. **The "Do It Now" Syndrome:** When users aggressively prompt "do it now" or "write all code immediately", LLMs running in autonomous background modes will heavily prioritize fulfilling the user request over following passive skill guidelines. We had to implement harsh "mechanical stops" (e.g., `STRICTLY FORBIDDEN to write source code`, `SYSTEM LOCKED`) to prevent the architecture agent from dumping 20,000+ tokens of code blindly.
4. **Tool Double-Executions:** Ambiguous instructions like "verify that the test fails before fixing the code" led the LLM to run test suites twice, unintentionally doubling the input context footprint. Skills must strictly instruct a single execution phase.

## Iteration & Stress Test Highlights

- **Architecture Planning:** When asked to build a Chess Engine "immediately", the agent initially leaked 21,000 tokens implementing the entire game despite the skill telling it to plan first. It required system-level lock warnings to restrict the output to a `DESIGN.md` artifact, successfully stopping execution before writing any Python code.
- **Git Hygiene:** Ignored generic instructions to separate commits. It required an absolute ban on `git add .` to force the agent to use `git status` and create atomic, semantic commits based on feature/refactor scopes.
- **Root Cause Analysis:** Gemini is often smart enough to spot simple type errors (like `len(int)`) by just reading the code, allowing it to fix the issue instantly and ignore the skill's order to "debug first". We had to impose an absolute prohibition on first-turn fixes to force the scientific method (adding `print()` to isolate state).
- **Code Review:** Started as a massive 4.2 KB skill. We aggressively compressed it down to 1.3 KB without losing its ability to catch silenced exceptions, missing database rowcount verifications, and logical bugs.

## 2026-09-23 — Rework: 14 skills → 6

Benchmarked 11 real tasks with and without the skills (Gemini 3.7 Flash Low, Antigravity CLI 1.2.8).

- **Most skills never fired.** Only 3-5 of 10 tasks loaded any skill; the four web skills never did. Skills trigger **only through their `description`**, so every description now lists the user's actual words (English and Spanish). Result: 9/9 correct activations, no false ones.
- **Only the description is paid every turn** (~1.2k input tokens for the whole list); the body is paid once, when the agent opens it. So a focused 6 KB skill that fires beats three 1.5 KB ones that don't.
- **Merged or removed:** `security-audit` → `code-review`; `ui-design-standards` + `modern-css` + `web-accessibility` + `ui-animation` → `web-frontend`; `architecture-planning`, `root-cause-analysis`, `output-quality` and `operational-efficiency` removed (they never fired, or repeated the global rules file).
- **Rules alone don't stop AI-looking pages.** With a banned-phrases list the model still wrote "unhurried" and "honest", invented "12 bikes in progress" and pasted a green "open now" dot. A deterministic linter (`revisa.py`) run in the check step took three landings from 6-9 warnings each to 0.
- **The 2026 AI template** is no longer the purple gradient: it's cream background + high-contrast serif + split hero with a beige info card. It is now explicitly banned.
- **What Dribbble does that AI doesn't:** the image leads. Adding one `generate_image` hero plus a die for style/hero/signature/typefaces made three briefs look distinct and designed. Cost: ~110-150 s and ~12k output tokens per landing, versus ~60 s without images.
- **Model choice:** Gemini 3.8 Flash Low was 1.5-4x slower than 3.7 Flash Low on the same 11 tasks with the same quality, and leaked reasoning into answers.


## 2026-09-26 — Skill-doctor pass (Antigravity CLI 1.2.11)

- **`unit-testing` was locking bugs in.** On code with a SQL injection it wrote 11 green tests that asserted the buggy behavior as expected. It now writes down the *correct* behavior first and asserts that: 9 tests, 2 red, injection reported.
- **The AI tells users actually name** — split hero, one headline word in another color, a row of stats, pointless glows — are now banned in `web-frontend` and caught by `revisa.py`, together with emoji above the H1, cream + serif, overlays above 75 %, photos over 350 KB and made-up real-looking phone numbers (→ `000 000 000` plus a "Missing details" list).
- **`foto.py`** compresses `generate_image` output (~850 → ~130 KB) and prints its size.
- `revisa.py` accepts several files, flags the same headline or typeface across 3+ versions, and exits with 1 on warnings (so the skill chains it with `;`).
- The die's styles and heroes now come from real Dribbble shots; none of the heroes is half text / half image.
