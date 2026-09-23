# Machine-readable transformation report

Every completed NiceTryGPT review should keep two aligned artifacts in the challenge root:

- `nicetrygpt-report.md` — short human-readable rationale;
- `nicetrygpt-report.json` — machine-readable evidence contract.

The JSON format is defined by `schemas/transformation-report.schema.json` in the
NiceTryGPT repository. The packaged skill uses the same field names described
below so a report can be produced without requiring a JSON Schema library.

## Why both formats exist

The Markdown report explains *why* a transformation is reasonable. The JSON
sidecar makes the preservation checks and Human Cost Gate mechanically
inspectable. Neither report replaces the end-to-end tests that actually
exercise the challenge.

Do not write a free-standing `human_cost_gate_pass` field. A validator should
derive the gate from the recorded facts.

## Required JSON sections

- `schema_version`: currently `"1.0"`.
- `challenge`: name, source type, and optional pinned upstream metadata.
- `final_status`: one of the four NiceTryGPT final statuses.
- `baseline`: reproduced baseline, vulnerability class, learning objective,
  prerequisite knowledge, and original difficulty band.
- `shortcut`: evidence-backed shortcut description and an operational
  reduction check.
- `transformation`: zero to two named resistance patterns, a concise summary,
  and files changed.
- `human_cost`: required/optional added meaningful actions, post-change
  difficulty band, and explicit forbidden-cost booleans.
- `verification`: deterministic preservation and end-to-end checks.
- `evidence`: deterministic-validation status, fresh-solver status, and links
  to evaluation artifacts when they exist.

## Derived Human Cost Gate

For `TRANSFORMED PASS`, the validator requires:

1. a reproduced baseline;
2. no more than two resistance patterns;
3. normally no more than three *required* added meaningful actions;
4. unchanged difficulty band;
5. no new exploit primitive, brute force, human-verification gimmick, external
   trivia, or artificial multi-stage chain;
6. passing shortcut-reduction, transformed E2E, vulnerability-preservation,
   learning-objective, prerequisite-knowledge, and flag-semantics checks.

Optional exploration is recorded separately from required work. A single cheap
semantic-decoy probe therefore does not silently become required solve cost.

## Evidence status

`fresh_solver_status` means only:

- `NOT_TESTED`: no isolated solver evaluation was performed;
- `OBSERVED`: one or more valid isolated solver observations exist;
- `NO_VALID_OBSERVATIONS`: attempts exist, but none qualify as solver evidence.

It does **not** mean “LLM resistant.” Use `evaluation_refs` to point to the
protocol/results that support any fresh-solver statement.
