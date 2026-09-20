# Mini IDOR — before

Run:

```bash
python server.py --port 8000
```

Player starts at `/` as `guest` and owns order `1001`.

Learning objective: identify and exploit an IDOR in the receipt endpoint.
