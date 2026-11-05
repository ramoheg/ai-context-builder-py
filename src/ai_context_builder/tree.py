from pathlib import Path

type Tree = dict[str, Tree]


def build_tree(files: list[Path], root: Path) -> Tree:
    tree: Tree = {}

    for file in files:
        current: Tree = tree
        for part in file.relative_to(root).parts:
            current = current.setdefault(part, {})
    return tree


def render_tree(tree: Tree, indent: str = "") -> list[str]:
    lines: list[str] = []
    for name, subtree in tree.items():
        if subtree:
            lines.append(f"{indent}{name}/")
            lines.extend(render_tree(subtree, indent + "    "))
        else:
            lines.append(f"{indent}{name}")

    return lines
