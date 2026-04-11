import argparse
from datetime import datetime
from pathlib import Path

from backup_manager import snapshot_paths, write_restore_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Save model output with timestamp and create recovery snapshot")
    parser.add_argument("--model", required=True, help="Model name, e.g. llama3_1_8b")
    parser.add_argument("--input", required=True, help="Path to raw model output text or JSON")
    parser.add_argument("--output-dir", default="llm_outputs", help="Directory to store timestamped outputs")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        raise FileNotFoundError(f"Input file not found: {src}")

    raw_output = src.read_text(encoding="utf-8")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    out_file = outdir / f"{args.model}_{ts}{src.suffix if src.suffix in {'.txt', '.json'} else '.txt'}"
    out_file.write_text(raw_output, encoding="utf-8")

    project_root = Path.cwd()
    snapshot_paths(project_root, [str(out_file), args.output_dir, "test_results"], label="model_output")
    manifest = write_restore_manifest(project_root, [args.output_dir, "extraction_outputs", "test_results", "ncert_extracts"])

    print(f"Saved model output: {out_file}")
    print(f"Updated restore manifest: {manifest}")


if __name__ == "__main__":
    main()
