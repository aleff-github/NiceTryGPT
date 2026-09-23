# Public CTF benchmark candidates

NiceTryGPT's built-in mini challenges are useful deterministic regression fixtures, but they are not a substitute for evaluation on independently authored CTFs.

This document records public, open-source challenge candidates for the v0.3 evidence milestone. It is a candidate registry, not a claim that every challenge has already been transformed successfully.

## Selection rules

A public challenge is eligible only when all of the following hold:

1. the source is publicly available under an explicit open-source license;
2. the challenge is from a completed/public CTF or an openly published challenge archive;
3. it can be run locally or in an isolated container without attacking a live third-party service;
4. the intended solve is documented well enough to verify that NiceTryGPT preserves the learning objective;
5. the player-facing surface can be reproduced without giving the solver source or writeup access;
6. the challenge is small enough that a before/after transformation can be reviewed as a bounded diff.

Prefer challenge diversity across authors, competitions, vulnerability classes, and implementation stacks.

## Reproducibility policy

For every challenge that enters an actual evaluation:

- record the upstream repository and exact commit SHA;
- preserve the upstream license and attribution;
- run the challenge locally;
- do not test the original organizer's live infrastructure;
- reproduce the intended baseline solve before transforming anything;
- keep the upstream source separate from NiceTryGPT-owned transformation patches where practical;
- provide models only the player-facing challenge information allowed by the protocol.

Public writeups create a possible model-training contamination risk. That is not hidden: the before/after comparison must be interpreted as testing whether a minimal transformation reduces a shortcut on a known public challenge, not as measuring performance on an unseen benchmark.

## Shortlist

| Challenge | Event / source | Intended security idea | License | Local packaging | Smoke status | Role |
|---|---|---|---|---|---|---|
| **Interstellar Ingress** | NexusCTF 2025 | JWT/session authentication bypass using an unsecured token | MIT | Docker, Node 22 | **TRANSFORMED PASS — GPT 5+5 complete** | Primary candidate |
| **DiceMiner** | DiceCTF Quals 2026 | IEEE-754 coordinate aliasing causes repeated reward accounting for one mined block | AGPL-3.0 | Docker, Node 22 | **TRANSFORMED PASS — GPT BEFORE complete, AFTER partial** | Primary cross-event candidate |
| **Some Stars Read Fast** | NexusCTF 2025 | SSRF hidden behind a reversible URL encoding layer | MIT | Docker, Node 22 | **PASS — baseline pending** | Reserve |
| **Orbital Uplink** | CSAW CTF 2025 Finals | privilege escalation plus improper access control / arbitrary file preview | Apache-2.0 | Docker, Python 3.12 | **PASS — baseline solved*** | Cross-check candidate |
| **Star Maps** | NexusCTF 2025 | source-map/client-side information disclosure | MIT | Docker, Node 22 | **PASS** | Secondary / methodology stress test |
| **Rolodex** | Pixels Camp 2016/2017, Probely archive | improper authorization via editable role data | Apache-2.0 | legacy Python service | Not yet smoke-tested | Secondary |
| **Get The List** | Pixels Camp 2016/2017, Probely archive | NoSQL injection against MongoDB-backed lookup | Apache-2.0 | legacy Python + MongoDB | Not yet smoke-tested | Secondary |
| **Regain Session** | Pixels Camp 2017, Probely archive | client-side/session/JWT trust failure | Apache-2.0 | Docker Compose | Not yet smoke-tested | Secondary |
| **Heap Dump** | CSAW CTF 2025 Finals | exposed Spring Boot actuator heap dump and credential disclosure | Apache-2.0 | Docker, Java/Gradle + PostgreSQL | **PASS*** | Secondary |
| **Conditional Constellation** | NexusCTF 2025 | intentionally brute-force a short-lived PIN | MIT | Docker, Node 22 | Not required yet | Negative/control candidate |

## Pinned upstream revisions

### NexusCTF 2025 web challenges

- Repository: https://github.com/michaeldaltonau/sydney-university-nexusctf-2025-web-challenges
- Commit: `ac450407fcdae9057a2063477e751a7b414a9cdd`
- License: MIT

The repository documents all six web challenges and provides Docker packaging and author writeups.

### DiceCTF Quals 2026

- Repository: https://github.com/dicegang/dicectf-quals-2026-challenges
- Commit: `308891d205d5d16329b0c0e888f430f73b35d54b`
- License: AGPL-3.0

`web/diceminer/challenge/` is a self-contained Node 22 Docker challenge. The baseline was reproduced locally from the pinned source. The exploit relies on JavaScript Number precision at the safe-integer boundary: a carefully chosen large coordinate makes repeated numeric increments alias to the same block key during one dig operation, while reward accounting and hauling-cost accounting diverge. The local solve reached the flag through the intended game API without reading the flag from source. The NiceTryGPT AFTER variant has also passed the canonical-shortcut reduction gate, vulnerability-preservation gate, Human Cost Gate, and runtime-randomization check. Its frozen transformation record is in [`diceminer.md`](diceminer.md).

### CSAW CTF 2025 Finals

