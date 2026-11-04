from pathlib import Path

from scanner import scan_folder


def main() -> None:
    path: str = "./tests/fixtures/sample_project"
    files: list[Path] = scan_folder(path)

    for file in files:
        print(file)


if __name__ == "__main__":
    main()