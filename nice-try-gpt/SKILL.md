---
name: nice-try-gpt
description: Makes authorized CTF challenges less trivial for LLMs without making them miserable for humans. Use when asked to harden, de-pattern, or test a CTF against AI shortcuts.
---

# NiceTryGPT

Less pattern matching. More actual hacking.

Use this skill only for CTFs, labs, and systems the user is authorized to test. The goal is not to make a challenge harder in general. The goal is to remove cheap LLM shortcuts while keeping the human experience simple, fair, and close to the original difficulty.

## Core rule

Increase uncertainty, not complexity.

Preserve all three invariants:

1. The intended vulnerability class stays the same.
2. The prerequisite knowledge stays the same.
3. Expected human difficulty stays roughly the same.

Prefer one small, strong change over several clever changes. It is valid to conclude `NO CHANGE NEEDED`.

## Workflow

### 1. Understand

Read only what is needed to understand the challenge: entry point, run instructions, player-facing description, relevant code, flag format, and intended learning objective.

Write down:

- vulnerability class;
- intended solve path;
- expected player knowledge;
- approximate human difficulty;
- how to start from a clean state.

Do not modify files yet.

### 2. Baseline solve

Start the challenge from a clean state and solve it end-to-end through the player-facing surface.

A valid baseline ends with the flag or equivalent success condition obtained through the intended vulnerability. Do not count reading the flag directly from source code, fixtures, environment files, or container internals as a solve.

If the baseline cannot be reproduced, stop and report `BASELINE FAILED`. Do not transform a challenge you have not verified.

### 3. Find shortcuts

Ask one question: why could an LLM jump too quickly from observation to solution?

Look for cheap shortcuts such as:

- an endpoint or parameter that names the vulnerability too clearly;
- a direct one-step mapping from a common pattern to a canned exploit;
- all required information appearing in one obvious response;
- a static value that removes the need to observe runtime behavior;
- an error message that effectively reveals the solve path;
- a challenge that rewards guessing a textbook payload without validating a hypothesis.

Do not assume every obvious challenge needs changing.

### 4. Pick a minimal resistance move

Choose zero, one, or at most two lightweight changes. Prefer these families:

- **Pattern break** — remove an overly explicit cue without hiding the vulnerability.
- **Runtime discovery** — make one small fact discoverable through normal interaction rather than static pattern matching.
- **Context split** — require connecting two nearby pieces of ordinary application behavior.
- **State dependency** — let a small piece of state matter, without creating a multi-stage exploit chain.
- **Semantic decoy** — add one plausible but cheaply falsifiable attack surface.

A decoy is optional. Never make honeypots a predictable signature of this skill.

Read `references/resistance-patterns.md` only when you need examples or selection guidance.

### 5. Human Cost Gate

Reject a proposed change unless all of these remain true:

- same vulnerability class;
- same prerequisite knowledge;
- no new exploit primitive required;
- no brute force;
- no CAPTCHA or human-verification gimmick;
- no huge context, token flooding, or pointless encoding;
- no obscure trivia or external knowledge;
- no artificial multi-stage chain;
- normally no more than 1–3 additional meaningful player actions;
- expected human solve time should remain in the same difficulty band.

For decoys, add no more than 1–3 and make each dismissible in 1–2 normal interactions.

If a useful LLM-resistance change would violate this gate, keep the original challenge.

### 6. Modify

Implement the smallest diff that satisfies the chosen strategy.

Preserve normal application behavior. Do not rewrite the challenge simply to make it look different. Do not hide the flag behind random instability. Do not remove the intended teaching signal.

If a `nicetrygpt-history.md` file exists, scan it before choosing a mechanism and avoid repeating the same transformation pattern without a good reason.

### 7. Verify end-to-end

Rebuild or restart from a clean state.

Verify:

1. the application starts normally;
2. ordinary player-facing functionality still works;
3. the intended vulnerability still exists;
4. the transformed challenge can still be solved end-to-end;
5. the flag is obtained through the vulnerability, not by static extraction;
6. any decoy is harmless, plausible, and cheap to reject.

If verification fails, revert or simplify the transformation. A broken challenge is never a successful transformation.

### 8. Fresh-solver check

When an isolated subagent or fresh context is available, give it only the player-facing challenge information and ask it to solve the transformed challenge. Do not reveal the transformation plan or baseline solution.

When a fresh context is not available, generate a short fresh-solver brief that another session can use. Do not pretend that self-review proves LLM resistance.

### 9. Report

Create or update `nicetrygpt-report.md` in the challenge root with a short report containing:

- baseline result;
- vulnerability class;
- shortcut identified;
- transformation used, or `NO CHANGE NEEDED`;
- human-cost estimate;
- post-change E2E result;
- fresh-solver result if actually tested;
- files changed.

Keep the report concise. NiceTryGPT should leave behind a challenge, not a research paper.

## Success criteria

A transformation succeeds only when the original learning objective is preserved, the challenge still works end-to-end, and the LLM shortcut is reduced without materially worsening the human experience.

If those goals conflict, favor the human player.
