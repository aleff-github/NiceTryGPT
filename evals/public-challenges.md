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
| **Interstellar Ingress** | NexusCTF 2025 | JWT/session authentication bypass using an unsecured token | MIT | Docker, Node 22 | **PASS** | Primary candidate |
| **Some Stars Read Fast** | NexusCTF 2025 | SSRF hidden behind a reversible URL encoding layer | MIT | Docker, Node 22 | **PASS** | Primary candidate |
| **Orbital Uplink** | CSAW CTF 2025 Finals | privilege escalation plus improper access control / arbitrary file preview | Apache-2.0 | Docker, Python 3.12 | **PASS** | Primary cross-event candidate |
| **Star Maps** | NexusCTF 2025 | source-map/client-side information disclosure | MIT | Docker, Node 22 | **PASS** | Secondary / methodology stress test |
| **Rolodex** | Pixels Camp 2016/2017, Probely archive | improper authorization via editable role data | Apache-2.0 | legacy Python service | Not yet smoke-tested | Secondary |
| **Get The List** | Pixels Camp 2016/2017, Probely archive | NoSQL injection against MongoDB-backed lookup | Apache-2.0 | legacy Python + MongoDB | Not yet smoke-tested | Secondary |
| **Regain Session** | Pixels Camp 2017, Probely archive | client-side/session/JWT trust failure | Apache-2.0 | Docker Compose | Not yet smoke-tested | Secondary |
| **Heap Dump** | CSAW CTF 2025 Finals | exposed Spring Boot actuator heap dump and credential disclosure | Apache-2.0 | Docker, Java/Gradle + PostgreSQL | Build verification in progress | Secondary |
| **Conditional Constellation** | NexusCTF 2025 | intentionally brute-force a short-lived PIN | MIT | Docker, Node 22 | Not required yet | Negative/control candidate |

## Pinned upstream revisions

### NexusCTF 2025 web challenges

- Repository: https://github.com/michaeldaltonau/sydney-university-nexusctf-2025-web-challenges
- Commit: `ac450407fcdae9057a2063477e751a7b414a9cdd`
- License: MIT

The repository documents all six web challenges and provides Docker packaging and author writeups.

### CSAW CTF 2025 Finals

- Repository: https://github.com/osirislab/CSAW-CTF-2025-Finals-Public
- Commit: `fe9c63ca6c2c7d7a3d753d20d49928b8a40bb09a`
- License: Apache-2.0

The public repository contains challenge source across categories. `web/orbital-uplink/infra/` and `web/heap-dump/heap-dump/` include container build material.

### Probely CTF Challenges

- Repository: https://github.com/Probely/CTF-Challenges
- Commit: `4f5d17a20ac16eebda41144dc33f5f3b7c02cf68`
- License: Apache-2.0

This archive contains older Pixels Camp challenges with source and solution documents. The web challenges are useful for vulnerability diversity, but their older runtime dependencies make them a second-wave target rather than the first pilot.

## Recommended first external pair

The strongest initial pair is:

1. **Interstellar Ingress** — small, modern, reproducible, and built around a recognizable authentication shortcut.
2. **Orbital Uplink** — independently authored by a different CTF, different stack, and different vulnerability shape.

Using two separate competitions reduces the risk of drawing conclusions from one author's challenge-design style.

**Some Stars Read Fast** is the preferred reserve candidate. Its SSRF solve normally uses an external request collector; an evaluation harness should replace that with a controlled local collector so the experiment has no external dependency.

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

Until then, the existing mini challenges remain regression fixtures and no external-evaluation result should be claimed.
