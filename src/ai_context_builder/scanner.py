from pathlib import Path


def scan_folder(path: str) -> list[Path]:
    folder: Path = Path(path)
    files: list[Path] = sorted(p for p in folder.rglob("*") if p.is_file())

    return files