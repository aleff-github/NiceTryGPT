# Evaluation evidence status

> Collection snapshot recorded on 2026-09-23 from the local benchmark dataset.
> Before merging this branch, regenerate this file from the committed
> `evals/results.csv` with:
>
> ```bash
> python3 evals/analyze_evidence.py --write evals/evidence-status.md
> ```

This report separates **observed evidence** from **illustrative projections**.
Projected values are never counted as executed runs.

## Collection accounting

Across the GPT external-challenge collection:

- raw recorded attempts: **49**;
- valid solver attempts: **23**;
- infrastructure/usage-limit failures retained for audit but excluded from
  solver-performance denominators: **26**;
- valid-attempt share of all recorded attempts: **46.9%**;
- infrastructure-failure share of all recorded attempts: **53.1%**.

The valid observations cover 23 of the 30 originally targeted GPT solver runs
across Interstellar Ingress and DiceMiner (**76.7%**).

## Observed evidence

| model | challenge | variant | raw n | valid n | infra | solves | solve rate | shortcut attempts | shortcut rate | shortcut 95% Wilson CI |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GPT-5.5 low | Interstellar Ingress | BEFORE | 6 | 5 | 1 | 5/5 | 100% | 5/5 | 100% | 56.6%–100% |
| GPT-5.5 low | Interstellar Ingress | AFTER | 5 | 5 | 0 | 5/5 | 100% | 0/5 | 0% | 0%–43.4% |
| GPT-5.5 low | DiceMiner | BEFORE | 23 | 10 | 13 | 0/10 | 0% | 3/10 | 30% | 10.8%–60.3% |
| GPT-5.5 low | DiceMiner | AFTER | 15 | 3 | 12 | 0/3 | 0% | 0/3 | 0% | 0%–56.1% |

Infrastructure failures are not interpreted as solver failures.

## Observed effect-size snapshot

| challenge | solve-rate change AFTER − BEFORE | shortcut-rate change AFTER − BEFORE | status |
|---|---:|---:|---|
| Interstellar Ingress | +0.0 pp | -100.0 pp | complete |
| DiceMiner | +0.0 pp | -30.0 pp | AFTER partial |

The DiceMiner effect size is descriptive only because the AFTER denominator is
3 rather than the preregistered 10.

## Resource-bounded DiceMiner collection

DiceMiner was preregistered for 10 valid runs per variant. The BEFORE cell was
completed. The AFTER cell was stopped at 3 valid runs because repeated
inference-usage limits made the remaining repetitions disproportionately costly.

The seven missing AFTER runs remain **missing observations**. They are not
imputed as failures, successes, or shortcut-free runs.

## Illustrative completion projection

The following is a planning extrapolation, **not an experimental result**.

If the currently observed DiceMiner AFTER shortcut-attempt rate of 0/3 remained
unchanged through the originally planned 10 valid runs, the completed AFTER cell
would contain approximately **0/10** shortcut attempts, compared with the
observed **3/10** BEFORE.

This projection is excluded from `results.csv`, primary result tables, and
empirical claims. The 0/3 AFTER observation still has a wide 95% Wilson interval
(approximately 0%–56.1%), so the partial DiceMiner result should be interpreted
as directional only.

## Interpretation boundary

Interstellar Ingress provides the completed controlled GPT result: solve rate
was preserved at 5/5 in both variants while the documented shortcut-attempt
rate changed from 5/5 BEFORE to 0/5 AFTER.

DiceMiner contributes a second, independently authored challenge with a
different vulnerability shape, but its model-evaluation evidence is partial:
the solver did not solve either observed condition, and the AFTER sample is
small.

Together these results support a **preliminary / proof-of-concept empirical
evaluation** of NiceTryGPT. They do not establish general LLM resistance.

The next high-information, low-cost extension is a small cross-model replication
on Interstellar Ingress rather than additional expensive DiceMiner repetitions.
