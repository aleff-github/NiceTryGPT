# Structural generalization status

This snapshot is generated from committed NiceTryGPT transformation reports and bundled challenge adapters.

> This is **structural coverage**, not proof of universal LLM resistance, human-subject validation, or cross-model generalization.

## Summary

- Validated transformations: **7**
- Bundled deterministic demos: **5**
- Independently authored external transformations: **2**
- Distinct recorded vulnerability classes: **7**
- Resistance patterns represented: **5/5**
- Bundled demos with executable adapters: **5/5**
- Reports with valid fresh-solver observations: **2/7**

## Transformation matrix

| Challenge | Source | Vulnerability class | Pattern(s) | Required added actions | Deterministic | Fresh solver |
|---|---|---|---|---:|---|---|
| DiceMiner | external | IEEE-754 coordinate aliasing / reward-accounting inconsistency | runtime_discovery | 1 | yes | OBSERVED |
| Interstellar Ingress | external | JWT/session authentication bypass via unsecured token verification | runtime_discovery | 1 | yes | OBSERVED |
| mini-command-injection | bundled_demo | Command injection in a restricted toy-shell wrapper | pattern_break | 0 | yes | NOT_TESTED |
| mini-idor | bundled_demo | IDOR / missing object-level authorization | runtime_discovery, semantic_decoy | 1 | yes | NOT_TESTED |
| mini-sqli | bundled_demo | SQL injection | context_split | 2 | yes | NOT_TESTED |
| mini-ssti | bundled_demo | Server-side template injection against a restricted template context | state_dependency | 1 | yes | NOT_TESTED |
| mini-traversal | bundled_demo | Path traversal | runtime_discovery | 1 | yes | NOT_TESTED |

## Pattern coverage

- **pattern_break**: mini-command-injection
- **runtime_discovery**: DiceMiner, Interstellar Ingress, mini-idor, mini-traversal
- **context_split**: mini-sqli
- **state_dependency**: mini-ssti
- **semantic_decoy**: mini-idor

## Interpretation

The matrix tests whether the same preservation contract can be represented and deterministically checked across multiple vulnerability classes and resistance patterns. It does not estimate a population-level success rate.

Only reports marked OBSERVED contain valid fresh-solver evidence. NOT_TESTED bundled demos contribute deterministic transformation evidence only. Human difficulty remains a bounded structural criterion rather than an empirically measured human-subject outcome.
