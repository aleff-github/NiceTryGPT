# Mini IDOR — after

This version keeps the same learning objective and difficulty band while removing the adjacent-ID shortcut.

Run:

```bash
CTF_FLAG='FLAG{local_demo}' python server.py --port 8000
```

On Windows PowerShell:

```powershell
$env:CTF_FLAG='FLAG{local_demo}'; python server.py --port 8000
```

The player still owns order `1001`.

The sensitive foreign order ID is generated at server startup, so it cannot be learned from a static adjacent-ID guess. The ID is exposed through normal `/api/activity` behavior and can then be used against the same vulnerable `/receipt` endpoint.

A safe `/download` endpoint provides one shallow semantic decoy. A normal download works; traversal is rejected cleanly.
