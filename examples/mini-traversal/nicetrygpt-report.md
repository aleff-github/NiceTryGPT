# NiceTryGPT report — mini-traversal

- Final status: `TRANSFORMED PASS`
- Baseline result: PASS
- Vulnerability class: Path traversal
- Cheap shortcut: a static export path makes `../exports/latest.txt` an immediate one-shot candidate
- Transformation: runtime discovery
- Human cost: +1 meaningful request
- Original difficulty band: Easy
- Post-change difficulty band: Easy
- Post-change E2E result: PASS
- Fresh-solver result: NOT TESTED
- Files changed: `after/server.py`

The vulnerable download logic is intentionally unchanged.

In the baseline, the application exposes a fixed export filename. In the transformed version, the export filename is generated at startup and is revealed through normal `/api/activity` behavior. The old static traversal path therefore fails, while the player can still discover the current export path and exploit the same traversal with one additional request.

No honeypot or decoy is used in this example.
