# NiceTryGPT ☕🤖

> **Less pattern matching. More actual hacking.**

[![Tests](https://github.com/aleff-github/NiceTryGPT/actions/workflows/test.yml/badge.svg)](https://github.com/aleff-github/NiceTryGPT/actions/workflows/test.yml)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Status: v0.1](https://img.shields.io/badge/status-v0.1%20POC-orange.svg)](#project-status)

### Your CTF got one-shot by an LLM? Nice try.

**NiceTryGPT** is a tiny Agent Skill that takes an existing, authorized CTF challenge, solves it end-to-end, identifies cheap LLM shortcuts, and applies the smallest useful change to reduce them.

**Without making the challenge worse for humans.**

> **Increase uncertainty, not complexity.**

NiceTryGPT is intentionally small: one skill, one demo, one E2E test, no framework.

## Try it in 30 seconds

For a project-local Claude Code skill, copy the `nice-try-gpt` directory into your CTF repository as:

```text
.claude/skills/nice-try-gpt/
└── SKILL.md
```

Then ask:

```text
Use NiceTryGPT on this CTF. Solve it first, identify the cheapest LLM shortcut,
make the smallest useful change, and verify the result end-to-end.
```

Claude Code discovers project skills from `.claude/skills/<skill-name>/SKILL.md`. Custom skills can also be packaged and uploaded where supported. See the [official Agent Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

## How it works

```text
UNDERSTAND
    ↓
SOLVE ORIGINAL
    ↓
FIND ONE CHEAP SHORTCUT
    ↓
MAKE 0–2 SMALL CHANGES
    ↓
SOLVE AGAIN
    ↓
REPORT
```

If the original challenge cannot be reproduced, NiceTryGPT stops. If the challenge is already fine, `NO CHANGE NEEDED` is a valid result.

## What it preserves

A successful transformation keeps:

- the same vulnerability class;
- the same learning objective;
- the same prerequisite knowledge;
- the same flag/success semantics;
- roughly the same human difficulty band.

The default is **one resistance change**. A second change is justified only when the first one is insufficient and the human-cost gate still passes.

## Before / after

The included `mini-idor` example is intentionally tiny.

| | Before | After |
|---|---|---|
| Vulnerability | IDOR | IDOR |
| Learning objective | Missing object-level authorization | Same |
| Cheap shortcut | Try the adjacent order ID | Adjacent guess fails |
| Needed observation | None | One runtime activity request |
| Human difficulty | Easy | Still easy |
| Decoy | None | One shallow, safe download decoy |

The transformed version does **not** hide the vulnerability behind complexity. It simply moves one solve-relevant fact into runtime behavior, so the solver has to observe the application instead of relying only on a static pattern.

## Run the demo

No third-party Python packages are required.

```bash
python tests/test_demo.py
```

The test verifies that:

- the original challenge is solvable through the obvious adjacent-ID shortcut;
- normal functionality still works after the transformation;
- the old adjacent-ID shortcut no longer works;
- the useful foreign object reference must be learned at runtime;
- the same IDOR still yields the flag;
- the semantic decoy behaves normally and rejects traversal.

Expected result:

```text
PASS  skill metadata
PASS  before baseline
PASS  after transformed

NiceTryGPT demo E2E: PASS
```

## Resistance patterns

NiceTryGPT currently uses a deliberately small menu:

- **Pattern break** — remove a cue that practically names the exploit.
- **Runtime discovery** — make one fact observable through normal interaction.
- **Context split** — connect two nearby pieces of application behavior.
- **State dependency** — let a small amount of ordinary state matter.
- **Semantic decoy** — add one plausible path that is cheap to rule out.

These are options, not a checklist. Most challenges should need zero or one.

See [`resistance-patterns.md`](nice-try-gpt/references/resistance-patterns.md).

## What NiceTryGPT will not do

It will not intentionally make a challenge annoying just to slow down an AI.

That means no:

- CAPTCHA or human-verification gimmicks;
- brute force as a design requirement;
- token/context flooding;
- pointless encoding layers;
- obscure trivia;
- fake flags or destructive traps;
- artificial five-stage exploit chains;
- piles of honeypots.

If LLM resistance and human experience conflict, **the human player wins**.

## What “LLM-resistant” means here

NiceTryGPT does **not** claim to prove that a challenge is AI-proof.

In v0.1, “resistance” means reducing an identified cheap shortcut while preserving the intended challenge. A same-model self-review is not evidence of resistance; fresh-context or cross-model solving should be reported separately when actually performed.

## Repository layout

```text
NiceTryGPT/
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── nice-try-gpt/
│   ├── SKILL.md
│   └── references/
│       └── resistance-patterns.md
├── examples/
│   └── mini-idor/
│       ├── before/
│       ├── after/
│       └── nicetrygpt-report.md
└── tests/
    └── test_demo.py
```

## Project status

**v0.1 — tiny on purpose.**

The current goal is to validate the method on a small set of reproducible CTFs before adding broader benchmarks, automation, or extra infrastructure.

## Contributing

Small, focused contributions are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first.

## Scope and responsible use

NiceTryGPT is intended for CTF challenges, training labs, and systems you own or are explicitly authorized to test. It is not intended to automate testing against third-party systems without authorization.

## Maintainer

Maintained by [@aleff-github](https://github.com/aleff-github).

## License

GNU General Public License v3.0. See [`LICENSE`](LICENSE).
