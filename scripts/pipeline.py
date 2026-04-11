import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Simple pipeline placeholder")
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--models", nargs="+", default=["mistral"])
    parser.add_argument("--output", default="pipeline_results.json")
    args = parser.parse_args()

    result = {
        "message": "Use scripts/phase1_pdf_extraction.py for extraction, then send extracted_text to your selected models.",
        "pdf": args.pdf,
        "models": args.models,
    }

    out = Path(args.output)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
