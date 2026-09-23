#!/usr/bin/env python3
"""Generate the structural generalization snapshot from committed transformation reports."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ["pattern_break", "runtime_discovery", "context_split", "state_dependency", "semantic_decoy"]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module(
    "validate_transformation_reports_for_generalization",
    ROOT / "scripts" / "validate_transformation_reports.py",
)
adapter_validator = load_module(
    "validate_challenge_adapters_for_generalization",
    ROOT / "scripts" / "validate_challenge_adapters.py",
)


def collect(root: Path = ROOT) -> dict:
    reports = []
    for path in validator.discover(root):
        data = json.loads(path.read_text(encoding="utf-8"))
        validator.validate_report(data, str(path))
        reports.append((path, data))

    adapters = {}
    for path in adapter_validator.discover(root):
        result = adapter_validator.validate_path(path, root)
        adapters[result["id"]] = path

    bundled = [data for _, data in reports if data["challenge"]["source_type"] == "bundled_demo"]
    external = [data for _, data in reports if data["challenge"]["source_type"] == "external"]
    patterns = sorted({p for _, data in reports for p in data["transformation"]["patterns"]})
    vuln_classes = sorted({data["baseline"]["vulnerability_class"] for _, data in reports})
    observed = [data for _, data in reports if data["evidence"]["fresh_solver_status"] == "OBSERVED"]
    adapted = [data for data in bundled if data["challenge"]["name"] in adapters]

    return {
        "reports": reports,
        "bundled": bundled,
        "external": external,
        "patterns": patterns,
        "vuln_classes": vuln_classes,
        "observed": observed,
        "adapter_count": len(adapted),
        "adapter_total": len(bundled),
    }


def render(root: Path = ROOT) -> str:
    data = collect(root)
    lines = [
        "# Structural generalization status",
        "",
        "This snapshot is generated from committed NiceTryGPT transformation reports and bundled challenge adapters.",
        "",
        "> This is **structural coverage**, not proof of universal LLM resistance, human-subject validation, or cross-model generalization.",
        "",
        "## Summary",
        "",
        f"- Validated transformations: **{len(data['reports'])}**",
        f"- Bundled deterministic demos: **{len(data['bundled'])}**",
        f"- Independently authored external transformations: **{len(data['external'])}**",
        f"- Distinct recorded vulnerability classes: **{len(data['vuln_classes'])}**",
        f"- Resistance patterns represented: **{len(data['patterns'])}/{len(PATTERNS)}**",
        f"- Bundled demos with executable adapters: **{data['adapter_count']}/{data['adapter_total']}**",
        f"- Reports with valid fresh-solver observations: **{len(data['observed'])}/{len(data['reports'])}**",
        "",
        "## Transformation matrix",
        "",
        "| Challenge | Source | Vulnerability class | Pattern(s) | Required added actions | Deterministic | Fresh solver |",
        "|---|---|---|---|---:|---|---|",
    ]
    for path, report in sorted(data["reports"], key=lambda x: x[1]["challenge"]["name"].lower()):
        challenge = report["challenge"]
        patterns = ", ".join(report["transformation"]["patterns"]) or "none"
        lines.append(
            "| {name} | {source} | {vuln} | {patterns} | {actions} | {det} | {fresh} |".format(
                name=challenge["name"],
                source=challenge["source_type"],
                vuln=report["baseline"]["vulnerability_class"].replace("|", "\\|"),
                patterns=patterns,
                actions=report["human_cost"]["added_required_meaningful_actions"],
                det="yes" if report["evidence"]["deterministic_validation"] else "no",
                fresh=report["evidence"]["fresh_solver_status"],
            )
        )

    lines += ["", "## Pattern coverage", ""]
    for pattern in PATTERNS:
        users = sorted(
            report["challenge"]["name"]
            for _, report in data["reports"]
            if pattern in report["transformation"]["patterns"]
        )
        lines.append(f"- **{pattern}**: {', '.join(users) if users else 'not represented'}")

    lines += [
        "",
        "## Interpretation",
        "",
        "The matrix tests whether the same preservation contract can be represented and deterministically checked across multiple vulnerability classes and resistance patterns. It does not estimate a population-level success rate.",
        "",
        "Only reports marked OBSERVED contain valid fresh-solver evidence. NOT_TESTED bundled demos contribute deterministic transformation evidence only. Human difficulty remains a bounded structural criterion rather than an empirically measured human-subject outcome.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    print(render(), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
