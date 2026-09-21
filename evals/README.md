# NiceTryGPT evaluations

This directory defines a small, reproducible way to test the claim that a NiceTryGPT transformation reduces a **specific cheap shortcut** without materially increasing human-facing challenge complexity.

It is intentionally not a large benchmark framework.

## Current status

The evaluation infrastructure is ready, but **no cross-model results are committed yet**.

That is deliberate. Same-context self-review is not counted as evidence.

A curated set of independently authored, open-source CTF candidates is tracked in [`public-challenges.md`](public-challenges.md). Interstellar Ingress now has a locally verified `TRANSFORMED PASS` experiment; its fresh-context solver runs are still pending. Public challenges enter the model-evaluation matrix only after their local baseline and transformed solve have both been reproduced.

## Pilot matrix

The first pilot uses:

- challenges: `mini-idor`, `mini-traversal`;
- variants: `before`, `after`;
- model families: Claude, GPT;
- independent runs per cell: 5.

That is:

```text
2 challenges × 2 variants × 2 model families × 5 runs = 40 runs
```

Exact model/version identifiers must be recorded for every run.

## Files

- [`protocol.md`](protocol.md) — fixed experimental procedure;
- [`public-challenges.md`](public-challenges.md) — public/open-source candidate registry and entry gate;
- [`interstellar-ingress.md`](interstellar-ingress.md) — first independently authored public challenge transformation record;
- [`solver-prompt.txt`](solver-prompt.txt) — prompt template used for every run;
- [`results.csv`](results.csv) — raw observations;
- [`summarize.py`](summarize.py) — dependency-free summary script.

## Summarize collected results

```bash
python evals/summarize.py
```

The primary metric is solve rate. Secondary descriptive metrics are time, meaningful actions, and whether the original cheap shortcut was attempted.

Do not turn a tiny pilot into claims of universal LLM resistance.
