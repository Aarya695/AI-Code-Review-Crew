import sys
from pathlib import Path

# allow running as `python src/main.py` as well as `python -m src.main`
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.crew import run_review


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <path-to-java-file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    code = file_path.read_text()

    print(f"Reviewing {file_path} ...\n")
    report = run_review(str(file_path), code)

    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    out_path = output_dir / f"report_{file_path.stem}.md"
    out_path.write_text(report)

    print(f"\nDone. Report saved to {out_path}")


if __name__ == "__main__":
    main()
