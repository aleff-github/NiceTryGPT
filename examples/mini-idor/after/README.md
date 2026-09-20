# Mini IDOR — after

Run:

```bash
python server.py --port 8000
```

The learning objective is unchanged: exploit an IDOR in the receipt endpoint.

The player still owns order `1001`, but the useful foreign object reference is learned through the normal `/api/activity` surface. A safe `/download` endpoint acts as a cheap semantic decoy and rejects traversal cleanly.
