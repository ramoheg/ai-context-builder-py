import argparse
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import find_dotenv, load_dotenv

from ai_context_builder.markdown import build_markdown
from ai_context_builder.scanner import scan_folder
from ai_context_builder.tokens import count_tokens
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
    parser.add_argument(
        "--count-tokens",
        action="store_true",
        help="count the tokens of the generated context (needs ANTHROPIC_API_KEY)",
    )

    return parser.parse_args()


def create_client() -> Anthropic:
    load_dotenv(find_dotenv(usecwd=True))

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise SystemExit(
            "--count-tokens needs an Anthropic API key. "
            "Set ANTHROPIC_API_KEY or add it to a .env file."
        )

    return Anthropic()


def main() -> None:
    args = parse_args()
    root: Path = args.folder.resolve()
    output_path: Path = args.output

    if not root.is_dir():
        raise SystemExit(f"Error: '{root}' is not a folder.")

    client: Anthropic | None = create_client() if args.count_tokens else None

    files: list[Path] = scan_folder(root, output_path)
    tree: Tree = build_tree(files, root)
    tree_lines: list[str] = render_tree(tree)

    content: str = build_markdown(root, files, tree_lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content + "\n", encoding="utf-8")

    print(f"Wrote {len(files)} files to {output_path}")

    if client is not None:
        tokens: int = count_tokens(client, content)
        print(f"Context size: {tokens:,} tokens")


if __name__ == "__main__":
    main()
