# Related work and positioning

NiceTryGPT sits between two areas of current work:

1. benchmarks and agents that measure or improve **LLM CTF-solving capability**;
2. guidance and research on **CTF design in the presence of capable LLMs**.

It is not intended to replace either.

## Nearby work

### Cybench

Cybench evaluates language-model agents on 40 professional-level CTF tasks and provides a framework for measuring cybersecurity capability.

- Project: https://cybench.github.io/
- ICLR 2025 paper: https://proceedings.iclr.cc/paper_files/paper/2025/hash/3e9412a9c1d93810ef3ef7825115016b-Abstract-Conference.html

**Different question:** Cybench asks how well an agent can solve cybersecurity tasks. NiceTryGPT asks how an existing challenge can be minimally transformed after a verified baseline solve.

### CTFTiny / CTFJudge

The AAAI 2026 work *Towards Effective Offensive Security LLM Agents* introduces CTFTiny, a 50-challenge benchmark, CTFJudge, and the CTF Competency Index for analyzing agent performance.

- Paper: https://doi.org/10.1609/aaai.v40i35.40210

**Different question:** this work focuses on evaluating and improving offensive-security agents. NiceTryGPT focuses on challenge transformation while bounding human cost.

### CTFAgent

CTFAgent explores an LLM-powered plan-and-execute agent for solving CTF challenges across categories.

- DOI: https://doi.org/10.1016/j.jisa.2025.104305

**Different question:** CTFAgent is a solver. NiceTryGPT is not.

### Adversarial CTF design in practice

A 2026 SecureCircuit write-up describes real CTF design choices intended to reduce trivial LLM-assisted solving, including state-dependent systems, large artifacts, reverse engineering, and empirical validation.

- Article: https://www.securecircuit.fyi/blog/how-we-built-a-reliable-ctf-platform-and-designed-challenges-to-resist-llms/

This is especially relevant because it shows that LLM-aware challenge design is already a real organizer concern.

NiceTryGPT intentionally rejects some heavy-handed approaches—such as making artifacts large merely to exceed model input limits—when they increase friction without improving the human learning objective.

### Fair CTFs in the age of AI

The 2026 preprint *The Disruptive Impact of Large Language Models on Capture the Flag Competitions and the Path Toward Fair Play* discusses LLM-resistant challenge design as one component of a broader competition safeguard framework.

- Preprint: https://arxiv.org/abs/2607.25425

NiceTryGPT targets only the challenge-design component. It is not an anti-cheat system and does not attempt to decide whether AI should be allowed in a competition.

### AI-centered cybersecurity education

The 2026 preprint *AI In Cybersecurity Education — Scalable Agentic CTF Design Principles and Educational Outcomes* studies autonomy levels, traceable agent workflows, and learning-focused CTF design.

- Preprint: https://arxiv.org/abs/2603.21551

This reinforces the importance of separating competition goals, learning outcomes, and agent capability measurements.

### CTFusion and contamination-aware evaluation

The 2026 work *CTFusion: A CTF-based Benchmark for LLM Agent Evaluation* argues
that static CTF benchmarks built from already published challenges are exposed
to training-data contamination and retrieval of known solutions. It evaluates
agents on live CTF events to reduce those threats.

- Paper: https://arxiv.org/abs/2605.11504
- Repository: https://github.com/kaist-hacking/CTFusion

**Different question:** CTFusion improves capability measurement by changing
where benchmark tasks come from. NiceTryGPT transforms an existing challenge
while preserving its learning objective. For NiceTryGPT evaluations on public
archived CTFs, contamination remains a stated limitation; adding more runs on
the same public tasks does not remove it.

This is one reason v0.4 prioritizes auditable evidence contracts over simply
increasing inference volume.

## NiceTryGPT's narrow position

A useful description is:

> **A minimal-diff transformation workflow for existing CTFs: solve first, identify one cheap LLM shortcut, make the smallest human-friendly change, then solve again.**

The differentiating emphasis is the combination of:

- an existing challenge as input;
- mandatory baseline reproduction;
- preservation of vulnerability class and learning objective;
- an explicit Human Cost Gate;
- minimal changes rather than redesign from scratch;
- post-change end-to-end verification;
- honest separation between deterministic regression tests and independent LLM evaluation.

This should be treated as a project hypothesis and engineering methodology, not as a claim of academic novelty until a more systematic literature review and evaluation are completed.

## What NiceTryGPT is not

NiceTryGPT is not:

- a CTF-solving agent;
- a cybersecurity benchmark;
- an automatic challenge generator;
- an AI detector;
- an anti-cheat platform;
- a claim that human reasoning can be cleanly separated from machine reasoning;
- proof that a challenge is “AI-proof.”

Keeping these boundaries explicit makes the project easier to understand and evaluate.
