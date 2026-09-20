# Changelog

All notable changes to NiceTryGPT are documented here.

## [0.2.0] — 2026-09-20

Variety without bloat.

### Added

- a third before/after demo for SQL injection;
- context split as a demonstrated primary resistance pattern;
- shared `examples/REPORT_TEMPLATE.md`;
- CI-enforced acceptance fields for every example;
- public roadmap, related-work notes, and launch kit.

### Changed

- example reports now use one consistent evidence contract;
- contribution guidance now documents the required example layout;
- release-note validation now follows the version in `VERSION` instead of hard-coding v0.1.0;
- README now presents three vulnerability classes.

### v0.2.0 evidence boundary

This release demonstrates deterministic regression properties:

- original challenge solve works;
- identified shortcut is reduced;
- intended vulnerability still yields the runtime flag;
- added human actions are explicitly documented.

It does **not** claim independent LLM resistance results. Those remain the v0.3.0 milestone.

## [0.1.0] — 2026-09-20

First public proof-of-concept release.

### Added

- compact `nice-try-gpt` Agent Skill;
- explicit baseline-first workflow;
- Human Cost Gate;
- four transformation outcomes: `BASELINE FAILED`, `NO CHANGE NEEDED`, `TRANSFORMED PASS`, and `TRANSFORMED FAILED`;
- five lightweight resistance patterns;
- IDOR before/after demo;
- path traversal before/after demo;
- E2E regression suite;
- reproducible skill packaging;
- minimal cross-model evaluation protocol and result schema;
- GitHub Actions validation.

### Design constraints

- preserve the intended vulnerability class;
- preserve the learning objective and prerequisite knowledge;
- keep the human difficulty band stable;
- prefer one minimal resistance move;
- never claim LLM resistance from same-context self-review alone.

NiceTryGPT v0.1.0 is intentionally a small proof of concept, not a benchmark suite or framework.
