# NiceTryGPT report — mini-traversal

- Final status: `TRANSFORMED PASS`
- Baseline result: PASS
- Vulnerability class: Path traversal
- Learning objective: identify and exploit unsafe path joining to escape the public download directory
- Cheap shortcut: a static export path makes `../exports/latest.txt` an immediate one-shot candidate
- Transformation: runtime discovery
- Human cost: +1 meaningful request
- Original difficulty band: Easy
- Post-change difficulty band: Easy
- Shortcut reduction check: PASS
- Post-change E2E result: PASS
- Fresh-solver result: `NOT TESTED`
- Files changed: `after/server.py`

The baseline is valid because the runtime flag is read through the vulnerable download endpoint using path traversal.

In the transformed version, the old static traversal path fails. A normal activity response reveals the current export path, and the same traversal primitive then reaches the flag.

No honeypot, new exploit primitive, or brute force is introduced, so the added human cost is one ordinary observation.
