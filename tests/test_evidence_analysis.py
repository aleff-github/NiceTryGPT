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


def synthetic_manifest():
    return {
        "schema_version": "1.0",
        "studies": [{
            "id": "dice-test",
            "challenge": "DiceMiner",
            "model_family": "GPT",
            "model_version": "gpt-5.5 (low)",
            "protocol": "test",
            "target_valid_runs": {"before": 10, "after": 10},
            "collection_status": "resource_bounded_partial",
            "projection": {"enabled": True, "variant": "after"},
        }],
    }


def row(run_id, variant, shortcut="0", stop="gave_up", actions="1", notes=""):
    return {
        "date_utc": "2026-09-23T00:00:00+00:00",
        "model_family": "GPT",
        "model_version": "gpt-5.5 (low)",
        "challenge": "DiceMiner",
        "variant": variant,
        "run_id": run_id,
        "success": "0",
        "time_seconds": "1",
        "meaningful_actions": actions,
        "flag_obtained": "0",
        "original_shortcut_attempted": shortcut,
        "stop_reason": stop,
        "notes": notes,
    }


class EvidenceAnalysisTests(unittest.TestCase):
    def test_wilson_zero_of_three_is_wide(self):
        low, high = evidence.wilson(0, 3)
        self.assertAlmostEqual(low, 0.0, places=6)
        self.assertGreater(high, 0.50)
        self.assertLess(high, 0.60)

    def test_explicit_infrastructure_marker_controls_classification(self):
        infra = row(
            "infra", "before", stop="error", actions="0",
            notes="infrastructure_error=codex_usage_limit",
        )
        solver_error = row("solver-error", "before", stop="error", actions="12")
        self.assertEqual(
            evidence.classify_row(infra), "infrastructure_failure"
        )
        self.assertEqual(
            evidence.classify_row(solver_error), "solver_observation"
        )

    def test_zero_action_unclassified_error_is_rejected(self):
        rows = [row("bad", "before", stop="error", actions="0")]
        with self.assertRaises(evidence.EvidenceContractError):
            evidence.validate_rows(rows, synthetic_manifest())

    def test_report_separates_projection_from_observations(self):
        rows = []
        for i in range(10):
            rows.append(row(f"b{i}", "before", shortcut="1" if i < 3 else "0"))
        for i in range(3):
            rows.append(row(f"a{i}", "after", shortcut="0"))
        report = evidence.build_report(rows, synthetic_manifest())
        self.assertIn("3/10", report)
        self.assertIn("0/3", report)
        self.assertIn("approximately **0/10**", report)
        self.assertIn("not experimental results", report)
        self.assertIn("Projected values are never inserted", report)
        self.assertIn("Observed effect-size snapshot", report)
        self.assertIn("-30.0 pp", report)

    def test_duplicate_run_id_is_rejected(self):
        rows = [row("same", "before"), row("same", "after")]
        with self.assertRaises(evidence.EvidenceContractError):
            evidence.validate_rows(rows, synthetic_manifest())

    def test_valid_count_cannot_exceed_preregistered_target(self):
        manifest = synthetic_manifest()
        manifest["studies"][0]["target_valid_runs"]["after"] = 1
        rows = [row("a1", "after"), row("a2", "after")]
        with self.assertRaises(evidence.EvidenceContractError):
            evidence.validate_rows(rows, manifest)


if __name__ == "__main__":
    unittest.main()
