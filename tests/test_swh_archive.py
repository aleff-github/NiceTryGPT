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


archive = load_module(
    "request_swh_archive",
    ROOT / "scripts" / "request_swh_archive.py",
)


class SoftwareHeritageArchiveTests(unittest.TestCase):
    def test_request_url_is_deterministic_and_encoded(self):
        url = archive.build_request_url("https://github.com/aleff-github/NiceTryGPT")
        self.assertEqual(
            url,
            "https://archive.softwareheritage.org/api/1/origin/save/"
            "?visit_type=git&origin_url=https%3A%2F%2Fgithub.com%2Faleff-github%2FNiceTryGPT",
        )

    def test_accepted_response_is_valid(self):
        status, task = archive.validate_response(
            {"save_request_status": "accepted", "save_task_status": "pending"}
        )
        self.assertEqual(status, "accepted")
        self.assertEqual(task, "pending")

    def test_pending_response_is_valid(self):
        status, _ = archive.validate_response(
            {"save_request_status": "pending", "save_task_status": None}
        )
        self.assertEqual(status, "pending")

    def test_failed_response_is_rejected(self):
        with self.assertRaises(archive.ArchiveRequestError):
            archive.validate_response(
                {"save_request_status": "rejected", "save_task_status": "failed"}
            )


if __name__ == "__main__":
    unittest.main()
