import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Prepare multi-LLM generation input")
    parser.add_argument("--extracted-text", required=True)
    parser.add_argument("--output-dir", default="llm_outputs")
    args = parser.parse_args()

    txt = Path(args.extracted_text)
    if not txt.exists():
        raise FileNotFoundError(f"Missing file: {txt}")

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    prompt = {
        "instruction": "Generate a 3-minute educational video script from the source content.",
        "source_content": txt.read_text(encoding="utf-8")[:12000],
    }
    out = outdir / "prompt_payload.json"
    out.write_text(json.dumps(prompt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
