from crewai import Crew, Process
from .agents import static_reviewer, logic_reviewer, report_writer
from .tasks import build_tasks


def run_review(file_path: str, code: str) -> str:
    tasks = build_tasks(file_path, code)

    crew = Crew(
        agents=[static_reviewer, logic_reviewer, report_writer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
