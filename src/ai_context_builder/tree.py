from pathlib import Path

type Tree = dict[str, Tree]


def build_tree(files: list[Path], root: Path) -> Tree:
    tree: Tree = {}

    for file in files:
        current: Tree = tree
        for part in file.relative_to(root).parts:
            current = current.setdefault(part, {})
    return tree


def render_tree(tree: Tree, prefix: str = "") -> list[str]:
    lines: list[str] = []
    entries = list(tree.items())

    for index, (name, subtree) in enumerate(entries):
        is_last: bool = index == len(entries) - 1
        connector: str = "└── " if is_last else "├── "

        if subtree:
            lines.append(f"{prefix}{connector}{name}/")
            extension: str = "    " if is_last else "|   "
            lines.extend(render_tree(subtree, prefix + extension))
        else:
            lines.append(f"{prefix}{connector}{name}")

    return lines
