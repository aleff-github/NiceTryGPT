#!/usr/bin/env python3
"""Execute bundled demo before/after checks through challenge adapters."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from validate_challenge_adapters import ROOT, discover, validate_path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("nicetrygpt_demo_tests", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    paths = discover()
    if not paths:
        raise SystemExit("no challenge adapters found")

    modules = {}
    for path in paths:
        validate_path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        module_path = ROOT / data["verification"]["test_module"]
        if module_path not in modules:
            modules[module_path] = load_module(module_path)
        module = modules[module_path]
        for phase in ("before", "after"):
            test_name = data["verification"][f"{phase}_test"]
            getattr(module, test_name)()
            print(f"PASS  {data['id']} {phase}")

    print(f"\nAdapter E2E: PASS ({len(paths)} bundled demos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
