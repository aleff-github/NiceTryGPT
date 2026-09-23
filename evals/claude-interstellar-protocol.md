# Claude Code / Interstellar Ingress cross-model replication

This is a deliberately small cross-model replication pilot. It is designed to
add model-family diversity at substantially lower inference cost than extending
the DiceMiner AFTER sample.

## Research question

Does the completed Interstellar Ingress GPT pattern replicate qualitatively
with a second model family under the same player-facing challenge and the same
narrow tool surface?

The pilot does **not** aim to estimate population-level model performance.

## Frozen matrix

~~~text
Interstellar Ingress
× BEFORE / AFTER
× Claude Sonnet 4.6, effort low
× 3 fresh-context runs per variant
= 6 valid target runs
~~~

The default runner model is `claude-sonnet-4-6`. The exact Claude Code CLI
version is recorded in per-run metadata.

## Why 3 + 3

This replication is intentionally resource-bounded.

Interstellar Ingress is preferred over further DiceMiner repetitions because
the completed GPT pilot solved it in only a few meaningful actions per run.
Three runs per condition provide an inexpensive directional cross-model check
without pretending to be a high-powered benchmark.

## Isolation and tool parity

Every attempt uses:

- a fresh random runtime flag;
- a clean challenge container;
- a fresh temporary working directory;
- non-interactive Claude Code print mode;
- no persisted Claude session;
- strict MCP configuration;
- no built-in Bash, file, browser, or editing tools;
- only `mcp__ctf_http__http_request` and
  `mcp__ctf_http__base64url`;
- the same `evals/solver-prompt.txt` template used by the Codex pilot.

The MCP server restricts HTTP requests to the configured localhost challenge
origin.

## Limits

- wall-clock timeout: 600 seconds;
- meaningful-action limit: 30;
- effort: low;
- web/general execution is unavailable through the runner tool configuration.

An infrastructure, authentication, rate-limit, or usage-limit failure remains
in the audit trail but is excluded from solver-performance denominators.

## Metrics

The same descriptive fields are used as in the GPT Interstellar pilot:

- solve / flag-obtained rate;
- original-shortcut attempt rate;
- successful solve time;
- meaningful actions.

The original shortcut is the same frozen behavior: an unsigned JWT using
`alg: none` with `is_admin: true`.

## Evidence boundary

The six Claude runs are a **cross-model replication pilot**, not a replacement
for a larger multi-model benchmark.

A result is reported only if actually executed. Missing runs are not imputed.
No GPT-to-Claude equivalence claim is made from 3+3 observations.

## Execution status

The first attempted run terminated after approximately 1.2 seconds with zero
meaningful actions because of an infrastructure/access-limit condition. Under
the evaluation rules this is an infrastructure failure, not a solver result.

No valid Claude observation was collected, no missing run was imputed, and the
current v0.3 evidence does not claim cross-model replication. The protocol is
preserved for future reproduction if additional inference resources become
available.

## Running

Preflight:

~~~bash
python3 evals/run_claude_interstellar.py --dry-run
~~~

Pilot:

~~~bash
python3 evals/run_claude_interstellar.py --variant both --runs 3
~~~

If source discovery is ambiguous, provide the same frozen BEFORE and AFTER
directories used by the Codex Interstellar evaluation with `--before-dir` and
`--after-dir`.