- Repository: https://github.com/osirislab/CSAW-CTF-2025-Finals-Public
- Commit: `fe9c63ca6c2c7d7a3d753d20d49928b8a40bb09a`
- License: Apache-2.0

The public repository contains challenge source across categories. `web/orbital-uplink/infra/` and `web/heap-dump/heap-dump/` include container build material.

\* The archived `Orbital Uplink` Dockerfile writes the flag to `/app/flag.txt`, while the application and official solution expect `/flag.txt`. The baseline solve succeeds after copying the already bundled flag to the expected path at container startup. This is recorded as a harness compatibility restoration, not a NiceTryGPT transformation.

\* `Heap Dump` still references the retired competition hostname `heap-dump.ctf.csaw.io` in its datasource URL. The unmodified container starts successfully when that hostname is mapped to `127.0.0.1`, where the bundled PostgreSQL service already runs. This compatibility mapping is part of the local harness, not a challenge transformation.

### Probely CTF Challenges

- Repository: https://github.com/Probely/CTF-Challenges
- Commit: `4f5d17a20ac16eebda41144dc33f5f3b7c02cf68`
- License: Apache-2.0

This archive contains older Pixels Camp challenges with source and solution documents. The web challenges are useful for vulnerability diversity, but their older runtime dependencies make them a second-wave target rather than the first pilot.

## Recommended first external pair

The strongest initial pair is:

1. **Interstellar Ingress** — small, modern, reproducible, and built around a recognizable authentication shortcut.
2. **DiceMiner** — independently authored for DiceCTF 2026, recent, self-contained, and based on a very different numeric/state-accounting failure.

Both have now passed local build/start and end-to-end baseline solve checks from pinned public source. Using two separate competitions and substantially different vulnerability shapes reduces the risk of drawing conclusions from one author's challenge-design style or one transformation recipe.

**Orbital Uplink** is the preferred cross-check candidate once its documented archive-path restoration is included in the harness. **Some Stars Read Fast** remains the preferred SSRF reserve candidate. Its SSRF solve normally uses an external request collector; an evaluation harness should replace that with a controlled local collector so the experiment has no external dependency.

## Negative-control rationale

NiceTryGPT should not transform every challenge.

**Conditional Constellation** is useful because brute-forcing the PIN is the explicit learning objective. A transformation that merely makes brute force harder could violate the Human Cost Gate or change the task itself. It can therefore test whether the methodology is willing to return `NO CHANGE NEEDED` rather than forcing a resistance modification.

**Star Maps** is another useful stress case: its learning objective depends on discovering exposed source-map information. Removing the exposure outright would likely destroy the intended challenge instead of minimally reducing an LLM shortcut.

## Entry gate for v0.3

A candidate moves from this shortlist into the model-evaluation matrix only after all of these are true:

- local build/start passes;
- baseline solve is reproduced end-to-end;
- intended vulnerability/learning objective is written down;
- NiceTryGPT produces either a Human-Cost-Gate-compliant transformation or `NO CHANGE NEEDED`;
- transformed instance is solved end-to-end;
- attribution and license obligations are recorded;
- the exact player-facing prompt and local harness are frozen.

## Verification completed on 2026-09-20

The following checks were executed against isolated local containers built from the pinned upstream repositories:

- **Interstellar Ingress:** build/start PASS; intended unsecured-JWT baseline solve PASS; runtime flag obtained through the vulnerable session flow.
- **DiceMiner:** build/start PASS; precision-loss/reward-accounting baseline solve PASS; runtime flag purchased through the game API.
- **Orbital Uplink:** build/start PASS; intended admin-parameter + arbitrary-preview solve PASS after restoring the archived flag to the path expected by the application and official solution.
- **Some Stars Read Fast:** build/start PASS; full SSRF baseline solve not yet frozen because the public solve normally depends on an external request collector.
- **Star Maps:** build/start PASS; retained as a methodology stress case.
- **Heap Dump:** build/start PASS when the retired competition database hostname is mapped to the PostgreSQL service already bundled in the container.

No organizer-hosted live challenge endpoint was attacked or used for these checks.

Interstellar Ingress now also has a verified NiceTryGPT after-variant and a completed GPT fresh-context pilot: 5/5 valid solves in both BEFORE and AFTER, with the documented shortcut attempted in 5/5 BEFORE runs and 0/5 AFTER runs. The transformation record is documented in [`interstellar-ingress.md`](interstellar-ingress.md).

DiceMiner now also has a verified NiceTryGPT after-variant. The resource-bounded GPT collection reached 10 valid BEFORE runs and 3 valid AFTER runs before further repetitions were stopped for inference/usage-budget reasons. The observed shortcut-attempt counts were 3/10 BEFORE and 0/3 AFTER; neither variant produced a model solve. The incomplete AFTER cell is reported as partial evidence only, and any completion estimate is labeled as a projection rather than an observed result. Its frozen transformation record is documented in [`diceminer.md`](diceminer.md).\n\nFor the remaining candidates, the existing mini challenges remain the regression fixtures until a verified after-variant exists.
