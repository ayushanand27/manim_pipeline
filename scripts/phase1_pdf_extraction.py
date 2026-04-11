import argparse
import json
import os
import re
from pathlib import Path
from backup_manager import snapshot_paths, write_restore_manifest

from pypdf import PdfReader

try:
    import fitz
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
except Exception:
    fitz = None
    pytesseract = None
    Image = None


def configure_tesseract_path() -> None:
    if pytesseract is None:
        return
    if os.environ.get("TESSERACT_PATH"):
        pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_PATH"]
        return
    default_path = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
    if default_path.exists():
        pytesseract.pytesseract.tesseract_cmd = str(default_path)


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess(img):
    gray = ImageOps.grayscale(img)
    gray = ImageOps.autocontrast(gray)
    gray = gray.filter(ImageFilter.MedianFilter(size=3))
    sharp = ImageEnhance.Sharpness(gray).enhance(2.0)
    bw = sharp.point(lambda x: 0 if x < 160 else 255, mode="1")
    return bw.convert("L")


def ocr_page(doc, page_index: int, dpi: float, psm: int, oem: int, lang: str) -> str:
    page = doc.load_page(page_index)
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi, dpi), alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = preprocess(img)
    return pytesseract.image_to_string(img, lang=lang, config=f"--oem {oem} --psm {psm}")


def extract(pdf_path: Path, use_ocr: bool, force_ocr: bool, max_chars: int, lang: str, dpi: float, psm: int, oem: int):
    reader = PdfReader(str(pdf_path))
    ocr_doc = None
    if use_ocr:
        if fitz is None or pytesseract is None or Image is None:
            raise RuntimeError("OCR dependencies missing. Install requirements.")
        configure_tesseract_path()
        ocr_doc = fitz.open(str(pdf_path))

    pages_breakdown = []
    full_parts = []

    for i, p in enumerate(reader.pages, start=1):
        direct = normalize_text(p.extract_text() or "")
        page_text = direct
        if use_ocr and ocr_doc is not None and (force_ocr or not direct):
            try:
                ocr_txt = normalize_text(ocr_page(ocr_doc, i - 1, dpi, psm, oem, lang))
                if ocr_txt and ocr_txt not in direct:
                    page_text = (direct + "\n" + ocr_txt).strip() if direct else ocr_txt
            except Exception as exc:
                print(f"[Warning] OCR failed for page {i}: {exc}")

        if page_text:
            pages_breakdown.append({"page": i, "text": page_text})
            full_parts.append(f"[Page {i}]\n{page_text}")

        if max_chars > 0 and sum(len(x["text"]) for x in pages_breakdown) >= max_chars:
            break

    if ocr_doc is not None:
        ocr_doc.close()

    return {
        "total_pages": len(reader.pages),
        "extracted_pages": len(pages_breakdown),
        "extracted_text": "\n\n".join(full_parts),
        "pages_breakdown": pages_breakdown,
    }


def write_page_chunks(result: dict, outdir: Path) -> Path:
    chunks_dir = outdir / "chunks_pages"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    for i, page in enumerate(result.get("pages_breakdown", []), start=1):
        page_no = page.get("page", i)
        text = page.get("text", "")
        (chunks_dir / f"page_{page_no:02d}.txt").write_text(text, encoding="utf-8")

    return chunks_dir


def write_grouped_page_chunks(
    result: dict,
    outdir: Path,
    target_chars: int = 12000,
    min_pages_per_group: int = 2,
) -> Path:
    grouped_dir = outdir / "chunks_grouped"
    grouped_dir.mkdir(parents=True, exist_ok=True)

    pages = result.get("pages_breakdown", [])
    groups = []
    current_group = []
    current_chars = 0

    for page in pages:
        text = page.get("text", "")
        page_chars = len(text)

        if current_group:
            enough_pages = len(current_group) >= max(1, min_pages_per_group)
            would_exceed_target = (current_chars + page_chars) > target_chars
            if enough_pages and would_exceed_target:
                groups.append(current_group)
                current_group = []
                current_chars = 0

        current_group.append(page)
        current_chars += page_chars

    if current_group:
        groups.append(current_group)

    for idx, group in enumerate(groups, start=1):
        first_page = group[0].get("page", 0)
        last_page = group[-1].get("page", 0)
        body = "\n\n".join(
            [f"[Page {p.get('page', 0)}]\n{p.get('text', '')}" for p in group]
        )
        filename = f"group_{idx:02d}_p{first_page:02d}-{last_page:02d}.txt"
        (grouped_dir / filename).write_text(body, encoding="utf-8")

    return grouped_dir


def main():
    parser = argparse.ArgumentParser(description="Extract PDF text with optional OCR")
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--output-dir", default="extraction_outputs")
    parser.add_argument("--json-only", action="store_true")
    parser.add_argument("--use-ocr", action="store_true")
    parser.add_argument("--force-ocr", action="store_true")
    parser.add_argument("--max-chars", type=int, default=0)
    parser.add_argument("--ocr-lang", default="eng")
    parser.add_argument("--ocr-dpi-scale", type=float, default=2.5)
    parser.add_argument("--tesseract-psm", type=int, default=6)
    parser.add_argument("--tesseract-oem", type=int, default=3)
    parser.add_argument("--group-target-chars", type=int, default=12000)
    parser.add_argument("--group-min-pages", type=int, default=2)
    args = parser.parse_args()

    pdf = Path(args.pdf)
    if not pdf.exists():
        raise FileNotFoundError(f"PDF not found: {pdf}")

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    result = extract(
        pdf,
        use_ocr=args.use_ocr,
        force_ocr=args.force_ocr,
        max_chars=args.max_chars,
        lang=args.ocr_lang,
        dpi=args.ocr_dpi_scale,
        psm=args.tesseract_psm,
        oem=args.tesseract_oem,
    )

    json_path = outdir / "extraction_breakdown.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    chunks_dir = write_page_chunks(result, outdir)
    grouped_dir = write_grouped_page_chunks(
        result,
        outdir,
        target_chars=args.group_target_chars,
        min_pages_per_group=args.group_min_pages,
    )

    if not args.json_only:
        (outdir / "extracted_text.txt").write_text(result["extracted_text"], encoding="utf-8")

    project_root = Path.cwd()
    snapshot_paths(
        project_root,
        [
            args.output_dir,
            "ncert_extracts",
            "test_results",
            "llm_outputs",
        ],
        label="phase1_extract",
    )
    write_restore_manifest(
        project_root,
        [
            "extraction_outputs",
            "llm_outputs",
            "test_results",
            "ncert_extracts",
        ],
    )

    print(f"Extracted {result['extracted_pages']} pages")
    print(f"JSON saved: {json_path}")
    print(f"Page chunks saved: {chunks_dir}")
    print(f"Grouped chunks saved: {grouped_dir}")


if __name__ == "__main__":
    main()
