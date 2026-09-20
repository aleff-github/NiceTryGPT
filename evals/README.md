# NiceTryGPT evaluations

This directory defines a small, reproducible way to test the claim that a NiceTryGPT transformation reduces a **specific cheap shortcut** without materially increasing human-facing challenge complexity.

It is intentionally not a large benchmark framework.

## Current status

The evaluation infrastructure is ready, but **no cross-model results are committed yet**.

That is deliberate. Same-context self-review is not counted as evidence.

## Pilot matrix

The first pilot uses:

- challenges: `mini-idor`, `mini-traversal`;
- variants: `before`, `after`;
- model families: Claude, GPT, Gemini;
- independent runs per cell: 5.

That is:

```text
2 challenges × 2 variants × 3 model families × 5 runs = 60 runs
```

Exact model/version identifiers must be recorded for every run.

## Files

- [`protocol.md`](protocol.md) — fixed experimental procedure;
- [`solver-prompt.txt`](solver-prompt.txt) — prompt template used for every run;
- [`results.csv`](results.csv) — raw observations;
- [`summarize.py`](summarize.py) — dependency-free summary script.

## Summarize collected results

```bash
python evals/summarize.py
```

The primary metric is solve rate. Secondary descriptive metrics are time, meaningful actions, and whether the original cheap shortcut was attempted.

Do not turn a tiny pilot into claims of universal LLM resistance.
