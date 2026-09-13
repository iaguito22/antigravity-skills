---
name: root-cause-analysis
description: >-
  Methodical debugging of complex failures. Activate when there is an obscure bug,
  the system crashes without a clear reason, or when previous fix attempts failed.
  Forbids blind patching.
---

# Root Cause Analysis: Scientific Method for Bugs

## 1. Prohibition of Early Fixes
It is **STRICTLY FORBIDDEN** to attempt fixing the code logic in your first turn, no matter how obvious the error seems.
Your first commit or modification MUST be EXCLUSIVELY to add instrumentation.

## 2. Mandatory Instrumentation
1. Execute the code to see the error.
2. Add `print()`, `console.log()`, or traces right before the crashing line to expose the state of the variables.
3. Execute the code again to capture that output.

## 3. Minimal Intervention
Only when you have the output from your `prints` confirming the exact error, you are authorized to remove the prints and propose the code that fixes the bug.
