from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import argparse
import os
import shutil
import sqlite3
import tempfile

FLAG = os.environ.get("CTF_FLAG", "FLAG{local_demo}")
RUNTIME_ROOT = tempfile.mkdtemp(prefix="nicetrygpt-sqli-after-")
DB_PATH = os.path.join(RUNTIME_ROOT, "users.db")


def initialize_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "CREATE TABLE users (email TEXT PRIMARY KEY, password TEXT, role TEXT, secret TEXT)"
        )
        db.executemany(
            "INSERT INTO users(email, password, role, secret) VALUES (?, ?, ?, ?)",
            [
                ("guest@tinysql.local", "guest", "guest", "Welcome, guest."),
                ("nightshift@staff.tinysql.local", "not-player-facing", "admin", FLAG),
            ],
        )


initialize_db()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            return self.send_text(
                200,
                "TinySQL Login\n"
                "Guest login: guest@tinysql.local / guest\n"
                "Team directory: /team\n"
                "Staff account help: /help\n"
                "Login: /login?email=...&password=...\n",
            )

        if parsed.path == "/team":
            return self.send_text(
                200,
                "Operations\n"
                "Administrator handle: nightshift\n",
            )

        if parsed.path == "/help":
            return self.send_text(
                200,
                "Staff email format: <handle>@staff.tinysql.local\n",
            )

        if parsed.path == "/login":
            params = parse_qs(parsed.query)
            email = params.get("email", [""])[0]
            password = params.get("password", [""])[0]

            # Intentional CTF vulnerability: unchanged from the baseline.
            query = (
                "SELECT email, role, secret FROM users "
                f"WHERE email = '{email}' AND password = '{password}'"
            )

            try:
                with sqlite3.connect(DB_PATH) as db:
                    row = db.execute(query).fetchone()
            except sqlite3.Error:
                return self.send_text(400, "login query failed\n")

            if not row:
                return self.send_text(401, "invalid credentials\n")

            user_email, role, secret = row
            return self.send_text(
                200,
                f"email={user_email}\nrole={role}\nmessage={secret}\n",
            )

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
