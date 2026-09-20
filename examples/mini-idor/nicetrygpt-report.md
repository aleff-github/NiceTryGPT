# NiceTryGPT report — mini-idor

- Baseline: PASS
- Vulnerability class: IDOR / missing object-level authorization
- Cheap shortcut: the sensitive object is the immediately adjacent numeric ID
- Transformation: runtime discovery + one semantic decoy
- Human cost: +1 meaningful request; same difficulty band
- Post-change E2E: PASS
- Fresh-solver check: not run in this local demo
- Files changed: `after/server.py`

The intended vulnerability and learning objective are unchanged. The transformed version asks the player to observe normal application activity before exploiting the same missing ownership check. The download decoy is intentionally shallow and rejects traversal in one request.
