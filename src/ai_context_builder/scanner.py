from pathlib import Path

from ai_context_builder.ignore import is_ignored


def scan_folder(root: Path) -> list[Path]:
    folder: Path = Path(root)
    files: list[Path] = sorted(
        p for p in folder.rglob("*") if p.is_file() and not is_ignored(p, root)
    )

    return files
