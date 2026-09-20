from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import argparse
import os

FLAG = os.environ.get("CTF_FLAG", "FLAG{local_demo}")
ORDERS = {
    "1001": ("guest", "Coffee beans — €9"),
    "1002": ("admin", FLAG),
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            return self.send_text(
                200,
                "MiniShop\nLogged in as: guest\nYour receipt: /receipt?order=1001\n",
            )

        if parsed.path == "/receipt":
            order_id = parse_qs(parsed.query).get("order", [""])[0]
            order = ORDERS.get(order_id)
            if not order:
                return self.send_text(404, "receipt not found\n")
            owner, body = order
            # Intentional CTF vulnerability: no ownership check.
            return self.send_text(200, f"owner={owner}\nreceipt={body}\n")

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
