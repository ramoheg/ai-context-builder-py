# AI Context Builder

A command line tool that turns a project folder into a single, AI-friendly Markdown file. It contains a tree of the project structure and the contents of all relevant files, ready to paste into an LLM.

## Features

- Scans a project folder recursively
- Filters out irrelevant files automatically:
  - folders like `.git`, `node_modules`, `bin`, `obj`, `.venv`, `__pycache__`
  - system files like `.DS_Store` and `Thumbs.db`
  - binary and unreadable files
  - files larger than 100 KB
- Generates a folder tree of the project
- Adds every file's content as a code block with syntax highlighting
- Never includes its own output file in the scan

## Requirements

- Python 3.14 or newer

## Usage

From the repository root:

```powershell
$env:PYTHONPATH = "src"
python -m ai_context_builder <folder>
```

Options:

| Option | Description |
|---|---|
| `folder` | The project folder to scan (required) |
| `-o`, `--output` | Output file (default: `context.md`) |

Examples:

```powershell
python -m ai_context_builder .
python -m ai_context_builder C:\path\to\project -o docs/context.md
python -m ai_context_builder --help
```

## Example output

````markdown
# Project context: sample_project

## Structure

```
sample_project/
├── README.md
└── src/
    ├── main.py
    └── utils/
        └── helpers.py
```

## Files

### src/utils/helpers.py

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```
````

## Project structure

```
src/ai_context_builder/
├── __main__.py   # command line interface
├── scanner.py    # walks the folder and collects files
├── ignore.py     # filter rules
├── tree.py       # builds and renders the folder tree
└── markdown.py   # generates the Markdown output
```

## Roadmap

- Respect the project's `.gitignore`
- Token counting, to check whether the output fits a model's context window
- AI-generated file summaries