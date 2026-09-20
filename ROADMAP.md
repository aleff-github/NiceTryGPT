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

It currently demonstrates two vulnerability classes:

- IDOR;
- path traversal.

Both examples are dependency-free and tested in CI.

## v0.2.0 — variety without bloat

### Goal

Show that the NiceTryGPT method generalizes beyond one transformation recipe.

v0.2.0 is **not** about adding a dashboard, database, orchestration layer, or large benchmark suite.

It is about adding a small amount of carefully chosen variety.

### Release criteria

v0.2.0 should ship only when all of the following are true:

- at least three vulnerability classes are represented;
- at least three resistance patterns are demonstrated across the examples;
- at least one example does **not** rely on runtime discovery;
- every example has:
  - a reproducible `before`;
  - a reproducible `after`;
  - a short NiceTryGPT report;
  - a test proving the original solve works;
  - a test proving the identified shortcut is reduced;
  - a test proving the intended vulnerability still works;
- human-cost estimates use the same definition of meaningful action;
- no new infrastructure dependency is introduced without a demonstrated need.

### Planned work

#### 1. Add a mini SQL injection example

Preferred direction:

- Python standard library;
- `sqlite3`;
- easy human difficulty;
- same SQL injection before and after;
- transformed version should use **context split** or **pattern break**, not another runtime-randomized identifier.

The purpose is to test the methodology, not to create a clever SQLi challenge.

#### 2. Standardize example acceptance checks

Every example should answer the same five questions:

1. Can the original challenge be solved end-to-end?
2. What exact cheap shortcut was identified?
3. Does the transformed challenge remove or reduce that shortcut?
4. Does the original vulnerability class still produce the flag?
5. What is the additional human cost in meaningful actions?

The answers should remain readable by humans and directly testable where possible.

#### 3. Exercise a third resistance pattern

The current examples mainly demonstrate runtime discovery, with one shallow semantic decoy.

v0.2.0 should deliberately exercise a different primary pattern such as:

- context split;
- pattern break;
- state dependency.

Do not add a pattern merely to satisfy the count. The challenge must justify it.

#### 4. Keep the installable skill small

Changes to `SKILL.md` require evidence from an example or evaluation.

Avoid adding rules for hypothetical edge cases.

### Explicit non-goals

The following are out of scope for v0.2.0:

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

The evaluation infrastructure already exists under `evals/`, but raw model results are intentionally empty.

v0.3.0 is the evidence milestone.

Planned pilot:

```text
2+ challenges
× before / after
× Claude / GPT / Gemini
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
