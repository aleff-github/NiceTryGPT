from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen
import contextlib
import json
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
FLAG = "FLAG{nice_try_gpt_demo}"


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
    process = subprocess.Popen(
        [sys.executable, str(server), "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
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


def test_before():
    with run_server("examples/mini-idor/before") as base:
        status, home = get(base + "/")
        assert status == 200 and "order=1001" in home

        # Baseline shortcut: try the adjacent object id.
        status, receipt = get(base + "/receipt?order=1002")
        assert status == 200 and FLAG in receipt


def test_after():
    with run_server("examples/mini-idor/after") as base:
        status, home = get(base + "/")
        assert status == 200 and "/api/activity" in home

        # Runtime discovery: obtain the foreign object reference from normal app behavior.
        status, activity = get(base + "/api/activity")
        assert status == 200
        foreign = json.loads(activity)["recent_orders"][-1]

        # Same vulnerability class: receipt endpoint still lacks an ownership check.
        status, receipt = get(base + f"/receipt?order={foreign}")
        assert status == 200 and FLAG in receipt

        # Semantic decoy is safe and cheap to dismiss.
        status, body = get(base + "/download?file=../secret/flag.txt")
        assert status == 400 and "invalid public file" in body


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
    assert len(name) <= 64
    assert len(description) <= 1024
    assert all(c.islower() or c.isdigit() or c == "-" for c in name)


def main():
    tests = [
        ("skill metadata", test_skill_metadata),
        ("before baseline", test_before),
        ("after transformed", test_after),
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
