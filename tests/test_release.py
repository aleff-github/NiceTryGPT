from pathlib import Path
from zipfile import ZipFile
import csv
import json
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
EXPECTED_EVAL_HEADER = [
    "date_utc",
    "model_family",
    "model_version",
    "challenge",
    "variant",
    "run_id",
    "success",
    "time_seconds",
    "meaningful_actions",
    "flag_obtained",
    "original_shortcut_attempted",
    "stop_reason",
    "notes",
]
REQUIRED_REPORT_FIELDS = [
    "Final status",
    "Baseline result",
    "Vulnerability class",
    "Learning objective",
    "Cheap shortcut",
    "Transformation",
    "Human cost",
    "Original difficulty band",
    "Post-change difficulty band",
    "Shortcut reduction check",
    "Post-change E2E result",
    "Fresh-solver result",
    "Files changed",
]


def test_package():
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / f"nice-try-gpt-v{VERSION}.zip"
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "package_skill.py"), "--output", str(output)],
            check=True,
            capture_output=True,
            text=True,
        )

        assert output.is_file()
        with ZipFile(output) as archive:
            names = sorted(archive.namelist())

        assert "nice-try-gpt/SKILL.md" in names
        assert "nice-try-gpt/references/resistance-patterns.md" in names
        assert all(name.startswith("nice-try-gpt/") for name in names)
        assert not any("__pycache__" in name or name.endswith(".pyc") for name in names)


def test_claude_plugin():
    manifest_path = ROOT / ".claude-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["name"] == "nice-try-gpt"
    assert manifest["version"] == VERSION
    assert manifest["repository"] == "https://github.com/aleff-github/NiceTryGPT"
    assert manifest["license"] == "GPL-3.0-only"
    assert manifest["author"]["name"] == "Alessandro Greco"

    standalone = ROOT / "nice-try-gpt"
    plugin_skill = ROOT / "skills" / "nice-try-gpt"
    standalone_files = sorted(
        path.relative_to(standalone) for path in standalone.rglob("*") if path.is_file()
    )
    plugin_files = sorted(
        path.relative_to(plugin_skill) for path in plugin_skill.rglob("*") if path.is_file()
    )

    assert standalone_files == plugin_files
    for relative in standalone_files:
        assert (standalone / relative).read_bytes() == (plugin_skill / relative).read_bytes()

    skill_text = (plugin_skill / "SKILL.md").read_text(encoding="utf-8")
    assert "name: nice-try-gpt" in skill_text
    assert f"version: {VERSION}" in skill_text


def test_eval_schema():
    results = ROOT / "evals" / "results.csv"
    with results.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    assert header == EXPECTED_EVAL_HEADER

    completed = subprocess.run(
        [sys.executable, str(ROOT / "evals" / "summarize.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "No evaluation results recorded yet." in completed.stdout


def test_example_contract():
    examples = ROOT / "examples"
    challenge_dirs = sorted(path for path in examples.iterdir() if path.is_dir())
    assert challenge_dirs

    for challenge in challenge_dirs:
        for relative in [
            Path("before/README.md"),
            Path("before/server.py"),
            Path("after/README.md"),
            Path("after/server.py"),
            Path("nicetrygpt-report.md"),
        ]:
            assert (challenge / relative).is_file(), f"{challenge.name}: missing {relative}"

        report = (challenge / "nicetrygpt-report.md").read_text(encoding="utf-8")
        assert report.startswith(f"# NiceTryGPT report — {challenge.name}\n")
        for field in REQUIRED_REPORT_FIELDS:
            assert f"- {field}:" in report, f"{challenge.name}: missing report field {field}"

        assert "- Baseline result: PASS" in report
        assert "- Shortcut reduction check: PASS" in report
        assert "- Post-change E2E result: PASS" in report
        assert "- Fresh-solver result: `NOT TESTED`" in report or "- Fresh-solver result: NOT TESTED" in report


def test_release_docs():
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    notes = (
        ROOT / ".github" / "release-notes" / f"v{VERSION}.md"
    ).read_text(encoding="utf-8")
    assert f"## [{VERSION}]" in changelog
    assert f"NiceTryGPT v{VERSION}" in notes


def test_project_metadata():
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    release_match = re.search(
        rf"## \[{re.escape(VERSION)}\] — (\d{{4}}-\d{{2}}-\d{{2}})",
        changelog,
    )
    assert release_match, "current VERSION must have a dated CHANGELOG entry"
    release_date = release_match.group(1)

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert 'cff-version: 1.2.0' in citation
    assert f'version: "{VERSION}"' in citation
    assert f'date-released: "{release_date}"' in citation
    assert 'repository-code: "https://github.com/aleff-github/NiceTryGPT"' in citation
    assert 'given-names: "Alessandro"' in citation
    assert 'family-names: "Greco"' in citation
    assert 'doi: "10.5281/zenodo.22858477"' in citation

    codemeta = json.loads((ROOT / "codemeta.json").read_text(encoding="utf-8"))
    assert codemeta["@context"] == "https://w3id.org/codemeta/3.1"
    assert codemeta["@type"] == "SoftwareSourceCode"
    assert codemeta["version"] == VERSION
    assert codemeta["datePublished"] == release_date
    assert codemeta["codeRepository"] == "https://github.com/aleff-github/NiceTryGPT"
    assert codemeta["identifier"] == "https://doi.org/10.5281/zenodo.22858477"
    assert codemeta["author"]["name"] == "Alessandro Greco"

    site = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert f'v{VERSION}' in site
    assert '"version": "' + VERSION + '"' in site
    assert 'https://github.com/aleff-github/NiceTryGPT/blob/main/CITATION.cff' in site
    assert "10.5281/zenodo.22858477" in site
    assert "Alessandro Greco" in site
    assert 'name="google-site-verification"' in site

    llms = (ROOT / "docs" / "llms.txt").read_text(encoding="utf-8")
    assert f"Current release: {VERSION}" in llms
    assert "DOI: 10.5281/zenodo.22858477" in llms

    preservation = (ROOT / "docs" / "preservation.md").read_text(encoding="utf-8")
    assert "Software Heritage" in preservation
    assert "Zenodo" in preservation

    archive_workflow = (ROOT / ".github" / "workflows" / "archive.yml").read_text(encoding="utf-8")
    assert "archive.softwareheritage.org/api/1/origin/save/" in archive_workflow
    assert "release:" in archive_workflow


def test_readme_local_links():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)

    for target in links:
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        path = target.split("#", 1)[0]
        if not path:
            continue
        assert (ROOT / path).exists(), f"README local link does not exist: {target}"


def main():
    tests = [
        ("release package", test_package),
        ("Claude Code plugin", test_claude_plugin),
        ("evaluation schema", test_eval_schema),
        ("example contract", test_example_contract),
        ("release docs", test_release_docs),
        ("project metadata", test_project_metadata),
        ("README local links", test_readme_local_links),
    ]
    failed = 0

    for name, fn in tests:
        try:
            fn()
            print(f"PASS  {name}")
        except Exception as exc:
            failed += 1
            print(f"FAIL  {name}: {exc}")

    if failed:
        raise SystemExit(1)

    print("\nNiceTryGPT release checks: PASS")


if __name__ == "__main__":
    main()
