# Mini IDOR — before

This is the intentionally shortcut-friendly baseline.

Run:

```bash
CTF_FLAG='FLAG{local_demo}' python server.py --port 8000
```

On Windows PowerShell:

```powershell
$env:CTF_FLAG='FLAG{local_demo}'; python server.py --port 8000
```

The player starts at `/` as `guest` and owns order `1001`.

Learning objective: identify and exploit an IDOR / missing object-level authorization issue in the receipt endpoint.

The cheap shortcut is intentional: the sensitive order is the immediately adjacent ID.
