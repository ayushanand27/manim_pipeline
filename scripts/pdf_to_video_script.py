import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Minimal PDF-to-video helper")
    parser.add_argument("--extracted-json", default="extraction_outputs/extraction_breakdown.json")
    parser.add_argument("--output", default="test_results/motion_generated_script.json")
    args = parser.parse_args()

    data = json.loads(Path(args.extracted_json).read_text(encoding="utf-8"))
    payload = {
        "topic": "Describing Motion",
        "grade": 9,
        "duration_minutes": 3,
        "source_length": len(data.get("extracted_text", "")),
        "note": "Feed source text to your selected LLM and paste model output into llm_outputs/*.txt",
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
