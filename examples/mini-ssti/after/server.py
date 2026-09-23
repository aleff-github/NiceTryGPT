#!/usr/bin/env python3
import argparse
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

FLAG = os.environ.get("CTF_FLAG", "FLAG{demo}")
TOKEN = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")
DRAFTS = {}
NEXT_ID = 1


def render(template: str) -> str:
    context = {"name": "guest", "flag": FLAG}
    return TOKEN.sub(lambda m: context.get(m.group(1), ""), template)


class Handler(BaseHTTPRequestHandler):
    def send_text(self, status: int, body: str):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        global NEXT_ID
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_text(200, "TinyTemplate\nCreate a draft with /draft?template=Hello%20{{name}}, then preview it.\n")
            return
        if parsed.path == "/draft":
            template = parse_qs(parsed.query).get("template", [""])[0]
            if not template:
                self.send_text(400, "missing template")
                return
            draft_id = f"d{NEXT_ID}"
            NEXT_ID += 1
            DRAFTS[draft_id] = template
            self.send_text(200, f"draft={draft_id}\npreview=/preview?id={draft_id}")
            return
        if parsed.path == "/preview":
            params = parse_qs(parsed.query)
            if "template" in params:
                self.send_text(400, "preview requires stored draft")
                return
            draft_id = params.get("id", [""])[0]
            template = DRAFTS.get(draft_id)
            if template is None:
                self.send_text(404, "unknown draft")
                return
            self.send_text(200, render(template))
            return
        self.send_text(404, "not found")

    def log_message(self, *_):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
