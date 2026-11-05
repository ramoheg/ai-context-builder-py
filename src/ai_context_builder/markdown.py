from pathlib import Path

LANGUAGES: dict[str, str] = {
    ".py": "python",
    ".cs": "csharp",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "jsx",
    ".tsx": "tsx",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".md": "markdown",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
    ".sql": "sql",
    ".ps1": "powershell",
    ".sh": "bash",
}


def render_file(file: Path, root: Path) -> str:
    relative_path: str = file.relative_to(root).as_posix()
    language: str = LANGUAGES.get(file.suffix.lower(), "")
    content = file.read_text(encoding="utf-8").rstrip("\n")

    return f"### {relative_path}\n\n```{language}\n{content}\n```"


def build_markdown(root: Path, files: list[Path], tree_lines: list[str]) -> str:
    tree: str = "\n".join([f"{root.name}/", *tree_lines])

    sections: list[str] = [
        f"# Project context: {root.name}",
        "## Structure",
        f"```\n{tree}\n```",
        "## Files",
    ]
    sections.extend(render_file(file, root) for file in files)

    return "\n\n".join(sections)
