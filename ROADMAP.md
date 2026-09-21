# Roadmap

NiceTryGPT is intentionally developed in small evidence-driven steps.

The project should not become a framework just because it can.

> **Increase uncertainty, not complexity.**

## v0.1.0 — proof of concept ✅

Released on 2026-09-20.

The first release established the core method:

- solve the original challenge before changing it;
- identify one cheap LLM shortcut;
- apply the smallest useful transformation;
- enforce a Human Cost Gate;
- verify the transformed challenge end-to-end;
- report fresh-solver results only when they were actually tested.

It demonstrated two vulnerability classes:

- IDOR;
- path traversal.

## v0.2.0 — variety without bloat ✅

Released on 2026-09-20.

v0.2.0 showed that the method can generalize beyond one transformation recipe without turning NiceTryGPT into a framework.

It adds:

- SQL injection as a third vulnerability class;
- context split as a primary non-runtime resistance pattern;
- three demonstrated resistance patterns across the examples:
  - runtime discovery;
  - semantic decoy;
  - context split;
- a shared report template;
- CI enforcement for the example acceptance contract.

Every example now provides:

- a reproducible `before`;
- a reproducible `after`;
- a short NiceTryGPT report;
- a test proving the original solve works;
- a test proving the identified shortcut is reduced;
- a test proving the intended vulnerability still works;
- a human-cost estimate using meaningful actions.

No new infrastructure dependency was introduced.

### Explicit non-goals preserved

v0.2.0 still does not add:

- autonomous multi-model evaluation infrastructure;
- a hosted SaaS;
- a web dashboard;
- a challenge marketplace;
- automatic CTF generation from scratch;
- AI-use detection;
- anti-cheat telemetry;
- model-specific adversarial prompt tricks;
- claims that a transformed challenge is AI-proof.

## v0.3.0 — evaluation

The evaluation infrastructure exists under `evals/`, but raw model results are intentionally empty.

v0.3.0 is the evidence milestone.

In addition to the built-in regression fixtures, v0.3 preparation now includes a pinned registry of independently authored public CTFs. Interstellar Ingress (NexusCTF 2025) and DiceMiner (DiceCTF Quals 2026) have both passed isolated local build/start and baseline-solve checks. Interstellar Ingress has additionally passed a local NiceTryGPT transformation and end-to-end after verification (`TRANSFORMED PASS`); fresh-context solver runs remain pending. DiceMiner still requires its transformed variant before entering the model matrix.

Planned pilot:

```text
2+ challenges
× before / after
× Claude / GPT
× 5 fresh-context runs
```

Exact model versions, tool access, prompt, time budget, action budget, and failures must be recorded.

This milestone waits for access to an appropriate workstation and model tooling. There is no reason to weaken the protocol just to collect results sooner.

## v1.0.0 — stable methodology

A future v1.0.0 should mean that:

- the transformation workflow is stable;
- multiple vulnerability classes have been validated;
- the Human Cost Gate has useful empirical support;
- cross-model evaluation has been reproduced;
- installation and reporting formats no longer change casually.

It should not mean “the repository has many features.”

## Decision rule

Before adding anything, ask:

> Does this make NiceTryGPT better at minimally transforming and validating real CTF challenges?

If the answer is not clearly yes, it probably does not belong in the project.
