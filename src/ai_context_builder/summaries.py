from pathlib import Path

from anthropic import Anthropic
from anthropic.types import ModelParam, ToolParam
from pydantic import BaseModel, Field


class FileSummary(BaseModel):
    summary: str = Field(
        description=(
            "One or two sentences describing what the file does and why it exists."
        )
    )
    dependencies: list[str] = Field(
        description=(
            "Relative paths of other files from this project that the file uses. "
            "Paths start below the top folder of the project tree and include every "
            "folder from there, with forward slashes, for example "
            "'src/ai_context_builder/tree.py'. Leave out external packages."
        )
    )


SUMMARY_MODEL: ModelParam = "claude-haiku-5-5"

SUMMARY_TOOL: ToolParam = {
    "name": "save_file_summary",
    "description": "Saves the summary of a source file.",
    "input_schema": FileSummary.model_json_schema(),
}


def build_system_prompt(tree_text: str) -> str:
    return (
        "You summarize source files of a software project for a developer who is "
        "new to it. Be concrete: name what the file does, not how it is written. "
        "Do not repeat the file name.\n\n"
        f"<project_tree>\n{tree_text}\n</project_tree>"
    )


def summarize_file(
    client: Anthropic,
    file: Path,
    root: Path,
    system_prompt: str,
    model: ModelParam = SUMMARY_MODEL,
) -> FileSummary:
    relative_path: str = file.relative_to(root).as_posix()
    content: str = file.read_text(encoding="utf-8").rstrip("\n")

    response = client.messages.create(
        model=model,
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": (
                    f'<file path="{relative_path}">\n{content}\n</file>\n\n'
                    "Summarize this file."
                ),
            }
        ],
        tools=[SUMMARY_TOOL],
        tool_choice={"type": "tool", "name": "save_file_summary"},
    )

    tool_use = next(
        (block for block in response.content if block.type == "tool_use"), None
    )

    if tool_use is None:
        raise ValueError("Claude did not return a summary.")

    return FileSummary.model_validate(tool_use.input)
