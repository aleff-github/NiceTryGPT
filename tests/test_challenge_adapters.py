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
    "validate_challenge_adapters",
    ROOT / "scripts" / "validate_challenge_adapters.py",
)


class ChallengeAdapterTests(unittest.TestCase):
    def test_every_bundled_demo_has_one_adapter(self):
        demos = sorted(path.name for path in (ROOT / "examples").iterdir() if path.is_dir())
        adapters = sorted(path.stem for path in validator.discover(ROOT))
        self.assertEqual(adapters, demos)

    def test_all_adapters_validate(self):
        for path in validator.discover(ROOT):
            with self.subTest(path=path):
                validator.validate_path(path, ROOT)

    def test_adapter_must_point_to_matching_report(self):
        path = ROOT / "adapters" / "mini-idor.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        bad = copy.deepcopy(data)
        bad["challenge_name"] = "wrong-name"
        with self.assertRaises(validator.AdapterError):
            validator.validate_adapter(bad, root=ROOT)

    def test_adapter_rejects_missing_entrypoint(self):
        path = ROOT / "adapters" / "mini-sqli.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        bad = copy.deepcopy(data)
        bad["runtime"]["after_entrypoint"] = "examples/does-not-exist/server.py"
        with self.assertRaises(validator.AdapterError):
            validator.validate_adapter(bad, root=ROOT)


if __name__ == "__main__":
    unittest.main()
