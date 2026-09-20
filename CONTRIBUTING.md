# Contributing to NiceTryGPT

NiceTryGPT is intentionally small. Contributions should preserve that property.

## Before opening a pull request

1. Keep the proposed change focused.
2. Preserve the principle: **increase uncertainty, not complexity**.
3. Do not add anti-LLM tricks that materially worsen the human player experience.
4. Run:

```bash
python tests/test_demo.py
```

5. If you add a resistance pattern, explain the expected human cost and why an existing pattern is insufficient.

## Good contributions

- clearer skill instructions;
- small, reproducible CTF examples;
- tests that catch regressions;
- evidence that a transformation reduces cheap shortcuts without increasing the difficulty band;
- documentation fixes.

## Avoid

- large frameworks or unnecessary dependencies;
- dashboards, databases, or services without a demonstrated need;
- CAPTCHA, brute force, token flooding, pointless encoding, or intentionally frustrating decoys;
- changes that turn a simple challenge into a multi-stage exploit chain.

## Maintainer

Project decisions are maintained by [@aleff-github](https://github.com/aleff-github).
