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
