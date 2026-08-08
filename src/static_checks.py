"""
Lightweight heuristic static analysis for Java source files.

This is NOT a full parser -- it's a set of regex/line-based heuristics
that are fast, dependency-free, and good enough to hand real findings
to the LLM reasoning agent for deeper review. Extend this file with
more checks as you build the project out (e.g. cyclomatic complexity,
unused imports, missing null checks).
"""

import re
from crewai.tools import tool


def _find_long_methods(lines: list[str], max_lines: int = 25) -> list[str]:
    findings = []
    method_start = None
    method_name = None
    brace_depth = 0
    in_method = False

    method_pattern = re.compile(
        r"\b(public|private|protected|static|\s)+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*\{?"
    )

    for i, line in enumerate(lines):
        if not in_method:
            m = method_pattern.search(line)
            if m and "{" in line and "class " not in line:
                in_method = True
                method_start = i
                method_name = m.group(2)
                brace_depth = line.count("{") - line.count("}")
        else:
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0:
                length = i - method_start
                if length > max_lines:
                    findings.append(
                        f"Line {method_start + 1}: method '{method_name}' is "
                        f"{length} lines long (over {max_lines}) -- consider splitting it."
                    )
                in_method = False
    return findings


def _find_empty_catch_blocks(lines: list[str]) -> list[str]:
    findings = []
    for i, line in enumerate(lines):
        if "catch" in line and "(" in line:
            # look ahead a couple of lines for an empty body
            snippet = " ".join(lines[i : i + 3])
            if re.search(r"catch\s*\([^)]*\)\s*\{\s*\}", snippet):
                findings.append(
                    f"Line {i + 1}: empty catch block -- exceptions are being swallowed silently."
                )
    return findings


def _find_todo_comments(lines: list[str]) -> list[str]:
    findings = []
    for i, line in enumerate(lines):
        if re.search(r"//\s*(TODO|FIXME)", line, re.IGNORECASE):
            findings.append(f"Line {i + 1}: unresolved TODO/FIXME -- {line.strip()}")
    return findings


def _find_magic_numbers(lines: list[str]) -> list[str]:
    findings = []
    pattern = re.compile(r"(?<![\w.])\b(?!0\b|1\b)\d{2,}\b(?![\w.])")
    for i, line in enumerate(lines):
        if "//" in line:
            line = line.split("//")[0]
        if pattern.search(line) and "final" not in line:
            findings.append(
                f"Line {i + 1}: possible magic number -- consider a named constant."
            )
    return findings


def _find_naming_violations(lines: list[str]) -> list[str]:
    findings = []
    var_pattern = re.compile(r"\b(int|String|boolean|double|float|long|char)\s+([A-Z]\w*)\s*[=;,)]")
    for i, line in enumerate(lines):
        m = var_pattern.search(line)
        if m:
            findings.append(
                f"Line {i + 1}: variable '{m.group(2)}' should be camelCase, not PascalCase."
            )
    return findings


@tool("java_static_analyzer")
def java_static_analyzer(source_code: str) -> str:
    """
    Runs heuristic static checks over a Java source file and returns a
    plain-text list of findings: long methods, empty catch blocks,
    TODO/FIXME markers, likely magic numbers, and naming violations.
    Input is the full Java source code as a string.
    """
    lines = source_code.splitlines()

    findings = []
    findings += _find_long_methods(lines)
    findings += _find_empty_catch_blocks(lines)
    findings += _find_todo_comments(lines)
    findings += _find_magic_numbers(lines)
    findings += _find_naming_violations(lines)

    if not findings:
        return "No heuristic issues found by static analysis."

    return "\n".join(f"- {f}" for f in findings)
