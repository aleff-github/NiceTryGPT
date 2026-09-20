# Mini Path Traversal — after

This version keeps the same path traversal and the same difficulty band while removing the static export-path shortcut.

Run:

```bash
CTF_FLAG='FLAG{local_demo}' python server.py --port 8000
```

On Windows PowerShell:

```powershell
$env:CTF_FLAG='FLAG{local_demo}'; python server.py --port 8000
```

The public download endpoint is unchanged and remains intentionally vulnerable.

The export filename is generated when the server starts. A normal `/api/activity` response exposes the current export path, so the player needs one runtime observation before applying the same traversal technique.

There is no decoy in this example.
