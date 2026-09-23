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


evidence = load_module(
    "analyze_evidence",
    ROOT / "evals" / "analyze_evidence.py",
)


class EvidenceAnalysisTests(unittest.TestCase):
    def test_wilson_zero_of_three_is_wide(self):
        low, high = evidence.wilson(0, 3)
        self.assertAlmostEqual(low, 0.0, places=6)
        self.assertGreater(high, 0.50)
        self.assertLess(high, 0.60)

    def test_report_separates_projection_from_observations(self):
        rows = []
        for i in range(10):
            rows.append({
                "model_family": "GPT",
                "model_version": "gpt-5.5 (low)",
                "challenge": "DiceMiner",
                "variant": "before",
                "run_id": f"b{i}",
                "success": "0",
                "original_shortcut_attempted": "1" if i < 3 else "0",
                "stop_reason": "gave_up",
                "notes": "",
            })
        for i in range(3):
            rows.append({
                "model_family": "GPT",
                "model_version": "gpt-5.5 (low)",
                "challenge": "DiceMiner",
                "variant": "after",
                "run_id": f"a{i}",
                "success": "0",
                "original_shortcut_attempted": "0",
                "stop_reason": "gave_up",
                "notes": "",
            })
        report = evidence.build_report(rows)
        self.assertIn("3/10", report)
        self.assertIn("0/3", report)
        self.assertIn("approximately **0/10**", report)
        self.assertIn("not an experimental result", report)
        self.assertIn("never inserted into `results.csv`", report)


if __name__ == "__main__":
    unittest.main()
