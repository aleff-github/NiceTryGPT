# Distribution and discovery

NiceTryGPT has one canonical source:

- Repository: https://github.com/aleff-github/NiceTryGPT
- Website: https://aleff-github.github.io/NiceTryGPT/
- Canonical Agent Skill: https://github.com/aleff-github/NiceTryGPT/tree/main/skills/nice-try-gpt
- Standalone mirror: https://github.com/aleff-github/NiceTryGPT/tree/main/nice-try-gpt
- Current release: v0.2.0
- License: GPL-3.0-only
- DOI: https://doi.org/10.5281/zenodo.22858477

## Install

Cross-agent installers compatible with the open Agent Skills format can discover the skill directly from the repository:

```bash
npx -y skills add aleff-github/NiceTryGPT --skill nice-try-gpt
```

Claude Code plugin users can also add the repository marketplace:

```text
/plugin marketplace add aleff-github/NiceTryGPT
/plugin install nice-try-gpt@nicetrygpt
```

For a project-local installation, copy `nice-try-gpt/` to:

```text
.claude/skills/nice-try-gpt/
```

## Directory metadata

Use the canonical repository URL rather than copying the skill into a new repository.

- ID / slug: `nice-try-gpt`
- Name: `NiceTryGPT`
- Category: Security / CTF / Security Education
- Author: Alessandro Greco (`@aleff-github`)
- License: `GPL-3.0-only`
- Source: https://github.com/aleff-github/NiceTryGPT
- Skill path: `skills/nice-try-gpt/SKILL.md`
- Website: https://aleff-github.github.io/NiceTryGPT/

### Short summary

> Adapts authorized CTF challenges to reduce cheap LLM pattern-matching shortcuts while preserving the intended vulnerability and human difficulty.

### Longer summary

> NiceTryGPT is an open-source Agent Skill for CTF authors and security educators. It reproduces an authorized challenge end-to-end, identifies one evidence-backed cheap LLM shortcut, applies the smallest useful human-friendly transformation, and verifies the result while preserving the vulnerability class, learning objective, prerequisite knowledge, and roughly the same human difficulty.

### Suggested keywords

`ctf`, `cybersecurity`, `security-education`, `agent-skills`, `llm`, `ai-security`, `challenge-design`, `claude-code`, `security-training`

## Current ecosystem status

- **Anthropic Agent Skills repository:** upstream submission open as [anthropics/skills#1798](https://github.com/anthropics/skills/pull/1798).
- **AI Skill Store:** NiceTryGPT is already indexed under `aiskillstore/marketplace`; the canonical repository remains the source of truth for current metadata and licensing.
- **skills.sh:** the repository is compatible with the `skills` CLI. skills.sh states that leaderboard entries are created from anonymous installation telemetry after users install a skill.
- **ClaudSkills:** its public crawler discovers eligible public GitHub repositories containing valid `SKILL.md` files; the canonical skill has the required name and description metadata.

Directory inclusion is not an endorsement. Pending submissions should not be described as accepted until the directory maintainers merge or publish them.

## Evidence boundary

Distribution copy should not claim that NiceTryGPT makes challenges AI-proof or universally LLM-resistant.

For v0.2.0, supported claims are limited to:

- three reproducible demonstration vulnerability classes;
- deterministic before/after regression checks;
- a documented Human Cost Gate;
- an explicit authorization boundary;
- an independent multi-model evaluation protocol whose results are not claimed until completed.

See [the evaluation protocol](../evals/protocol.md) and [related work](related-work.md).
