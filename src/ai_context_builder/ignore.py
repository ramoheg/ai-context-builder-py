from pathlib import Path

MAX_FILE_SIZE: int = 100_000  # 100 KB

IGNORED_FILES: set[str] = {".git", ".DS_Store", "Thumbs.db"}
IGNORED_DIRS: set[str] = {
    ".git",
    "node_modules",
    "bin",
    "obj",
    ".venv",
    "__pycache__",
    ".idea",
    ".vs"
}

def is_ignored(file: Path, root: Path) -> bool:
    relative_path: Path = file.relative_to(root)

    if relative_path.name in IGNORED_FILES:
        return True

    for part in relative_path.parent.parts:
        if part in IGNORED_DIRS:
            return True

    if is_too_large(file):
        return True
    
    return is_binary(file)


def is_binary(file: Path) -> bool:
    try:
        file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return True

    return False


def is_too_large(file: Path) -> bool:
    return file.stat().st_size > MAX_FILE_SIZE