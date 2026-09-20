# NiceTryGPT report — mini-idor

- Final status: `TRANSFORMED PASS`
- Baseline result: PASS
- Vulnerability class: IDOR / missing object-level authorization
- Learning objective: identify and exploit a missing ownership check on an object reference
- Cheap shortcut: the sensitive object is the immediately adjacent numeric ID
- Transformation: runtime discovery + one semantic decoy
- Human cost: +1 meaningful request, with one optional failed decoy hypothesis
- Original difficulty band: Easy
- Post-change difficulty band: Easy
- Shortcut reduction check: PASS
- Post-change E2E result: PASS
- Fresh-solver result: `NOT TESTED`
- Files changed: `after/server.py`

The baseline is valid because the runtime flag is obtained through the vulnerable receipt endpoint rather than by reading source or fixtures.

The transformed server no longer rewards the adjacent-ID guess. A valid foreign order reference is instead exposed through ordinary application activity, after which the same missing ownership check yields the flag.

The shallow download decoy is optional to test and can be dismissed in one request, so it does not change the prerequisite knowledge or difficulty band.
