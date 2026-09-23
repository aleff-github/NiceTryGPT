# Evaluation evidence status

This file is generated from evals/results.csv and evals/experiment-manifest.json by evals/analyze_evidence.py.
It deliberately separates **solver observations**, **infrastructure failures**, and **illustrative projections**.
Projected values are never inserted into results.csv and are never counted as executed runs.

## Dataset contract

- a row is an **infrastructure failure** only when stop_reason=error and notes contains an explicit infrastructure_error= marker;
- every other row is a **solver observation**, including a non-zero-action solver process that exits with stop_reason=error for a reason not classified as infrastructure;
- zero-action error rows require explicit infrastructure classification and cannot silently enter solver denominators;
- preregistered valid-run targets and collection status are stored in evals/experiment-manifest.json.

## Collection accounting

- raw recorded attempts: **50**;
- valid solver observations: **23**;
- infrastructure failures retained for audit but excluded from solver denominators: **27**;
- valid-observation share of all recorded attempts: **46.0%**;
- infrastructure-failure share of all recorded attempts: **54.0%**.

## Observed evidence

| model | version | challenge | variant | raw n | valid n | infra | solves | solve rate | shortcut attempts | shortcut rate | shortcut 95% Wilson CI |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT | gpt-5.5 (low) | DiceMiner | after | 15 | 3 | 12 | 0/3 | 0.0% | 0/3 | 0.0% | 0.0%–56.1% |
| GPT | gpt-5.5 (low) | DiceMiner | before | 23 | 10 | 13 | 0/10 | 0.0% | 3/10 | 30.0% | 10.8%–60.3% |
| Claude | claude-sonnet-4-6 (low) | Interstellar Ingress | before | 1 | 0 | 1 | 0/0 | - | 0/0 | - | - |
| GPT | gpt-5.5 (low) | Interstellar Ingress | after | 5 | 5 | 0 | 5/5 | 100.0% | 0/5 | 0.0% | 0.0%–43.4% |
| GPT | gpt-5.5 (low) | Interstellar Ingress | before | 6 | 5 | 1 | 5/5 | 100.0% | 5/5 | 100.0% | 56.6%–100.0% |

## Observed effect-size snapshot

| study | solve-rate change AFTER − BEFORE | shortcut-rate change AFTER − BEFORE | collection status |
|---|---:|---:|---|
| interstellar-gpt-5.5-low | +0.0 pp | -100.0 pp | complete |
| diceminer-gpt-5.5-low | +0.0 pp | -30.0 pp | resource-bounded partial |

## Preregistered targets and collection status

| study | target BEFORE | observed BEFORE | target AFTER | observed AFTER | status |
|---|---:|---:|---:|---:|---|
| interstellar-gpt-5.5-low | 5 | 5 | 5 | 5 | complete |
| diceminer-gpt-5.5-low | 10 | 10 | 10 | 3 | resource-bounded partial |
| interstellar-claude-sonnet-4.6-low | 3 | 0 | 3 | 0 | no valid observations |

## Illustrative completion projections

The following values are planning extrapolations, **not experimental results**.

- **diceminer-gpt-5.5-low / AFTER**: if the observed shortcut-attempt rate (0/3) remained unchanged through 10 valid runs, the completed cell would contain approximately **0/10** shortcut attempts.

These projected values are excluded from primary result tables, statistical claims, and results.csv. Small observed samples can leave substantial uncertainty.

## Interpretation boundary

The current evidence is appropriate for a proof-of-concept / preliminary empirical evaluation. It does not establish general or universal LLM resistance. The Claude study contains no valid solver observation and therefore does not establish cross-model replication.

