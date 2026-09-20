from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import argparse
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "nice-try-gpt"
VERSION_FILE = ROOT / "VERSION"
DIST_DIR = ROOT / "dist"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def read_version():
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not version or any(c not in "0123456789." for c in version):
        raise ValueError(f"invalid VERSION: {version!r}")
    return version


def package(output=None):
    version = read_version()
    if not (SKILL_DIR / "SKILL.md").is_file():
        raise FileNotFoundError("nice-try-gpt/SKILL.md is missing")

    destination = Path(output) if output else DIST_DIR / f"nice-try-gpt-v{version}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)

    files = sorted(path for path in SKILL_DIR.rglob("*") if path.is_file())

    with ZipFile(destination, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            info = ZipInfo(relative, FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())

    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    print(destination)
    print(f"sha256:{digest}")
    return destination


def main():
    parser = argparse.ArgumentParser(description="Build a deterministic NiceTryGPT skill archive.")
    parser.add_argument("--output", help="Optional output ZIP path.")
    args = parser.parse_args()
    package(args.output)


if __name__ == "__main__":
    main()
