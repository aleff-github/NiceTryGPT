from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse
import argparse
import json
import os
import secrets

FLAG = os.environ.get("CTF_FLAG", "FLAG{local_demo}")
ADMIN_ORDER_ID = str(5000 + secrets.randbelow(5000))

ORDERS = {
    "1001": ("guest", "Coffee beans — €9"),
    ADMIN_ORDER_ID: ("admin", FLAG),
}
PUBLIC_FILES = {"welcome.txt": "Welcome to MiniShop.\n"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            return self.send_text(
                200,
                "MiniShop\n"
                "Logged in as: guest\n"
                "Your receipt: /receipt?order=1001\n"
                "Recent activity: /api/activity\n"
                "Download welcome file: /download?file=welcome.txt\n",
            )

        if parsed.path == "/api/activity":
            # The useful foreign reference is discoverable through ordinary runtime behavior.
            return self.send_text(
                200,
                json.dumps({"recent_orders": ["1001", ADMIN_ORDER_ID]}) + "\n",
            )

        if parsed.path == "/receipt":
            order_id = parse_qs(parsed.query).get("order", [""])[0]
            order = ORDERS.get(order_id)
            if not order:
                return self.send_text(404, "receipt not found\n")
            owner, body = order
            # Intentional CTF vulnerability: still no ownership check.
            return self.send_text(200, f"owner={owner}\nreceipt={body}\n")

        if parsed.path == "/download":
            name = unquote(parse_qs(parsed.query).get("file", [""])[0])
            # Deliberately safe decoy: one traversal probe is enough to reject it.
            if name not in PUBLIC_FILES or "/" in name or "\\" in name or ".." in name:
                return self.send_text(400, "invalid public file\n")
            return self.send_text(200, PUBLIC_FILES[name])

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
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
