from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


runner = load_module(
    "run_claude_interstellar",
    ROOT / "evals" / "run_claude_interstellar.py",
)


class ClaudeInterstellarRunnerTests(unittest.TestCase):
    def test_command_is_restricted_to_mcp_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "mcp.json"
            cmd = runner.claude_command(
                "/usr/bin/claude",
                "PROMPT",
                "claude-sonnet-4-6",
                "low",
                cfg,
            )
        joined = " ".join(cmd)
        self.assertIn("--strict-mcp-config", cmd)
        self.assertIn("--no-session-persistence", cmd)
        self.assertIn("--tools", cmd)
        self.assertIn("mcp__ctf_http__http_request", cmd)
        self.assertIn("mcp__ctf_http__base64url", cmd)
        self.assertIn("claude-sonnet-4-6", cmd)
        self.assertNotIn("Bash", joined)
        self.assertNotIn("WebFetch", joined)

    def test_usage_limit_is_infrastructure_error(self):
        self.assertEqual(
            runner.claude_infrastructure_error(
                '{"type":"error","message":"Usage limit reached"}',
                "",
            ),
            "claude_usage_limit",
        )

    def test_next_run_id_skips_existing_log_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            results = root / "results.csv"
            logs = root / "logs"
            logs.mkdir()
            (logs / "claude-interstellar-before-03").mkdir()
            results.write_text(
                "date_utc,model_family,model_version,challenge,variant,run_id,success,time_seconds,meaningful_actions,flag_obtained,original_shortcut_attempted,stop_reason,notes\n"
                "x,Claude,claude-sonnet-4-6 (low),Interstellar Ingress,before,claude-interstellar-before-02,0,1,1,0,0,gave_up,\n",
                encoding="utf-8",
            )
            self.assertEqual(
                runner.next_run_id(results, logs, "before"),
                "claude-interstellar-before-04",
            )


if __name__ == "__main__":
    unittest.main()
