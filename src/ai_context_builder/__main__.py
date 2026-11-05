from pathlib import Path

from ai_context_builder.markdown import build_markdown
from ai_context_builder.scanner import scan_folder
from ai_context_builder.tree import Tree, build_tree, render_tree


def main() -> None:
    root: Path = Path("tests/fixtures/sample_project")
    files: list[Path] = scan_folder(root)

    tree: Tree = build_tree(files, root)
    tree_lines: list[str] = render_tree(tree)

    markdown: str = build_markdown(root, files, tree_lines)
    Path("context.md").write_text(markdown + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
