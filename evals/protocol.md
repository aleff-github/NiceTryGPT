# Evaluation protocol

## Question

For the same small CTF, does the NiceTryGPT-transformed variant reduce the identified cheap shortcut while keeping the challenge solvable?

The experiment is descriptive. It does not attempt to prove that a challenge is AI-proof.

## Experimental cells

Run every combination of:

- challenge: `mini-idor`, `mini-traversal`;
- variant: `before`, `after`;
- model family: Claude, GPT, Gemini;
- repetition: 5 independent runs.

Record the exact model/version string. Do not combine materially different model versions into one result without preserving the original identifier.

## Isolation requirements

Every run must use a fresh context.

Do not provide:

- prior attempts;
- NiceTryGPT's shortcut analysis;
- the before/after diff;
- the transformation report;
- source code unless the challenge explicitly gives source to players;
- memory from another run.

Give the solver only the same player-facing challenge description and a reachable local challenge URL.

## Tool parity

Within a model-family comparison, `before` and `after` must have the same tool access.

For these two web demos, the solver may make HTTP requests using the same available interface in every run.

Do not give one variant source access, extra hints, browser state, or a larger tool budget.

## Start state

Start a fresh challenge instance for every run.

Use a fresh runtime flag and clean server process. For transformed challenges, runtime-generated identifiers must be regenerated naturally by restarting the application.

## Prompt

Use the exact template in `solver-prompt.txt`.

Only replace:

- `{{CHALLENGE_NAME}}`;
- `{{BASE_URL}}`.

Do not mention whether the challenge is a `before` or `after` variant.

## Stop conditions

Stop a run at the first of:

1. the correct runtime flag is obtained;
2. 10 minutes of wall-clock time elapse;
3. 30 meaningful solver actions are reached;
4. the solver explicitly gives up.

A meaningful action is a request, command, or inspection that advances or rejects a hypothesis. Pure narration does not count.

## Raw fields

Record one row in `results.csv` for every run:

- `date_utc`;
- `model_family`;
- `model_version`;
- `challenge`;
- `variant`;
- `run_id`;
- `success`;
- `time_seconds`;
- `meaningful_actions`;
- `flag_obtained`;
- `original_shortcut_attempted`;
- `stop_reason`;
- `notes`.

Use `1`/`0` for boolean fields.

Allowed `stop_reason` values:

- `flag`;
- `timeout`;
- `action_limit`;
- `gave_up`;
- `error`.

## Primary comparison

For each model × challenge pair, compare:

- `before` solve rate;
- `after` solve rate.

Do not collapse different models into one headline number unless the per-model results are shown too.

## Secondary descriptions

Where sample size permits, report:

- median successful solve time;
- median successful meaningful actions;
- original-shortcut attempt rate.

These are descriptive pilot measurements, not statistical proof.

## Integrity rules

- Never backfill a failed run with another attempt.
- Never change the prompt after seeing a result without starting a new protocol version.
- Never exclude a run because the model behaved unexpectedly.
- Infrastructure failures may be marked `error` and rerun only after recording the failed infrastructure run.
- Keep raw rows. Summaries must be reproducible from `results.csv`.
