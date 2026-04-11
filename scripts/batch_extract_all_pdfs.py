import argparse
import subprocess
from pathlib import Path


def run_command(cmd: list[str]) -> int:
    process = subprocess.run(cmd)
    return process.returncode


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch extract all PDFs into separate subfolders")
    parser.add_argument("--input-dir", default="iesc1dd")
    parser.add_argument("--output-root", default="extraction_outputs")
    parser.add_argument("--use-ocr", action="store_true")
    parser.add_argument("--force-ocr", action="store_true")
    parser.add_argument("--max-chars", type=int, default=0)
    parser.add_argument("--group-target-chars", type=int, default=12000)
    parser.add_argument("--group-min-pages", type=int, default=2)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        raise FileNotFoundError(f"Input dir not found: {input_dir}")

    pdfs = sorted(input_dir.glob("*.pdf"))
    if not pdfs:
        print("No PDFs found.")
        return

    print(f"Found {len(pdfs)} PDF files")

    for pdf in pdfs:
        chapter = pdf.stem
        output_dir = Path(args.output_root) / chapter
        cmd = [
            "python",
            "scripts/phase1_pdf_extraction.py",
            "--pdf",
            str(pdf),
            "--output-dir",
            str(output_dir),
            "--max-chars",
            str(args.max_chars),
            "--group-target-chars",
            str(args.group_target_chars),
            "--group-min-pages",
            str(args.group_min_pages),
        ]

        if args.use_ocr:
            cmd.append("--use-ocr")
        if args.force_ocr:
            cmd.append("--force-ocr")

        print(f"\nProcessing: {pdf.name}")
        rc = run_command(cmd)
        if rc != 0:
            print(f"Failed: {pdf.name}")
        else:
            print(f"Done: {pdf.name} -> {output_dir}")


if __name__ == "__main__":
    main()
