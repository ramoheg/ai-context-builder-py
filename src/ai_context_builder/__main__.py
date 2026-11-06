import argparse
from pathlib import Path

from ai_context_builder.markdown import build_markdown
from ai_context_builder.scanner import scan_folder
from ai_context_builder.tree import Tree, build_tree, render_tree


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate AI-Friendly Markdown context file from a project folder."
    )

    parser.add_argument("folder", type=Path, help="the project folder to scan.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("context.md"),
        help="output file (default: context.md)",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root: Path = args.folder.resolve()
    output_path: Path = args.output

    if not root.is_dir():
        raise SystemExit(f"Error: '{root}' is not a folder.")

    files: list[Path] = scan_folder(root, output_path)
    tree: Tree = build_tree(files, root)
    tree_lines: list[str] = render_tree(tree)

    markdown: str = build_markdown(root, files, tree_lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown + "\n", encoding="utf-8")

    print(f"Wrote {len(files)} files to {output_path}")


if __name__ == "__main__":
    main()
