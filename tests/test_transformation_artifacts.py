from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


validator = load_module(
    "validate_transformation_reports",
    ROOT / "scripts" / "validate_transformation_reports.py",
)


class TransformationArtifactTests(unittest.TestCase):
    def reports(self):
        return validator.discover(ROOT)

    def test_all_committed_reports_validate(self):
        reports = self.reports()
        self.assertGreaterEqual(len(reports), 5)
        for path in reports:
            with self.subTest(path=path):
                result = validator.validate_path(path)
                self.assertIn(result["status"], validator.ALLOWED_STATUSES)

    def test_every_bundled_demo_has_json_companion(self):
        for challenge in sorted((ROOT / "examples").iterdir()):
            if not challenge.is_dir():
                continue
            self.assertTrue(
                (challenge / "nicetrygpt-report.json").is_file(),
                f"{challenge.name}: missing machine-readable report",
            )

    def test_human_cost_gate_is_derived_not_self_asserted(self):
        path = ROOT / "examples" / "mini-traversal" / "nicetrygpt-report.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertNotIn("human_cost_gate_pass", data)
        result = validator.validate_report(data)
        self.assertEqual(result["human_cost_gate"], "PASS")

    def test_transformed_pass_rejects_excess_required_actions(self):
        path = ROOT / "examples" / "mini-traversal" / "nicetrygpt-report.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        bad = copy.deepcopy(data)
        bad["human_cost"]["added_required_meaningful_actions"] = 4
        with self.assertRaises(validator.ReportError):
            validator.validate_report(bad)

    def test_transformed_pass_rejects_new_exploit_primitive(self):
        path = ROOT / "examples" / "mini-sqli" / "nicetrygpt-report.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        bad = copy.deepcopy(data)
        bad["human_cost"]["new_exploit_primitive"] = True
        with self.assertRaises(validator.ReportError):
            validator.validate_report(bad)

    def test_observed_fresh_solver_requires_evaluation_reference(self):
        path = ROOT / "evals" / "transformations" / "interstellar-ingress.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        bad = copy.deepcopy(data)
        bad["evidence"]["evaluation_refs"] = []
        with self.assertRaises(validator.ReportError):
            validator.validate_report(bad)


if __name__ == "__main__":
    unittest.main()
