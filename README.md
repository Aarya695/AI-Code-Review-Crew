# AI Code Review Crew

A multi-agent AI code reviewer for Java, built with **CrewAI** and running
entirely on a **local model via Ollama** (no API key needed).

Three agents work in sequence:

1. **Static Code Analyst** -- runs heuristic checks (long methods, empty
   catch blocks, TODOs, magic numbers, naming) via a custom tool.
2. **Senior Java Reviewer** -- uses the LLM to reason about correctness,
   edge cases, null handling, and resource/thread safety.
3. **Tech Lead** -- consolidates both into one prioritized markdown report
   (Critical / Warning / Nit).

### 1. Install Ollama

Download from https://ollama.com/download and install for your OS.

### 2. Pull a code model

On 16GB RAM / CPU-only, start with the 7B quantized coder model:

```bash
ollama pull qwen2.5-coder:7b-instruct-q4_K_M
```

If responses feel too slow while you're iterating on the code, switch to the
3B variant for speed (edit `OLLAMA_MODEL` in `src/agents.py` or set the env
var below):

```bash
ollama pull qwen2.5-coder:3b-instruct-q4_K_M
```

Ollama runs as a background service after install -- no need to start it
manually. Verify it's up:

```bash
ollama list
```

### 3. Python environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. (Optional) override the model/host

```bash
export OLLAMA_MODEL="ollama/qwen2.5-coder:3b-instruct-q4_K_M"
export OLLAMA_API_BASE="http://localhost:11434"
```

### 5. Run it

```bash
python src/main.py sample/Sample.java
```

The `sample/Sample.java` file has deliberate issues planted in it (off-by-one
loop, empty catch block, division without a zero-check, PascalCase variable,
magic numbers, an oversized method) so you can confirm each agent is
actually catching things.

Output report lands at `output/report_Sample.md`.

## Project structure

```
ai-code-review-crew/
├── README.md
├── requirements.txt
├── sample/
│   └── Sample.java          # test file with planted issues
├── src/
│   ├── static_checks.py     # heuristic analyzer (CrewAI tool)
│   ├── agents.py            # 3 agent definitions + local LLM config
│   ├── tasks.py             # task prompts, chained via `context`
│   ├── crew.py              # assembles and runs the Crew
│   └── main.py              # CLI entrypoint
└── output/                  # generated reports land here
```
