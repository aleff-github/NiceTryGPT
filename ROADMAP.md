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

## v0.3.0 — external empirical evaluation ✅

Released on 2026-09-23.

v0.3.0 is the first external evidence milestone.

Two independently authored public CTFs have passed local baseline,
transformation, vulnerability-preservation, and Human Cost gates:

- **Interstellar Ingress** (NexusCTF 2025);
- **DiceMiner** (DiceCTF Quals 2026).

The collected GPT evaluation is intentionally resource-bounded:

- Interstellar Ingress: 5 valid BEFORE + 5 valid AFTER runs;
- DiceMiner: 10 valid BEFORE + 3 valid AFTER runs;
- infrastructure and usage-limit failures are retained for audit and excluded
  from solver-performance denominators;
- missing DiceMiner AFTER runs remain missing observations and are not imputed.

The completed Interstellar GPT cell preserved 5/5 solve rate in both variants
while the documented shortcut-attempt rate changed from 5/5 BEFORE to 0/5
AFTER.

DiceMiner produced 0/10 solves BEFORE and 0/3 solves AFTER. The documented
shortcut was attempted in 3/10 valid BEFORE runs and 0/3 valid AFTER runs.
Because the AFTER cell is incomplete and neither condition was solved, this is
reported as directional/descriptive evidence only.

A small Claude 3+3 cross-model replication was preregistered, but the first
attempt terminated before any solver action because of an infrastructure /
access-limit failure. No valid Claude run is therefore counted as evidence, and
the project does not claim cross-model replication for v0.3.0.

Illustrative projections are kept separate from observed results and are never
inserted into the raw dataset.

## v0.4.0 — reproducible transformation artifacts

Release target: 2026-09-23.

### Theme

Turn the proof-of-concept methodology into an auditable research artifact without increasing paid benchmark volume.

### Problem

v0.3.0 added external evidence, but several important contracts remained implicit:

- Human Cost Gate results were described in Markdown rather than derived from structured facts;
- study targets and resource-bounded status were partly embedded in analysis code;
- infrastructure classification depended on a notes convention that was not validated as a dataset contract;
- the release workflow did not execute the complete CI suite.

### Deliverables

- machine-readable transformation reports and JSON Schema;
- a derived Human Cost Gate with negative tests;
- an experiment manifest for study identity, targets, and collection status;
- explicit solver-observation versus infrastructure-failure semantics;
- manifest-driven evidence generation with projections kept separate;
- a common evaluation protocol aligned with the actual v0.3 external studies;
- one offline research-artifact verification command used by CI and releases;
- formal methodology and claim-boundary documentation.

### Acceptance criteria

v0.4.0 is ready only when:

- the 50-row v0.3 raw dataset remains unchanged;
- generated evidence still yields 23 solver observations and 27 infrastructure failures;
- Interstellar and DiceMiner observed counts remain exactly those released in v0.3.0;
- all transformation JSON reports pass the derived Human Cost Gate;
- a deliberately over-budget or exploit-changing report fails validation;
- the generated evidence snapshot is reproducible from raw data plus manifest;
- deterministic demos and all evaluation harness tests pass;
- VERSION, skill/plugin metadata, citation metadata, website metadata, roadmap, changelog, and release notes agree on 0.4.0;
- the release workflow runs the complete research-artifact verifier.

### Claims allowed

- v0.4.0 improves reproducibility and auditability;
- the Human Cost Gate is machine-checkable for the recorded artifact fields;
- v0.3.0 observations are reproduced under an explicit evidence contract;
- external evidence remains preliminary and resource-bounded.

### Claims not allowed

- new empirical model evidence;
- universal or general LLM resistance;
- cross-model replication;
- empirically unchanged human difficulty without human-subject evidence;
- treating the seven missing DiceMiner AFTER runs as observations.

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
