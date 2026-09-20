# Interstellar Ingress transformation record

This document records the first NiceTryGPT transformation of an independently authored public CTF challenge.

It is **transformation evidence**, not fresh-solver or cross-model evidence.

## Upstream

- Challenge: **Interstellar Ingress**
- Event: NexusCTF 2025
- Repository: https://github.com/michaeldaltonau/sydney-university-nexusctf-2025-web-challenges
- Pinned commit: `ac450407fcdae9057a2063477e751a7b414a9cdd`
- License: MIT
- Verification date: 2026-09-20
- Organizer infrastructure contacted: **no**

## Status

```text
TRANSFORMED PASS
fresh_solver_tested: false
```

The baseline and transformed variants were both rebuilt and solved locally from clean state. Same-context transformation verification is intentionally not counted as fresh solver evidence.

## Baseline

The player-facing guest-login flow issues a JWT whose payload exposes a self-describing privilege claim:

```json
{"is_admin": false}
```

The intended weakness is an insecure verification fallback that accepts an unsecured JWT. A forged `alg:none` token with `is_admin: true` reaches the admin view and the runtime flag.

The concrete cheap shortcut is therefore not merely “knowing JWT”: one observed token reveals the claim name, type, and obvious winning value, so a canonical `alg:none` recipe can be replayed with essentially no challenge-specific discovery.

## Minimal transformation

NiceTryGPT applied one resistance move: **runtime discovery**.

The transformed challenge:

- changes the guest claim to `{"clearance": "transit-guest"}`;
- generates a per-process warden clearance in the form `wk-<random bytes>`;
- decides admin access by comparing the forged `clearance` value to that runtime value;
- exposes the accepted warden clearance on the normal player-facing login page.

The insecure JWT verification function is left unchanged. The intended vulnerability remains forging an unsigned `alg:none` token; the player must simply observe the runtime-specific value before forging it.

The transformation patch touched four source files and did not add a new exploit primitive, brute force, CAPTCHA, artificial chain, or unrelated refactor.

## Verification

The local clean-state verification established:

- BEFORE intended solve: **PASS**;
- AFTER intended solve: **PASS**;
- zero-observation shortcut against AFTER: **reduced**;
- ordinary guest/login/logout behavior: **preserved**;
- flag leakage through normal non-admin surfaces: **not observed**;
- runtime value changes across server restart: **PASS**.

The submitted verification also exercised a shortcut probe: the zero-observation recipe remained effective against BEFORE but failed across the AFTER probe attempts.

## Human Cost Gate

**PASS**

- vulnerability class: unchanged;
- learning objective: unchanged;
- prerequisite knowledge: unchanged;
- added meaningful actions: **+1 observation**;
- added HTTP requests: **0–1**;
- new exploit primitive: **none**.

The intended effect is to force challenge-specific observation, not to prevent an agent that reads the application from solving the challenge.

## Evidence boundary

This record does **not** establish that the transformed challenge is AI-proof, LLM-proof, statistically resistant, or harder for every model.

A fresh solver that receives only the player-facing prompt and local URL may still solve the transformed challenge quickly. That is compatible with the design goal: reduce a cheap zero-observation shortcut while preserving the intended human learning path.

Fresh-context model results belong in `results.csv` only after they are run under the fixed evaluation protocol with exact model/version identifiers recorded.
