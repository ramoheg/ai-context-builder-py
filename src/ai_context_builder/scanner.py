from pathlib import Path

from ai_context_builder.ignore import is_ignored


def scan_folder(root: Path, output_path: Path) -> list[Path]:
    output_file: Path = output_path.resolve()

    return sorted(
        p
        for p in root.rglob("*")
        if p.is_file() and p.resolve() != output_file and not is_ignored(p, root)
    )
