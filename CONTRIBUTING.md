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
```

6. If you add or change a resistance pattern, explain:
   - which cheap shortcut it targets;
   - the expected additional human actions;
   - why an existing pattern is insufficient.

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

## Pull requests

Prefer a small PR with one clear purpose. The E2E workflow should be green before merge.

## Maintainer

Project decisions are maintained by [@aleff-github](https://github.com/aleff-github).
