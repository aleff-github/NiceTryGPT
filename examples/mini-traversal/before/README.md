# Mini Path Traversal — before

This is the intentionally shortcut-friendly baseline.

Run:

```bash
CTF_FLAG='FLAG{local_demo}' python server.py --port 8000
```

On Windows PowerShell:

```powershell
$env:CTF_FLAG='FLAG{local_demo}'; python server.py --port 8000
```

The application serves public files from `/download?file=...`.

Learning objective: identify and exploit a path traversal caused by joining user-controlled input to the public-files directory without containment checks.

The cheap shortcut is intentional: the home page exposes the static export path `exports/latest.txt`, so `../exports/latest.txt` is an immediate traversal candidate.
