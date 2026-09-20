# NiceTryGPT ☕🤖

> **Less pattern matching. More actual hacking.**

[![Tests](https://github.com/aleff-github/NiceTryGPT/actions/workflows/test.yml/badge.svg)](https://github.com/aleff-github/NiceTryGPT/actions/workflows/test.yml)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Version: v0.2.0](https://img.shields.io/badge/version-v0.2.0-orange.svg)](#project-status)

### Your CTF got one-shot by an LLM? Nice try.

**NiceTryGPT** is a tiny Agent Skill that takes an existing, authorized CTF challenge, solves it end-to-end, identifies cheap LLM shortcuts, and applies the smallest useful change to reduce them.

**Without making the challenge worse for humans.**

> **Increase uncertainty, not complexity.**

NiceTryGPT is intentionally small: one skill, three tiny demos, one E2E test suite, no framework.

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

NiceTryGPT currently ships with three deliberately tiny examples:

| Example | Before | After | Human cost |
|---|---|---|---|
| `mini-idor` | adjacent order ID gives the flag | foreign order ID must be observed at runtime | +1 request |
| `mini-traversal` | static export path is immediately reusable | export filename changes each run and is exposed by normal activity | +1 request |
| `mini-sqli` | privileged identity is handed to the player | identity must be reconstructed from two normal app surfaces | +2 requests |

All keep the original vulnerability class and learning objective.

### mini-idor

| | Before | After |
|---|---|---|
| Vulnerability | IDOR | IDOR |
| Cheap shortcut | Try the adjacent order ID | Adjacent guess fails |
| Needed observation | None | One runtime activity request |
| Human difficulty | Easy | Still easy |
| Decoy | None | One shallow, safe download decoy |

### mini-traversal

| | Before | After |
|---|---|---|
| Vulnerability | Path traversal | Path traversal |
| Cheap shortcut | Static `../exports/latest.txt` path | Static path fails |
| Needed observation | None | One runtime activity request |
| Human difficulty | Easy | Still easy |
| Decoy | None | None |

The traversal example is intentionally useful as a generalization check: it uses **no honeypot**. The only change is moving one solve-relevant fact from static behavior into ordinary runtime behavior.

### mini-sqli

| | Before | After |
|---|---|---|
| Vulnerability | SQL injection | SQL injection |
| Cheap shortcut | Admin identity shown directly | Old identity fails |
| Needed observation | None | Connect handle + staff email format |
| Primary pattern | None | Context split |
| Human difficulty | Easy | Still easy |
| Runtime randomization | None | None |

The SQLi example deliberately avoids runtime randomization. The vulnerable query is unchanged; the player simply has to connect two nearby, static application clues before applying the same injection primitive.

## Run the demos

No third-party Python packages are required.

```bash
python tests/test_demo.py
python tests/test_release.py
```

The suite verifies that each original challenge is solvable, the identified cheap shortcut stops working after transformation, normal functionality still works, and the intended vulnerability still reaches the runtime flag.

## Package the skill

Build a deterministic ZIP containing only the installable skill:

```bash
python scripts/package_skill.py
```

Output:

```text
dist/nice-try-gpt-v0.2.0.zip
```

The ZIP keeps `nice-try-gpt/` as its root directory, so it can be inspected or copied directly into a compatible Agent Skills location.

## Evaluations

NiceTryGPT now includes a minimal reproducible evaluation protocol under [`evals/`](evals/).

The first planned pilot is:

```text
2 challenges
× 2 variants
× 3 model families
× 5 fresh-context runs
= 60 runs
```

The protocol fixes isolation, tool parity, prompt, stop conditions, and raw result fields. **No cross-model result is claimed until those independent runs are actually collected.**

See [`evals/protocol.md`](evals/protocol.md).


## Roadmap

**v0.2.0 — variety without bloat** is complete: the method now spans three vulnerability classes and includes a non-runtime primary resistance pattern.

The next evidence milestone is **v0.3.0 — independent multi-model evaluation**.

See [`ROADMAP.md`](ROADMAP.md).

## Resistance patterns

NiceTryGPT currently uses a deliberately small menu:

- **Pattern break** — remove a cue that practically names the exploit.
- **Runtime discovery** — make one fact observable through normal interaction.
- **Context split** — connect two nearby pieces of application behavior.
- **State dependency** — let a small amount of ordinary state matter.
- **Semantic decoy** — add one plausible path that is cheap to rule out.

These are options, not a checklist. Most challenges should need zero or one.

See [`resistance-patterns.md`](nice-try-gpt/references/resistance-patterns.md).


## Related work

NiceTryGPT is neither a CTF-solving benchmark nor an anti-cheat system. Its narrow focus is **minimal transformation of an existing, verified challenge** while preserving its learning objective and bounding additional human effort.

See [`docs/related-work.md`](docs/related-work.md) for the current positioning against CTF-agent benchmarks and recent LLM-aware challenge-design work.

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

In v0.2.0, “resistance” means reducing an identified cheap shortcut while preserving the intended challenge. A same-model self-review is not evidence of resistance; fresh-context or cross-model solving is reported separately when actually performed.

## Repository layout

```text
NiceTryGPT/
├── README.md
├── CHANGELOG.md
├── VERSION
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── nice-try-gpt/
│   ├── SKILL.md
│   └── references/
│       └── resistance-patterns.md
├── examples/
│   ├── mini-idor/
│   ├── mini-traversal/
│   └── mini-sqli/
├── evals/
│   ├── README.md
│   ├── protocol.md
│   ├── solver-prompt.txt
│   ├── results.csv
│   └── summarize.py
├── scripts/
│   └── package_skill.py
└── tests/
    ├── test_demo.py
    └── test_release.py
```

## Project status

**v0.2.0 — variety without bloat.**

The method is demonstrated across IDOR, path traversal, and SQL injection. Example reports now follow one CI-enforced acceptance contract, and context split is demonstrated as a primary non-runtime resistance pattern. Independent cross-model evaluation remains the next evidence milestone.

See [`CHANGELOG.md`](CHANGELOG.md).



## Feedback from CTF authors

If you design, organize, or teach CTFs, feedback on the methodology is especially useful.

The most valuable questions are:

- does the Human Cost Gate match real challenge-design constraints?
- which transformations feel fair versus annoying?
- which vulnerability classes are most affected by one-shot LLM solving?
- what evidence would make you trust a before/after transformation?

Use the [CTF author feedback issue form](https://github.com/aleff-github/NiceTryGPT/issues/new?template=ctf-author-feedback.yml). No model-evaluation results are required to give design feedback.

## Contributing

Small, focused contributions are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first.

## Scope and responsible use

NiceTryGPT is intended for CTF challenges, training labs, and systems you own or are explicitly authorized to test. It is not intended to automate testing against third-party systems without authorization.

## Maintainer

Maintained by [@aleff-github](https://github.com/aleff-github).

## License

GNU General Public License v3.0. See [`LICENSE`](LICENSE).
