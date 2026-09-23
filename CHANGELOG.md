# Changelog

All notable changes to NiceTryGPT are documented here.

## [0.4.0] — 2026-09-23

### Added

- machine-readable transformation reports and a JSON Schema contract;
- a derived Human Cost Gate validator with negative regression tests;
- structured reports for all bundled demos plus Interstellar Ingress and DiceMiner;
- an experiment manifest recording exact study identity, valid-run targets, protocol paths, and collection status;
- an explicit solver-observation / infrastructure-failure classification contract;
- a formal methodology document and packaged report-format reference;
- a single offline research-artifact verifier used by both CI and release validation.

### Changed

- evidence analysis is manifest-driven instead of hard-coding Interstellar/DiceMiner targets;
- the umbrella evaluation protocol now matches the external v0.3 studies rather than the obsolete mini-demo planning matrix;
- zero-action error rows cannot silently enter solver denominators without an explicit infrastructure marker;
- release validation now executes the complete deterministic/unit suite;
- human-readable reports now have JSON sidecars for machine validation.

### v0.4.0 evidence boundary

v0.4.0 adds **no new paid model observations**. The empirical dataset is the unchanged v0.3.0 dataset: 50 raw attempts, 23 valid solver observations, and 27 infrastructure failures.

The release improves the reproducibility of those observations and the auditability of transformations. It does not establish universal LLM resistance, empirically unchanged human difficulty, or cross-model replication.

## [0.3.0] — 2026-09-23

### Added

- machine-readable `CITATION.cff` citation metadata and human-readable citation guidance;
- CodeMeta 3.1 software metadata;
- an expanded GitHub Pages site with methodology, evidence, FAQ, citation, and project-resource sections;
- `llms.txt` as a concise machine-readable project guide;
- structured bug and methodology-proposal issue forms;
- Dependabot updates for GitHub Actions;
- automated Software Heritage archival requests and preservation/DOI guidance;
- Zenodo archival metadata and version-specific DOI `10.5281/zenodo.22858477` for v0.2.0;
- Google Search Console ownership-verification metadata for the GitHub Pages site;
- native Claude Code plugin manifest and auto-discovered `skills/nice-try-gpt/` layout;
- a synchronization helper and CI checks that keep standalone and plugin skill copies identical;
- standalone Claude Code marketplace metadata for direct repository installation;
- verified cross-agent installation through the open `skills` CLI without telemetry;
- recorded the successful Software Heritage snapshot SWHID `swh:1:snp:6c77799e7623abf2653ab9363d3e2f57899174cf`.
- added a pinned public/open-source CTF candidate registry with verified local baselines for NexusCTF, DiceCTF, and CSAW candidates;
- recorded the first independently authored public CTF transformation: Interstellar Ingress reached local `TRANSFORMED PASS` while preserving the intended `alg:none` weakness;
- completed the Interstellar Ingress GPT fresh-context evaluation (5 valid BEFORE + 5 valid AFTER), preserving 5/5 solve rate while observed shortcut attempts changed from 5/5 to 0/5;
- added DiceMiner as a second independently authored benchmark and collected a resource-bounded GPT sample of 10 valid BEFORE + 3 valid AFTER runs;
- added auditable infrastructure-failure handling, Wilson confidence intervals, effect-size summaries, and explicit separation of observed results from illustrative projections;
- preregistered a low-cost Claude cross-model replication; its first attempt ended before any solver action because of an infrastructure/access-limit failure, so no Claude result is counted as evidence.

### Changed

- release checks now enforce version/date consistency across citation, CodeMeta, website, and machine-readable project metadata;
- release checks now detect broken local Markdown links in the README;
- contribution guidance now documents metadata synchronization and issue-routing expectations;
- canonical author metadata now identifies Alessandro Greco while retaining `@aleff-github` as the public GitHub alias.

### v0.3.0 evidence boundary

This release adds the first external fresh-context empirical evidence for NiceTryGPT.

Observed evidence includes:

- Interstellar Ingress: 5 valid GPT BEFORE + 5 valid GPT AFTER runs, with 5/5 solves in both variants and shortcut attempts changing from 5/5 to 0/5;
- DiceMiner: 10 valid GPT BEFORE + 3 valid GPT AFTER runs, with 0 solves in both observed conditions and shortcut attempts changing from 3/10 to 0/3;
- infrastructure and usage-limit failures retained for audit but excluded from solver-performance denominators;
- Wilson confidence intervals and descriptive effect-size reporting generated from the raw CSV;
- explicit separation of observed evidence from illustrative projections.

The DiceMiner AFTER cell is incomplete and is reported as partial directional evidence only. A preregistered Claude replication produced no valid solver observation because its first attempt ended before any meaningful action due to an infrastructure/access-limit condition. v0.3.0 therefore makes no cross-model replication claim and no universal LLM-resistance claim.

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
