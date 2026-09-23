from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


analysis = load_module(
    "analyze_generalization",
    ROOT / "scripts" / "analyze_generalization.py",
)


class GeneralizationTests(unittest.TestCase):
    def test_snapshot_is_generated(self):
        generated = analysis.render(ROOT).rstrip()
        committed = (ROOT / "docs" / "generalization-status.md").read_text(encoding="utf-8").rstrip()
        self.assertEqual(generated, committed)

    def test_v05_structural_coverage_contract(self):
        data = analysis.collect(ROOT)
        self.assertGreaterEqual(len(data["reports"]), 7)
        self.assertGreaterEqual(len(data["bundled"]), 5)
        self.assertGreaterEqual(len(data["external"]), 2)
        self.assertEqual(set(data["patterns"]), set(analysis.PATTERNS))
        self.assertEqual(data["adapter_count"], data["adapter_total"])

    def test_solver_evidence_is_not_inferred_from_deterministic_demos(self):
        data = analysis.collect(ROOT)
        bundled = data["bundled"]
        self.assertTrue(all(r["evidence"]["fresh_solver_status"] == "NOT_TESTED" for r in bundled))
        self.assertEqual(len(data["observed"]), 2)


if __name__ == "__main__":
    unittest.main()
