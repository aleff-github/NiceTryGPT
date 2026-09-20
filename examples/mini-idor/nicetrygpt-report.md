# NiceTryGPT report — mini-idor

- Final status: `TRANSFORMED PASS`
- Baseline result: PASS
- Vulnerability class: IDOR / missing object-level authorization
- Cheap shortcut: the sensitive object is the immediately adjacent numeric ID
- Transformation: runtime discovery + one semantic decoy
- Human cost: +1 meaningful request, with one optional failed decoy hypothesis
- Original difficulty band: Easy
- Post-change difficulty band: Easy
- Post-change E2E result: PASS
- Fresh-solver result: NOT TESTED
- Files changed: `after/server.py`

The vulnerability and learning objective are unchanged.

The foreign order ID is generated when the transformed server starts and is exposed through ordinary application activity. The player therefore has to observe runtime behavior before exploiting the same missing ownership check. The old adjacent-ID guess is explicitly tested and no longer succeeds.

The download decoy is shallow: its normal path works and a traversal probe is rejected in one request.
