# Changelog

All notable changes to NiceTryGPT are documented here.

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
