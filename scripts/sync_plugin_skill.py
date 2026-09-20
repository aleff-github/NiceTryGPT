from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "nice-try-gpt"
DESTINATION = ROOT / "skills" / "nice-try-gpt"


def sync():
    if not (SOURCE / "SKILL.md").is_file():
        raise FileNotFoundError("nice-try-gpt/SKILL.md is missing")

    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)

    shutil.copytree(SOURCE, DESTINATION)
    print(f"Synced {SOURCE.relative_to(ROOT)} -> {DESTINATION.relative_to(ROOT)}")


if __name__ == "__main__":
    sync()
