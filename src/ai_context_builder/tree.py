from pathlib import Path

type Tree = dict[str, Tree]


def build_tree(files: list[Path], root: Path) -> Tree:
    tree: Tree = {}

    for file in files:
        current: Tree = tree
        for part in file.relative_to(root).parts:
            current = current.setdefault(part, {})
    return tree
