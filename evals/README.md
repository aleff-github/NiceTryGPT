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

### Codex / Interstellar pilot

A fixed fresh-solver pilot is also prepared for Interstellar Ingress:

- variants: before and after;
- model: gpt-5.5 with low reasoning effort;
- independent runs per variant: 5;
- fresh challenge build and random flag for every attempt;
- ephemeral Codex context with web search and general execution tools disabled;
- only localhost HTTP interaction plus a generic Base64URL helper;
- 10-minute and 30-action limits;
- raw JSONL/action traces saved locally and summary rows appended to results.csv.

Run python evals/run_codex_interstellar.py --dry-run before collecting data. The fixed procedure and evidence boundary are documented in codex-interstellar-protocol.md.

## Files

- [`protocol.md`](protocol.md) — fixed experimental procedure;
- [`public-challenges.md`](public-challenges.md) — public/open-source candidate registry and entry gate;
- [`interstellar-ingress.md`](interstellar-ingress.md) — first independently authored public challenge transformation record;
- [`codex-interstellar-protocol.md`](codex-interstellar-protocol.md) — fixed Codex fresh-solver pilot;
- [`run_codex_interstellar.py`](run_codex_interstellar.py) — automated Codex pilot runner;
- [`solver-prompt.txt`](solver-prompt.txt) — prompt template used for every run;
- [`results.csv`](results.csv) — raw observations;
- [`summarize.py`](summarize.py) — dependency-free summary script.

## Summarize collected results

```bash
python evals/summarize.py
```

The primary metric is solve rate. Secondary descriptive metrics are time, meaningful actions, and whether the original cheap shortcut was attempted.

Do not turn a tiny pilot into claims of universal LLM resistance.
