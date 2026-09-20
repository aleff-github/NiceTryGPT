# NiceTryGPT ☕🤖

> **Less pattern matching. More actual hacking.**

Claude solved your CTF before you finished your coffee. Nice try.

**NiceTryGPT** is a tiny Agent Skill for turning an existing, authorized CTF challenge into a slightly more LLM-resistant version **without making it miserable for humans**.

The core idea is deliberately simple:

> **Increase uncertainty, not complexity.**

NiceTryGPT first reproduces the original solve end-to-end. Only then does it look for cheap LLM shortcuts, apply the smallest useful transformation, and solve the challenge again from a clean state.

## Why NiceTryGPT?

LLMs are very good at recognizing familiar CTF patterns. That can turn a small educational challenge into a one-shot template match. NiceTryGPT does not try to make AI fail at all costs. It tries to remove cheap shortcuts while keeping the challenge fair, understandable, and close to its original human difficulty.

## What it preserves

NiceTryGPT tries to preserve:

- the same vulnerability class;
- the same learning objective;
- the same prerequisite knowledge;
- roughly the same human difficulty.

It prefers one small change over a pile of anti-AI tricks. CAPTCHA, brute force, token flooding, pointless encoding, obscure trivia, and artificial exploit chains are explicitly out of scope.

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
│       └── after/
└── tests/
    └── test_demo.py
```

The skill itself is intentionally tiny. The example and tests exist so you can understand the idea without reading a framework.

## Install for Claude Code

Copy the `nice-try-gpt` folder into your target repository as:

```text
.claude/skills/nice-try-gpt/
```

The resulting path should contain:

```text
.claude/skills/nice-try-gpt/SKILL.md
```

You can also package the `nice-try-gpt` folder and upload it as a custom Agent Skill where supported.

## Use it

Ask Claude something like:

```text
Use NiceTryGPT on this CTF. Verify the current challenge end-to-end first, then make the smallest change that reduces cheap LLM shortcuts without increasing the human difficulty band.
```

The expected loop is:

```text
UNDERSTAND → SOLVE → FIND SHORTCUT → MINIMAL CHANGE → SOLVE AGAIN → REPORT
```

If the baseline does not work, NiceTryGPT stops. If the challenge is already fine, `NO CHANGE NEEDED` is a valid result.

## Tiny demo

`examples/mini-idor/before` is an intentionally obvious IDOR challenge. The player owns order `1001`; changing the ID directly reveals the flag.

`examples/mini-idor/after` keeps the same IDOR and the same difficulty band, but adds two lightweight resistance ideas:

- the interesting foreign order is learned from normal runtime activity instead of being the next obvious integer;
- a safe download endpoint provides one cheap semantic decoy that is easy to dismiss.

Run the demo test:

```bash
python tests/test_demo.py
```

The test launches both servers, verifies the original solve, verifies the transformed solve, and checks that the decoy rejects a traversal attempt.

## Design rule

If making the challenge meaningfully more LLM-resistant also makes it substantially worse for humans, **do not make the change**.

## Scope and responsible use

NiceTryGPT is intended for CTF challenges, training labs, and systems you own or are explicitly authorized to test. It is not intended to automate testing against third-party systems without authorization.

## Project status

**v0.1 — proof of concept.** Small on purpose.

The immediate goal is to validate the methodology on a handful of small challenges before adding automation or broader benchmarks.

## Maintainer

Maintained by [@aleff-github](https://github.com/aleff-github).

## License

GNU General Public License v3.0. See [`LICENSE`](LICENSE).
