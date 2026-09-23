#!/usr/bin/env python3
"""Validate NiceTryGPT bundled challenge adapter metadata."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP_KEYS = {"schema_version", "id", "challenge_name", "report_path", "runtime", "verification"}
RUNTIME_KEYS = {"kind", "before_entrypoint", "after_entrypoint", "ready_path"}
VERIFY_KEYS = {"test_module", "before_test", "after_test"}


class AdapterError(ValueError):
    pass


def _exact_keys(obj: dict, expected: set[str], source: str) -> None:
    if not isinstance(obj, dict):
        raise AdapterError(f"{source}: expected object")
    extra = set(obj) - expected
    missing = expected - set(obj)
    if extra or missing:
        raise AdapterError(f"{source}: missing={sorted(missing)} extra={sorted(extra)}")


def _text(obj: dict, key: str, source: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise AdapterError(f"{source}.{key}: expected non-empty string")
    return value


def discover(root: Path = ROOT) -> list[Path]:
    return sorted((root / "adapters").glob("*.json"))


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location("nicetrygpt_adapter_tests", path)
    if spec is None or spec.loader is None:
        raise AdapterError(f"{path}: cannot import verification module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_adapter(data: dict, source: str = "<memory>", root: Path = ROOT) -> dict:
    _exact_keys(data, TOP_KEYS, source)
    if data["schema_version"] != "1.0":
        raise AdapterError(f"{source}.schema_version: expected 1.0")

    adapter_id = _text(data, "id", source)
    challenge_name = _text(data, "challenge_name", source)
    if adapter_id != challenge_name:
        raise AdapterError(f"{source}: id and challenge_name must match")

    report_path = root / _text(data, "report_path", source)
    if not report_path.is_file():
        raise AdapterError(f"{source}: report_path does not exist: {report_path}")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("challenge", {}).get("name") != challenge_name:
        raise AdapterError(f"{source}: report challenge name mismatch")
    if report.get("challenge", {}).get("source_type") != "bundled_demo":
        raise AdapterError(f"{source}: adapters are only for bundled_demo reports")

    runtime = data["runtime"]
    _exact_keys(runtime, RUNTIME_KEYS, f"{source}.runtime")
    if runtime["kind"] != "python_http":
        raise AdapterError(f"{source}.runtime.kind: expected python_http")
    for key in ("before_entrypoint", "after_entrypoint"):
        path = root / _text(runtime, key, f"{source}.runtime")
        if not path.is_file():
            raise AdapterError(f"{source}: missing runtime entrypoint {path}")
    ready = _text(runtime, "ready_path", f"{source}.runtime")
    if not ready.startswith("/"):
        raise AdapterError(f"{source}.runtime.ready_path: must start with /")

    verification = data["verification"]
    _exact_keys(verification, VERIFY_KEYS, f"{source}.verification")
    module_path = root / _text(verification, "test_module", f"{source}.verification")
    if not module_path.is_file():
        raise AdapterError(f"{source}: missing test module {module_path}")
    module = _load_module(module_path)
    for key in ("before_test", "after_test"):
        name = _text(verification, key, f"{source}.verification")
        if not callable(getattr(module, name, None)):
            raise AdapterError(f"{source}: missing callable {name} in {module_path}")

    return {"id": adapter_id, "report_path": str(report_path.relative_to(root))}


def validate_path(path: Path, root: Path = ROOT) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AdapterError(f"{path}: invalid JSON: {exc}") from exc
    return validate_adapter(data, str(path), root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = args.paths or discover()
    if not paths:
        raise SystemExit("no challenge adapters found")

    seen = set()
    for path in paths:
        result = validate_path(path)
        if result["id"] in seen:
            raise AdapterError(f"duplicate adapter id: {result['id']}")
        seen.add(result["id"])
        print(f"PASS  {result['id']}")

    print(f"\nValidated {len(paths)} challenge adapters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
