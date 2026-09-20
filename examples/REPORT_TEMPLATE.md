# NiceTryGPT report template

Use this structure for every challenge example.

- Final status: `TRANSFORMED PASS`, `TRANSFORMED FAILED`, `BASELINE FAILED`, or `NO CHANGE NEEDED`
- Baseline result: PASS / FAIL
- Vulnerability class: concise class name
- Learning objective: one sentence
- Cheap shortcut: the specific shortcut identified from the baseline
- Transformation: primary resistance pattern, plus a second only if justified
- Human cost: additional meaningful actions
- Original difficulty band: e.g. Easy / Medium / Hard
- Post-change difficulty band: same scale
- Shortcut reduction check: PASS / FAIL / NOT APPLICABLE
- Post-change E2E result: PASS / FAIL / NOT APPLICABLE
- Fresh-solver result: result or `NOT TESTED`
- Files changed: transformation files only

Then add a short explanation covering:

1. why the original solve was valid;
2. how the shortcut was reduced;
3. why the intended vulnerability still works;
4. why the added human cost is acceptable.

Do not turn the report into a full write-up. It exists to make the transformation auditable.
