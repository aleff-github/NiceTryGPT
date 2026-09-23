#!/usr/bin/env python3
"""Run the complete offline NiceTryGPT research-artifact verification suite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("demo E2E", [sys.executable, "tests/test_demo.py"]),
    ("release contract", [sys.executable, "tests/test_release.py"]),
    ("Codex Interstellar harness", [sys.executable, "tests/test_codex_eval_runner.py"]),
    ("DiceMiner harness", [sys.executable, "tests/test_diceminer_eval_runner.py"]),
    ("evidence analysis", [sys.executable, "tests/test_evidence_analysis.py"]),
    ("Claude harness", [sys.executable, "tests/test_claude_interstellar_runner.py"]),
    ("transformation artifacts", [sys.executable, "tests/test_transformation_artifacts.py"]),
    ("Software Heritage archival helper", [sys.executable, "tests/test_swh_archive.py"]),
    (
        "machine-readable transformation reports",
        [sys.executable, "scripts/validate_transformation_reports.py"],
    ),
    (
        "evaluation contract",
        [sys.executable, "evals/analyze_evidence.py", "--validate-only"],
    ),
]


def main() -> int:
    for label, command in CHECKS:
        print(f"\n== {label} ==")
        subprocess.run(command, cwd=ROOT, check=True)

    print("\nNiceTryGPT research artifact: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
