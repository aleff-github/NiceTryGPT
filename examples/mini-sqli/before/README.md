# Mini SQL Injection — before

This is the intentionally shortcut-friendly baseline.

Run:

```bash
CTF_FLAG='FLAG{local_demo}' python server.py --port 8000
```

On Windows PowerShell:

```powershell
$env:CTF_FLAG='FLAG{local_demo}'; python server.py --port 8000
```

The application exposes a tiny login endpoint:

```text
/login?email=...&password=...
```

Learning objective: identify and exploit SQL injection in the login lookup to authenticate as the privileged user.

The cheap shortcut is intentional: the home page directly exposes the privileged email address, so the player can immediately use a comment-based SQL injection against that exact account.
