import os
from crewai import Agent, LLM
from .static_checks import java_static_analyzer

# Local model served via Ollama. Swap the tag to trade speed vs. quality:
#   - "ollama/qwen2.5-coder:3b-instruct-q4_K_M"  -> fastest, good while iterating
#   - "ollama/qwen2.5-coder:7b-instruct-q4_K_M"  -> better reasoning, slower on CPU
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "ollama/qwen2.5-coder:7b-instruct-q4_K_M")
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

llm = LLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.2,
)


static_reviewer = Agent(
    role="Static Code Analyst",
    goal="Run static heuristics over the given Java file and report every finding precisely.",
    backstory=(
        "You are a meticulous static analysis tool operator. You never guess -- "
        "you run the analyzer tool and report exactly what it returns, "
        "formatted as a clear bullet list."
    ),
    tools=[java_static_analyzer],
    llm=llm,
    verbose=True,
)

logic_reviewer = Agent(
    role="Senior Java Reviewer",
    goal=(
        "Review the Java source for correctness, edge cases, and design issues "
        "that static analysis can't catch -- null handling, off-by-one errors, "
        "resource leaks, thread-safety, and unclear logic."
    ),
    backstory=(
        "You are a senior backend engineer who has reviewed thousands of Java "
        "PRs. You read code the way a human reviewer would: you reason about "
        "what the code is trying to do, then flag where it could break. You are "
        "specific -- you always cite line numbers and explain WHY something is "
        "risky, and you suggest a concrete fix."
    ),
    llm=llm,
    verbose=True,
)

report_writer = Agent(
    role="Tech Lead",
    goal="Consolidate the static and logic review findings into one clean, prioritized markdown report.",
    backstory=(
        "You write review summaries that a busy engineer can act on in under a "
        "minute. You group findings by severity (Critical / Warning / Nit), "
        "avoid repeating the same point twice, and keep the tone constructive."
    ),
    llm=llm,
    verbose=True,
)
