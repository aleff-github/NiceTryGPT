from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
import argparse
import os
import shutil
import tempfile

FLAG = os.environ.get("CTF_FLAG", "FLAG{local_demo}")
RUNTIME_ROOT = Path(tempfile.mkdtemp(prefix="nicetrygpt-traversal-before-"))
PUBLIC_DIR = RUNTIME_ROOT / "public"
EXPORTS_DIR = RUNTIME_ROOT / "exports"

PUBLIC_DIR.mkdir(parents=True)
EXPORTS_DIR.mkdir(parents=True)
(PUBLIC_DIR / "welcome.txt").write_text("Welcome to TinyFiles.\n", encoding="utf-8")
(EXPORTS_DIR / "latest.txt").write_text(FLAG + "\n", encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            return self.send_text(
                200,
                "TinyFiles\n"
                "Public download: /download?file=welcome.txt\n"
                "Latest export: exports/latest.txt\n",
            )

        if parsed.path == "/download":
            name = unquote(parse_qs(parsed.query).get("file", [""])[0])
            # Intentional CTF vulnerability: user input is joined without a
            # containment check, so ../ can escape PUBLIC_DIR.
            target = PUBLIC_DIR / name
            if not target.is_file():
                return self.send_text(404, "file not found\n")
            return self.send_text(200, target.read_text(encoding="utf-8"))

        return self.send_text(404, "not found\n")

    def send_text(self, status, body):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    try:
        ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
    finally:
        shutil.rmtree(RUNTIME_ROOT, ignore_errors=True)


if __name__ == "__main__":
    main()
