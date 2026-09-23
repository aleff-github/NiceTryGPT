# Distribution and discovery

NiceTryGPT has one canonical source:

- Repository: https://github.com/aleff-github/NiceTryGPT
- Website: https://aleff-github.github.io/NiceTryGPT/
- Canonical Agent Skill: https://github.com/aleff-github/NiceTryGPT/tree/main/skills/nice-try-gpt
- Standalone mirror: https://github.com/aleff-github/NiceTryGPT/tree/main/nice-try-gpt
- Current release: v0.3.0
- License: GPL-3.0-only
- Archived v0.2.0 DOI: https://doi.org/10.5281/zenodo.22858477
- v0.3.0 DOI: pending Zenodo release deposit

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

Last verified: **2026-09-20**.

| Channel | Status | Evidence / note |
|---|---|---|
| Anthropic Agent Skills repository | **Submitted** | Upstream PR [anthropics/skills#1798](https://github.com/anthropics/skills/pull/1798) is open. |
| AI Skill Store / `aiskillstore/marketplace` | **Listed** | Initial automated submission was merged as [aiskillstore/marketplace#3490](https://github.com/aiskillstore/marketplace/pull/3490) with a `safe` security verdict. A metadata refresh has been submitted so the indexed copy picks up the current GPL-3.0-only frontmatter. |
| AgentSkill.sh | **Imported** | Public intake returned one imported NiceTryGPT skill with security score 100. |
| agent-skills.md | **Imported** | Public intake accepted the repository and reported one skill added. |
| skills.re | **Submitted** | Public intake accepted one NiceTryGPT skill into its upload workflow. |
| SkillMap | **Submitted** | Marketplace consideration request was accepted by its public feedback endpoint. |
| skills.sh | **Installer-compatible** | The `skills` CLI successfully discovers and installs `nice-try-gpt`. The project does not generate synthetic leaderboard installs; real user installs may be reflected by skills.sh telemetry. |
| ClaudSkills | **Crawler-ready** | The public repository exposes valid `SKILL.md` metadata and canonical discovery links; no claim of manual fast-track acceptance is made. |
| SkillsMD | **Intake error** | Its public submission endpoint returned `GitHub repo not found` for the valid public repository, so repeated automated retries are intentionally avoided. |
| skillsrep.com | **Temporarily unavailable** | A submission attempt encountered an upstream HTTP 521 response; no acceptance is claimed. |

The canonical repository remains the source of truth for current content, licensing, and evidence. Directory inclusion is not an endorsement. Pending submissions are not described as accepted until the relevant service reports that state.

## Evidence boundary

Distribution copy should not claim that NiceTryGPT makes challenges AI-proof or universally LLM-resistant.

For v0.3.0, supported claims are limited to:

- three reproducible demonstration vulnerability classes;
- deterministic before/after regression checks;
- a documented Human Cost Gate;
- an explicit authorization boundary;
- completed GPT fresh-context evidence on Interstellar Ingress (5 BEFORE + 5 AFTER valid runs);
- resource-bounded GPT evidence on DiceMiner (10 BEFORE + 3 AFTER valid runs);
- transparent infrastructure-failure accounting and observed-vs-projected separation;
- no claim of universal LLM resistance or completed cross-model replication.

See [the evaluation protocol](../evals/protocol.md) and [related work](related-work.md).
