#!/usr/bin/env python3
import argparse
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

FLAG = os.environ.get("CTF_FLAG", "FLAG{demo}")


def toy_shell(command: str) -> str:
    out = []
    for raw in command.split(";"):
        part = raw.strip()
        if part.startswith("ping "):
            out.append(f"PING {part[5:].strip()}: ok")
        elif part == "printenv CTF_FLAG":
            out.append(FLAG)
        elif part:
            out.append(f"unknown command: {part}")
    return "\n".join(out)


class Handler(BaseHTTPRequestHandler):
    def send_text(self, status: int, body: str):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_text(200, "TinyDiag\nTry /diagnostic?host=127.0.0.1\n")
            return
        if parsed.path == "/diagnostic":
            params = parse_qs(parsed.query)
            host = params.get("host", [""])[0]
            if not host:
                self.send_text(400, "missing host")
                return
            self.send_text(200, toy_shell(f"ping {host}"))
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
