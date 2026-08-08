from crewai import Task
from .agents import static_reviewer, logic_reviewer, report_writer

STATIC_TASK_DESC = """\
Analyze this Java file using the java_static_analyzer tool. Pass the full
source code below into the tool exactly as given, then report the tool's
findings as a bullet list. Do not invent findings the tool did not return.

FILE: {file_path}

SOURCE:
{code}
"""

LOGIC_TASK_DESC = """\
Review this Java file for correctness and design issues that static analysis
would miss: null handling, off-by-one errors, resource leaks, thread-safety,
unclear or overly complex logic, and poor error handling. For each issue,
cite the line number, explain the risk in one sentence, and suggest a
concrete fix in one sentence.

FILE: {file_path}

SOURCE:
{code}

STATIC ANALYSIS FINDINGS (for context, don't just repeat these):
{{static_findings}}
"""

REPORT_TASK_DESC = """\
Combine the static analysis findings and the logic review findings into one
markdown report for {file_path}. Structure it as:

# Code Review: {file_path}

## Critical
(bugs, correctness issues, resource leaks)

## Warning
(style, maintainability, naming, magic numbers)

## Nit
(minor polish suggestions)

Deduplicate overlapping points. Keep each bullet to one or two sentences.
End with a one-line overall verdict (Ready to merge / Needs changes / Needs rework).
"""


def build_tasks(file_path: str, code: str):
    static_task = Task(
        description=STATIC_TASK_DESC.format(file_path=file_path, code=code),
        expected_output="A bullet list of static analysis findings.",
        agent=static_reviewer,
    )

    logic_task = Task(
        description=LOGIC_TASK_DESC.format(file_path=file_path, code=code),
        expected_output="A bullet list of logic/design issues with line numbers and fixes.",
        agent=logic_reviewer,
        context=[static_task],
    )

    report_task = Task(
        description=REPORT_TASK_DESC.format(file_path=file_path),
        expected_output="A single consolidated markdown review report.",
        agent=report_writer,
        context=[static_task, logic_task],
    )

    return [static_task, logic_task, report_task]
