# Mini SQL Injection — after

This version keeps the exact same SQL injection primitive and the same easy difficulty band, but removes the one-shot privileged-identity shortcut.

Run:

```bash
CTF_FLAG='FLAG{local_demo}' python server.py --port 8000
```

On Windows PowerShell:

```powershell
$env:CTF_FLAG='FLAG{local_demo}'; python server.py --port 8000
```

The login endpoint is still:

```text
/login?email=...&password=...
```

The privileged identity is no longer printed on the home page.

Instead, two ordinary static application surfaces provide:

- the administrator handle via `/team`;
- the staff email convention via `/help`.

The player connects those clues and then applies the same comment-based SQL injection as in the baseline.

There is no runtime randomization and no decoy in this example.
