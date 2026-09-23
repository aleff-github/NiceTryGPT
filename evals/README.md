# NiceTryGPT evaluations

This directory contains the reproducible evaluation layer for NiceTryGPT. It
tests a narrow question: whether a minimal transformation reduces a specific,
pre-identified shortcut while preserving the intended challenge.

It is intentionally not a large benchmark framework.

## v0.3 observed evidence

The published raw dataset is results.csv. Its collection plan and status are
machine-readable in experiment-manifest.json.

- Interstellar Ingress / GPT-5.5 low: 5 valid BEFORE + 5 valid AFTER
  observations; 5/5 solves in both cells; shortcut attempts 5/5 to 0/5.
- DiceMiner / GPT-5.5 low: 10 valid BEFORE + 3 valid AFTER observations;
  0 solves in both observed cells; shortcut attempts 3/10 to 0/3.
- Interstellar Ingress / Claude Sonnet 4.6: one recorded attempt, zero valid
  solver observations because it ended as infrastructure/access failure before
  meaningful action.

Infrastructure failures remain in raw accounting and are excluded from solver
denominators only through the explicit classification contract in protocol.md.
The missing DiceMiner AFTER observations remain missing. No synthetic rows are
created.

## Reproduce the evidence snapshot

Validate raw data and targets:

    python3 evals/analyze_evidence.py --validate-only

Regenerate the committed evidence report:

    python3 evals/analyze_evidence.py --write evals/evidence-status.md

Print the compact summary:

    python3 evals/summarize.py

## Experiment registry

experiment-manifest.json is the dataset-level source of truth for study
identity, exact model/version, frozen protocol path, target valid runs,
collection status, and whether an illustrative projection is allowed.

This removes challenge-specific target counts from analysis code.

## Transformation evidence

Machine-readable external transformation records live under
evals/transformations/. They encode deterministic preservation checks
separately from fresh-solver evidence.

## Main files

- protocol.md: common evaluation and classification contract;
- experiment-manifest.json: study registry and targets;
- results.csv: raw attempts;
- analyze_evidence.py: validation, intervals, effects, and projections;
- evidence-status.md: generated snapshot;
- summarize.py: dependency-free console summary;
- public-challenges.md: external candidate registry.

The current evidence supports preliminary / proof-of-concept claims only.
