#!/usr/bin/env python3

import ast
import subprocess
import sys

from collections.abc import Callable, Sequence
from pathlib import Path


def format_with_ruff(files: Sequence[str]) -> bool:
    cmd = [
        "ruff",
        "format",
        "--isolated",
        "--config",
        "line-length=120",
        "--config",
        "format.indent-style='tab'",
        "--config",
        "format.skip-magic-trailing-comma=true",
        "--config",
        "format.line-ending='lf'",
        "--config",
        "format.docstring-code-format=false",
        *files,
    ]

    result = subprocess.run(  # noqa: S603 - the command is fixed and shell execution is disabled
        cmd, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        sys.stderr.write(f"Error running ruff: {result.stderr}\n")
        return False
    return True


def _is_docstring_node(node: ast.stmt) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def remove_blank_lines(file_path: str) -> None:
    path = Path(file_path)
    with path.open() as f:
        content = f.read()

    # Keep only non-empty lines (lines with at least one non-whitespace character)
    lines = content.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]

    with path.open("w") as f:
        f.write("\n".join(non_empty_lines))


def remove_docstrings(file_path: str) -> bool:
    path = Path(file_path)
    with path.open() as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        sys.stderr.write(f"Error parsing {file_path}: {e}\n")
        return False

    # Target nodes that can have docstrings
    docstring_containers = (
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.Module,
    )

    for node in ast.walk(tree):
        if not isinstance(node, docstring_containers):
            continue

        # Remove the first statement if it's a docstring
        if node.body and _is_docstring_node(node.body[0]):
            node.body.pop(0)

    # Reconstruct source code and write back
    minimized_source = ast.unparse(tree)
    with path.open("w") as f:
        f.write(minimized_source)

    return True


def _process_files(files: Sequence[str], processor: Callable[[str], bool | None]) -> bool:
    """Apply a processing function to files, skipping flag arguments"""
    for file_path in files:
        if file_path.startswith("-"):
            continue
        if not processor(file_path):
            return False
    return True


def main() -> None:
    """Minimize Python files by removing docstrings and blank lines"""
    min_args = 2
    if len(sys.argv) < min_args:
        sys.stderr.write("Usage: python_minimization.py <file1> [file2] ...\n")
        sys.exit(1)

    files = sys.argv[1:]

    sys.stdout.write("Step: Removing docstrings...\n")
    if not _process_files(files, remove_docstrings):
        sys.exit(1)

    sys.stdout.write("Step: Formatting with ruff...\n")
    if not format_with_ruff(files):
        sys.exit(1)

    sys.stdout.write("Step: Removing blank lines...\n")
    _process_files(files, remove_blank_lines)

    sys.stdout.write("Done!\n")


if __name__ == "__main__":
    main()
