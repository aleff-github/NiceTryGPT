from pathlib import Path
from zipfile import ZipFile
import csv
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
EXPECTED_EVAL_HEADER = [
    "date_utc",
    "model_family",
    "model_version",
    "challenge",
    "variant",
    "run_id",
    "success",
    "time_seconds",
    "meaningful_actions",
    "flag_obtained",
    "original_shortcut_attempted",
    "stop_reason",
    "notes",
]


def test_package():
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / f"nice-try-gpt-v{VERSION}.zip"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "package_skill.py"), "--output", str(output)],
            check=True,
            capture_output=True,
            text=True,
        )

        assert output.is_file()
        with ZipFile(output) as archive:
            names = sorted(archive.namelist())

        assert "nice-try-gpt/SKILL.md" in names
        assert "nice-try-gpt/references/resistance-patterns.md" in names
        assert all(name.startswith("nice-try-gpt/") for name in names)
        assert not any("__pycache__" in name or name.endswith(".pyc") for name in names)


def test_eval_schema():
    results = ROOT / "evals" / "results.csv"
    with results.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    assert header == EXPECTED_EVAL_HEADER

    completed = subprocess.run(
        [sys.executable, str(ROOT / "evals" / "summarize.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "No evaluation results recorded yet." in completed.stdout


def test_release_docs():
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    notes = (ROOT / ".github" / "release-notes" / "v0.1.0.md").read_text(encoding="utf-8")
    assert f"## [{VERSION}]" in changelog
    assert f"NiceTryGPT v{VERSION}" in notes


def main():
    tests = [
        ("release package", test_package),
        ("evaluation schema", test_eval_schema),
        ("release docs", test_release_docs),
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

    print("\nNiceTryGPT release checks: PASS")


if __name__ == "__main__":
    main()
