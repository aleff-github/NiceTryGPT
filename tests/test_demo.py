from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.parse import quote
import contextlib
import json
import os
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
FLAG = "FLAG{nice_try_gpt_runtime_demo}"


def free_port():
    with contextlib.closing(socket.socket()) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_ready(port, timeout=5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urlopen(f"http://127.0.0.1:{port}/", timeout=0.3) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(0.05)
    raise RuntimeError(f"server on port {port} did not become ready")


@contextlib.contextmanager
def run_server(relative_dir):
    port = free_port()
    server = ROOT / relative_dir / "server.py"
    env = os.environ.copy()
    env["CTF_FLAG"] = FLAG

    process = subprocess.Popen(
        [sys.executable, str(server), "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    try:
        wait_ready(port)
        yield f"http://127.0.0.1:{port}"
    finally:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=2)


def get(url):
    try:
        with urlopen(url, timeout=2) as response:
            return response.status, response.read().decode()
    except HTTPError as exc:
        return exc.code, exc.read().decode()


def test_idor_before():
    with run_server("examples/mini-idor/before") as base:
        status, home = get(base + "/")
        assert status == 200
        assert "order=1001" in home
        assert FLAG not in home

        status, own_receipt = get(base + "/receipt?order=1001")
        assert status == 200
        assert "owner=guest" in own_receipt
        assert FLAG not in own_receipt

        status, receipt = get(base + "/receipt?order=1002")
        assert status == 200
        assert FLAG in receipt


def test_idor_after():
    with run_server("examples/mini-idor/after") as base:
        status, home = get(base + "/")
        assert status == 200
        assert "/api/activity" in home
        assert FLAG not in home

        status, own_receipt = get(base + "/receipt?order=1001")
        assert status == 200
        assert "owner=guest" in own_receipt
        assert FLAG not in own_receipt

        status, guessed = get(base + "/receipt?order=1002")
        assert status == 404
        assert FLAG not in guessed

        status, activity = get(base + "/api/activity")
        assert status == 200
        assert FLAG not in activity
        foreign = json.loads(activity)["recent_orders"][-1]
        assert foreign not in {"1001", "1002"}

        status, receipt = get(base + f"/receipt?order={foreign}")
        assert status == 200
        assert FLAG in receipt

        status, body = get(base + "/download?file=welcome.txt")
        assert status == 200
        assert "Welcome to MiniShop" in body
        assert FLAG not in body

        status, body = get(base + "/download?file=../secret/flag.txt")
        assert status == 400
        assert "invalid public file" in body
        assert FLAG not in body


def test_traversal_before():
    with run_server("examples/mini-traversal/before") as base:
        status, home = get(base + "/")
        assert status == 200
        assert "exports/latest.txt" in home
        assert FLAG not in home

        status, public = get(base + "/download?file=welcome.txt")
        assert status == 200
        assert "Welcome to TinyFiles" in public
        assert FLAG not in public

        shortcut = quote("../exports/latest.txt", safe="/.")
        status, exported = get(base + f"/download?file={shortcut}")
        assert status == 200
        assert FLAG in exported


def test_traversal_after():
    first_runtime_path = None

    with run_server("examples/mini-traversal/after") as base:
        status, home = get(base + "/")
        assert status == 200
        assert "/api/activity" in home
        assert "exports/latest.txt" not in home
        assert FLAG not in home

        status, public = get(base + "/download?file=welcome.txt")
        assert status == 200
        assert "Welcome to TinyFiles" in public
        assert FLAG not in public

        old_shortcut = quote("../exports/latest.txt", safe="/.")
        status, old = get(base + f"/download?file={old_shortcut}")
        assert status == 404
        assert FLAG not in old

        status, activity = get(base + "/api/activity")
        assert status == 200
        assert FLAG not in activity
        first_runtime_path = json.loads(activity)["latest_export"]
        assert first_runtime_path.startswith("exports/report-")
        assert first_runtime_path.endswith(".txt")

        traversal = quote("../" + first_runtime_path, safe="/.")
        status, exported = get(base + f"/download?file={traversal}")
        assert status == 200
        assert FLAG in exported

    # A fresh challenge instance should not reuse the same static export filename.
    with run_server("examples/mini-traversal/after") as base:
        status, activity = get(base + "/api/activity")
        assert status == 200
        second_runtime_path = json.loads(activity)["latest_export"]
        assert second_runtime_path != first_runtime_path


def test_skill_metadata():
    skill = (ROOT / "nice-try-gpt" / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\n")

    frontmatter = skill.split("---", 2)[1]
    fields = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()

    name = fields["name"]
    description = fields["description"]

    assert name == "nice-try-gpt"
    assert 1 <= len(name) <= 64
    assert description
    assert len(description) <= 1024
    assert all(c.islower() or c.isdigit() or c == "-" for c in name)
    assert "<" not in name and ">" not in name
    assert "<" not in description and ">" not in description


def main():
    tests = [
        ("skill metadata", test_skill_metadata),
        ("IDOR before", test_idor_before),
        ("IDOR after", test_idor_after),
        ("traversal before", test_traversal_before),
        ("traversal after", test_traversal_after),
    ]
    failed = 0

    for name, fn in tests:
        try:
            fn()
            print(f"PASS  {name}")
        except Exception as exc:
            failed += 1
            print(f"FAIL  {name}: {exc}")

    if failed:
        raise SystemExit(1)

    print("\nNiceTryGPT demo E2E: PASS")


if __name__ == "__main__":
    main()
