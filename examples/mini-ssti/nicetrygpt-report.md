# NiceTryGPT report — mini-ssti

- Final status: TRANSFORMED PASS
- Baseline result: PASS
- Vulnerability class: Server-side template injection against a restricted template context
- Learning objective: identify that attacker-controlled template expressions are evaluated against server-side context
- Cheap shortcut: a stateless preview endpoint accepts the complete winning template expression in one request with no application state
- Transformation: require one normal draft-creation action before previewing the same attacker-controlled template
- Human cost: +1 required meaningful action
- Original difficulty band: Easy
- Post-change difficulty band: Easy
- Shortcut reduction check: PASS — the old stateless preview request fails while a stored draft containing the same template expression reaches the flag
- Post-change E2E result: PASS
- Fresh-solver result: NOT TESTED
- Files changed: after/server.py
