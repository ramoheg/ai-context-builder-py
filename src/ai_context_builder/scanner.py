from pathlib import Path

from ignore import is_ignored


def scan_folder(root: str) -> list[Path]:
    folder: Path = Path(root)
    files: list[Path] = sorted(p for p in folder.rglob("*") if p.is_file() and not is_ignored(p, root))

    return files