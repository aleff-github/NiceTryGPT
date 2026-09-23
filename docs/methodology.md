# NiceTryGPT methodology

NiceTryGPT is a minimal-diff methodology for adapting existing, authorized CTF
challenges when a verified solve exposes a cheap LLM shortcut.

> **Increase uncertainty, not complexity.**

The method is intentionally narrower than a CTF generator, anti-cheat system,
or model benchmark. A transformed challenge may still be solved quickly by a
capable model.

## Transformation estimand

For a specific challenge and a pre-identified shortcut, NiceTryGPT asks whether
a bounded transformation can reduce reliance on that shortcut while preserving
the intended challenge.

The target is therefore **shortcut reduction under preservation constraints**,
not a generic decrease in model solve rate.

## Preservation invariants

A successful transformation preserves:

1. vulnerability class;
2. learning objective;
3. prerequisite knowledge;
4. flag/success semantics;
5. the human difficulty band.

The original challenge must first be solved end-to-end through the
player-facing surface. If the baseline cannot be reproduced, transformation
stops with `BASELINE FAILED`.

## Operational shortcut definition

A shortcut must be grounded in baseline behavior and described so it can be
tested. Examples include an adjacent object ID, a static path, or a privileged
identity exposed in one response.

The report records both:

- the shortcut description;
- a concrete reduction check against the transformed challenge.

This prevents “the challenge feels less obvious” from being treated as
evidence.

## Transformation budget

Default to one resistance pattern. A second is allowed only when the first is
insufficient and the Human Cost Gate still passes.

The supported patterns are deliberately small:

- pattern break;
- runtime discovery;
- context split;
- state dependency;
- semantic decoy.

The transformation budget is not a target. Zero patterns and
`NO CHANGE NEEDED` are valid outcomes.

## Human Cost Gate

For a transformed pass, required added player work should normally remain
within 0–3 meaningful actions. A meaningful action is an interaction that
materially advances or rejects a hypothesis.

The gate rejects transformations that introduce a new exploit primitive, brute
force, CAPTCHA/human verification, obscure external trivia, or an artificial
multi-stage chain. The post-change difficulty band must remain the same.

Required solve work and optional exploration are recorded separately.

The machine-readable report does not contain a self-asserted gate result.
`scripts/validate_transformation_reports.py` derives it from the facts in the
report.

## Evidence classes

NiceTryGPT keeps four categories separate:

- **deterministic validation** — local tests of baseline solve, shortcut
  reduction, vulnerability preservation, and transformed E2E behavior;
- **solver observations** — valid isolated model attempts under a frozen
  protocol;
- **infrastructure failures** — recorded attempts that did not constitute
  solver evidence;
- **projections** — explicitly labelled planning extrapolations that are never
  inserted into the raw observation dataset.

Fresh-solver observations strengthen an evaluation, but they are not required
to establish deterministic transformation correctness.

## Claims

Supported wording should match the evidence actually present, for example:

- “deterministically validated transformation”;
- “observed shortcut reduction”;
- “preliminary / proof-of-concept evidence”;
- “resource-bounded evaluation.”

Do not claim:

- AI-proof or LLM-proof challenges;
- universal LLM resistance;
- cross-model replication without valid observations from the additional model
  family;
- missing runs as failures, successes, or completed observations.

## Reproducibility contract

A research-grade NiceTryGPT transformation should preserve:

- a pinned or otherwise reproducible baseline;
- a human-readable transformation report;
- its machine-readable JSON companion;
- deterministic verification;
- the frozen evaluation protocol when model runs are performed;
- raw attempts, including infrastructure failures;
- generated summaries that can be recreated from the raw dataset.

This contract is the v0.4 direction: improve auditability before increasing
benchmark volume.


## Structural generalization

v0.5.0 adds a separate structural-generalization layer. It asks whether the same preservation and reporting contract can be represented across heterogeneous challenge shapes, vulnerability classes, and resistance patterns.

The generated snapshot in `docs/generalization-status.md` is derived from committed transformation reports. Bundled demos additionally use executable challenge adapters that identify the before/after entrypoints and their deterministic verification functions.

This layer is deliberately not a statistical model-generalization claim. A larger count of vulnerability classes or represented patterns does not imply that a transformation will resist every model, that each pattern works equally well, or that the challenge population has been sampled representatively.

Human difficulty is also not inferred from the adapter matrix. Without participant data, NiceTryGPT reports a bounded structural Human Cost Gate: preserved vulnerability/learning prerequisites and difficulty band, no new exploit primitive or artificial friction, and at most three required added meaningful actions for a transformed pass.
