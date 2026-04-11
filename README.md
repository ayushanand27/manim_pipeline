# Gen AI Internship - NCERT Video Script Pipeline

This repository extracts chapter text from NCERT PDFs, creates page and grouped chunks, supports manual LLM generation, and evaluates generated script outputs in either plain text or JSON.

## Repository Structure

- `scripts/` - all Python automation scripts
- `iesc1dd/` - source NCERT PDFs
- `extraction_outputs/` - extracted text plus page/group chunks per chapter
- `llm_outputs/` - model plain-text script outputs
- `test_results/` - evaluation outputs and validation artifacts
- `ncert_extracts/` - curated text extracts
- `docs/` - supplementary docs
- `workspace/my_work.txt` - personal working notes (kept intact)
- `.recovery/` - local recovery snapshots and restore metadata

## Setup

1. Create and activate virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements_pdf_to_script.txt
```

3. Optional OCR prerequisites

- Install Tesseract OCR on Windows.
- Default path used by script: `C:/Program Files/Tesseract-OCR/tesseract.exe`.

## Workflow

### 1) Single PDF extraction

```powershell
python .\scripts\phase1_pdf_extraction.py --pdf ".\iesc1dd\iesc107.pdf" --use-ocr --force-ocr --max-chars 0 --output-dir ".\extraction_outputs\iesc107"
```

Outputs include:

- `extraction_outputs/iesc107/extraction_breakdown.json`
- `extraction_outputs/iesc107/extracted_text.txt`
- `extraction_outputs/iesc107/chunks_pages/page_01.txt` ...
- `extraction_outputs/iesc107/chunks_grouped/group_01_p01-02.txt` ...

### 2) Chunking strategy

- `chunks_pages/`: one full page per file, no page splitting.
- `chunks_grouped/`: content-based grouping of whole pages, no page splitting.

Grouping controls:

- `--group-target-chars 12000`
- `--group-min-pages 2`

### 3) Batch extraction for all PDFs

```powershell
python .\scripts\batch_extract_all_pdfs.py --input-dir ".\iesc1dd" --output-root ".\extraction_outputs" --use-ocr --force-ocr --max-chars 0 --group-target-chars 12000 --group-min-pages 2
```

### 4) Manual LLM generation

Recommended manual flow per chapter/group:

1. Copy content from `chunks_grouped` or `extracted_text.txt`.
2. Paste the common prompt from `video_script_prompt.txt`.
3. Save model output as plain text or JSON into `llm_outputs/`.

Example naming:

- `llm_outputs/llama3_1_8b_iesc107.txt`
- `llm_outputs/mistral_7b_iesc107.txt`

### 5) Evaluation

```powershell
python .\scripts\phase4_evaluation.py --inputs llm_outputs\llama3_1_8b.txt llm_outputs\mistral_7b.txt --output test_results\model_evaluation.txt
```

### 6) Recovery and versioned outputs

Save timestamped model output and create snapshot:

```powershell
python .\scripts\save_model_output.py --model llama3_1_8b --input .\llm_outputs\llama3_1_8b.txt
```

Restore latest snapshot:

```powershell
python .\scripts\restore_outputs.py
```

Recovery paths:

- `.recovery/snapshots/`
- `.recovery/latest_restore_manifest.json`

## Notes

- No project files were deleted during restructuring.
- `my_work.txt` content is unchanged and now located at `workspace/my_work.txt`.
