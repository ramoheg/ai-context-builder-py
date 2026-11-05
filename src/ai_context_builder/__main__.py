from pathlib import Path

from ai_context_builder.scanner import scan_folder
from ai_context_builder.tree import Tree, build_tree, render_tree


def main() -> None:
    root: Path = Path("tests/fixtures/sample_project")
    files: list[Path] = scan_folder(root)

    tree: Tree = build_tree(files, root)

    lines: list[str] = render_tree(tree, "    ")
    print(f"{root.name}/")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
