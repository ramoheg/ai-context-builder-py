from pathlib import Path

from ai_context_builder.scanner import scan_folder
from ai_context_builder.tree import Tree, build_tree


def main() -> None:
    root: Path = Path("tests/fixtures/sample_project")
    files: list[Path] = scan_folder(root)

    tree: Tree = build_tree(files, root)
    print(tree)


if __name__ == "__main__":
    main()
