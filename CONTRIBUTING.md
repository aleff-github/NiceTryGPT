# Contributing to NiceTryGPT

NiceTryGPT is intentionally small. Contributions should preserve that property.

## Before opening a pull request

1. Keep the change focused.
2. Preserve the principle: **increase uncertainty, not complexity**.
3. Do not add anti-LLM tricks that materially worsen the human player experience.
4. Avoid new dependencies unless they solve a demonstrated problem.
5. Run:

```bash
python tests/test_demo.py
python tests/test_release.py
```

6. If you add or change a resistance pattern, explain:
   - which cheap shortcut it targets;
   - the expected additional human actions;
   - why an existing pattern is insufficient.

## Adding an example

Every challenge under `examples/` must include:

```text
example-name/
├── before/
│   ├── README.md
│   └── server.py
├── after/
│   ├── README.md
│   └── server.py
└── nicetrygpt-report.md
```

Use [`examples/REPORT_TEMPLATE.md`](examples/REPORT_TEMPLATE.md) for the report.

The CI checks that each example records the same acceptance evidence: baseline, learning objective, cheap shortcut, transformation, human cost, shortcut reduction, post-change E2E result, and fresh-solver status.

## What a good change looks like

Good contributions include:

- clearer skill instructions;
- small, reproducible CTF examples;
- tests that prove both functionality and shortcut reduction;
- evidence that a transformation preserves the human difficulty band;
- documentation fixes.

Avoid:

- large frameworks or unnecessary dependencies;
- dashboards, databases, or services without a demonstrated need;
- CAPTCHA, brute force, token flooding, pointless encoding, or frustrating decoys;
- changes that turn a simple challenge into an artificial multi-stage chain;
- claims of “AI-proof” or “LLM-resistant” based only on self-review.

## Claude Code plugin mirror

The canonical standalone skill under `nice-try-gpt/` is mirrored under `skills/nice-try-gpt/` so the repository can also load as a Claude Code plugin.

After changing the skill or its bundled references, run:

```bash
python scripts/sync_plugin_skill.py
```

Do not edit only one copy. CI requires the two trees to be byte-for-byte identical.

## Project metadata

If a release changes `VERSION`, keep the matching release metadata synchronized. The release checks validate `CITATION.cff`, `codemeta.json`, the website, and `docs/llms.txt` against the current version and dated changelog entry.

Do not add personal contact details to metadata unless the person has explicitly published them for that purpose.

## Issues and pull requests

Use the structured bug form for reproducible unintended behavior, the method-proposal form for new examples or methodology changes, and the CTF-author form for design feedback. Security-sensitive reports belong under the repository security policy.

Prefer a small PR with one clear purpose. The E2E workflow should be green before merge.

## Maintainer

Project decisions are maintained by [@aleff-github](https://github.com/aleff-github).
