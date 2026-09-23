# Evaluation protocol

## Research question

For the same authorized CTF challenge, does a NiceTryGPT-transformed variant
reduce the pre-identified cheap shortcut while preserving the intended
challenge?

The evaluation is descriptive. It does not attempt to prove that a challenge is
AI-proof or universally LLM-resistant.

## Protocol registry

The v0.3 evidence dataset is governed by evals/experiment-manifest.json. Each
study points to its frozen challenge-specific protocol:

- GPT / Interstellar Ingress: evals/codex-interstellar-protocol.md;
- GPT / DiceMiner: evals/codex-diceminer-protocol.md;
- Claude / Interstellar Ingress: evals/claude-interstellar-protocol.md.

The early mini-demo 40-run matrix was a planning scaffold, not the external
v0.3 evidence dataset. The bundled mini challenges remain deterministic
regression fixtures.

## Common isolation requirements

Every solver run must use a fresh model context and a fresh challenge instance.

Do not provide prior attempts, NiceTryGPT shortcut analysis, the before/after
diff, the transformation report, source code unless player-facing, or memory
from another run.

Within one study, BEFORE and AFTER must have the same solver prompt, tool access,
stop conditions, and model/version settings except for the challenge variant.

## Frozen shortcut

The original cheap shortcut must be defined before collecting solver
observations. Its definition must not be changed simply because a result is
inconvenient.

## Raw observation schema

results.csv stores one row for every attempted run with date, exact model,
challenge/variant, run ID, success, time, meaningful actions, flag status,
shortcut attempt status, stop reason, and notes.

Boolean fields use 1/0. Allowed stop reasons are flag, timeout, action_limit,
gave_up, and error.

## Evidence-classification contract

The raw row is preserved. Its evidence class is derived mechanically:

- infrastructure failure: stop_reason=error and notes contains an explicit
  infrastructure_error= marker;
- solver observation: every other row.

A non-zero-action solver process that later exits with an unclassified error is
therefore still a solver observation. This preserves the v0.3 accounting
instead of retroactively reinterpreting inconvenient attempts.

A zero-action error row is invalid unless it carries the explicit
infrastructure marker. This prevents empty failures from silently entering
solver denominators.

Run python3 evals/analyze_evidence.py --validate-only to enforce this contract,
unique run IDs, success/flag consistency, manifest membership, and
preregistered valid-run ceilings.

## Resource-bounded stopping

A preregistered target describes intended valid solver observations, not a
promise to spend unlimited inference budget.

If resource or access limits make collection impractical:

1. retain every raw attempt;
2. classify proven infrastructure failures explicitly;
3. leave unexecuted valid runs missing;
4. set collection status to resource_bounded_partial;
5. never impute missing runs.

Any completion extrapolation must be labelled illustrative, excluded from the
raw CSV, and excluded from primary observed result tables.

## Metrics

Primary descriptive metrics are solve rate and original-shortcut attempt rate
among valid solver observations.

Secondary descriptions may include successful solve time, successful meaningful
actions, Wilson intervals, and BEFORE-to-AFTER percentage-point changes.

Small-sample intervals and effects describe the observed sample; they do not
establish universal effects.

## Integrity rules

- Never backfill a valid unfavorable run with another attempt.
- Never delete infrastructure failures from raw accounting.
- Never convert projections or synthetic fixtures into observations.
- Never change prompt or shortcut definition after seeing results without a new
  protocol version.
- Do not collapse materially different model versions into one headline result.
- Keep deterministic transformation validation separate from model evidence.

Summaries must be reproducible from results.csv plus experiment-manifest.json.
