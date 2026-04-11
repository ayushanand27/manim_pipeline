# PDF → Video Script → LLM Comparison Pipeline

Complete end-to-end workflow to extract PDF content, generate video scripts from multiple LLMs, and compare outputs.

## Quick Start Workflow (Minimal Commands)

### Step 1: PDF Extraction (OCR Enabled)
Extract text from PDF with OCR fallback.

```bash
python .\phase1_pdf_extraction.py --pdf ".\iesc107.pdf" --use-ocr --force-ocr --max-chars 0 --output-dir ".\extraction_outputs"
```

**Output Files:**
- `extraction_outputs/extracted_text.txt` — Full extracted text
- `extraction_outputs/extraction_breakdown.json` — Structured breakdown

**View extracted text:**
```bash
notepad .\extraction_outputs\extracted_text.txt
```

---

### Step 2: Chunk Text into Equal Parts (8000 chars each)
Split extracted text into manageable chunks for LLM processing.

```bash
python -c "import json, math, pathlib; t=json.load(open('extraction_outputs/extraction_breakdown.json','r',encoding='utf-8'))['extracted_text']; n=8000; p=pathlib.Path('extraction_outputs/chunks'); p.mkdir(parents=True, exist_ok=True); total=math.ceil(len(t)/n); [open(p/f'chunk_{i+1}.txt','w',encoding='utf-8').write(t[i*n:(i+1)*n]) for i in range(total)]; print('chunks:',total)"
```

**Output:** `extraction_outputs/chunks/chunk_1.txt`, `chunk_2.txt`, etc.

---

### Step 3: Generate Video Scripts from LLMs
Feed chunks to multiple LLM models with standardized prompt.

**System Prompt:**
```
You are an educational video script writer.
Using only the source content below, generate a 3-minute video script for Grade 9.
Return only plain text with no JSON.

Rules:
- exactly 5 scenes
- 400 to 500 words
- simple student-friendly language
- no hallucination; use only source content
```

**For each LLM model:**
1. Load the chunk text from `extraction_outputs/chunks/chunk_1.txt` (or other chunks)
2. Send to LLM with the prompt above
3. Copy the plain-text output

**Save outputs with model name:**
```
llm_outputs/llama3_1_8b.txt
llm_outputs/mistral_7b.txt
llm_outputs/gpt4o.txt
llm_outputs/claude_opus.txt
```

**Output Format (Plain Text):**
```text
TITLE: Motion and Distance Displacement
GRADE: 9
DURATION: 3 minutes

SCENE 1: ...
Visuals: ...
Narration: ...

SCENE 2: ...
Visuals: ...
Narration: ...

SCENE 3: ...
Visuals: ...
Narration: ...

SCENE 4: ...
Visuals: ...
Narration: ...

SCENE 5: recap
Visuals: ...
Narration: ...

REAL-LIFE EXAMPLE: ...
RECAP: ...
```

---

### Step 4: Evaluate Generated Scripts
Compare LLM outputs against quality criteria.

```bash
python .\scripts\phase4_evaluation.py --inputs llm_outputs\llama3_1_8b.txt llm_outputs\mistral_7b.txt --output test_results\model_evaluation.txt
```

**Evaluation Criteria:**
- ✅ Plain text output
- ✅ All required fields present
- ✅ Exactly 5 scenes
- ✅ Word count: 400-500
- ✅ No hallucination (uses only source content)

---

## 4-Phase Workflow (Deprecated - Use Quick Start Above)

### Phase 1: PDF Extraction
Extract text from PDF using embedded text + OCR fallback.

```bash
.\.venv\Scripts\python.exe phase1_pdf_extraction.py \
  --pdf iesc107.pdf \
  --output-dir extraction_outputs \
  --use-ocr \
  --force-ocr \
  --max-chars 50000
```

**Output:**
- `extraction_outputs/extracted_text.txt` — Clean extracted text
- `extraction_outputs/extraction_breakdown.json` — Page-by-page breakdown

---

### Phase 2 & 3: Multi-LLM Video Script Generation
Generate video scripts from multiple LLM providers simultaneously.

```bash
.\.venv\Scripts\python.exe phase2_multi_llm_generation.py \
  --extracted-text extraction_outputs/extracted_text.txt \
  --topic "Motion and Distance Displacement" \
  --output-dir llm_outputs \
  --openai-model gpt-4o gpt-4-turbo \
  --anthropic-model claude-opus-4-1 \
  --hf-model meta-llama/Llama-2-7b-chat-hf \
  --lmstudio-model mistral-7b-instruct-v0.2
```

**Before running Phase 2:**
1. Set API keys in environment:
   ```powershell
   $env:OPENAI_API_KEY="your-key"
   $env:ANTHROPIC_API_KEY="your-key"
   $env:HF_TOKEN="your-token"
   ```

2. If using LM Studio:
   - Start LM Studio and load your model
   - Ensure server is running on `http://127.0.0.1:1234`

**Output:**
- `llm_outputs/multi_llm_outputs.json` — All LLM responses

---

### Phase 4: Evaluation & Comparison
Compare scripts using metrics and LLM judges.

```bash
.\.venv\Scripts\python.exe phase4_evaluation.py \
  --llm-outputs llm_outputs/multi_llm_outputs.json \
  --criteria "engagement, clarity, structure, accuracy, educational_value" \
  --judge-model both \
  --output-dir evaluation_results
```

**Output:**
- `evaluation_results/evaluation_results.json` — Detailed metrics for each script
- `evaluation_results/summary.txt` — Judge rankings and recommendations

---

## Quick Start (All 4 Phases in Sequence)

```powershell
# 1. Extract
.\.venv\Scripts\python.exe phase1_pdf_extraction.py \
  --pdf your_pdf.pdf --use-ocr --force-ocr

# 2. Generate from multiple LLMs
.\.venv\Scripts\python.exe phase2_multi_llm_generation.py \
  --extracted-text extraction_outputs/extracted_text.txt \
  --openai-model gpt-4o \
  --anthropic-model claude-opus-4-1 \
  --lmstudio-model mistral

# 3. Evaluate
.\.venv\Scripts\python.exe phase4_evaluation.py \
  --llm-outputs llm_outputs/multi_llm_outputs.json \
  --judge-model both
```

---

## Environment Setup

### 1. Install Dependencies
```powershell
pip install -r requirements_pdf_to_script.txt
```

### 2. Set API Keys (if using paid APIs)

**OpenAI:**
```powershell
$env:OPENAI_API_KEY="sk-..."
```

**Anthropic (Claude):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

**HuggingFace:**
```powershell
$env:HF_TOKEN="hf_..."
```

### 3. LM Studio Setup (Local Models)
- Download LM Studio: https://lmstudio.ai
- Load Mistral 7B or Phi-3 Mini
- Start Local Server on port 1234
- Use `--lmstudio-model <model-name>` in Phase 2

### 4. Tesseract OCR (for scanned PDFs)
```powershell
# Add to PATH
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"
```

Verify:
```powershell
tesseract --version
```

---

## Phase Parameters Explained

### Phase 1: PDF Extraction
| Parameter | Default | Notes |
|-----------|---------|-------|
| `--use-ocr` | false | Enable OCR fallback for scanned pages |
| `--force-ocr` | false | Run OCR on every page (slower but more thorough) |
| `--max-chars` | 50000 | Stop extraction after this many characters |
| `--ocr-lang` | eng | Tesseract language code (eng, hin, fra, etc) |
| `--ocr-dpi-scale` | 2.5 | Scale for OCR rendering (higher = better quality, slower) |
| `--tesseract-psm` | 6 | Page segmentation mode (4, 6, 11, etc) |

### Phase 2: Multi-LLM Generation
| Parameter | Notes |
|-----------|-------|
| `--openai-model` | Comma-separated OpenAI models (gpt-4o, gpt-4-turbo, etc) |
| `--anthropic-model` | Anthropic models (claude-opus-4-1, claude-sonnet-4, etc) |
| `--hf-model` | HuggingFace model IDs |
| `--lmstudio-model` | Local models loaded in LM Studio |
| `--lmstudio-url` | Default: `http://127.0.0.1:1234/v1` |

### Phase 4: Evaluation
| Parameter | Options |
|-----------|---------|
| `--judge-model` | `openai`, `claude`, `both`, `none` |
| `--criteria` | Custom evaluation criteria (comma-separated) |

---

## Output Structure

```
extraction_outputs/
  ├── extracted_text.txt
  └── extraction_breakdown.json

llm_outputs/
  └── multi_llm_outputs.json

evaluation_results/
  ├── evaluation_results.json
  └── summary.txt
```

---

## Metrics Explained

### Readability Metrics (Phase 4)
- **Flesch Reading Ease**: 0-100 (higher = easier to read)
  - 90-100: 5th grade
  - 60-70: 8th-9th grade
  - < 30: College graduate

- **Flesch-Kincaid Grade**: US grade level required to understand

### ROUGE Scores
- **ROUGE-1**: 1-gram overlap (word-level)
- **ROUGE-2**: 2-gram overlap (phrase-level)
- **ROUGE-L**: Longest common subsequence

### BERTScore
- **Precision**: How much of the candidate is relevant
- **Recall**: How much of the reference is covered
- **F1**: Combined score

### Judge Rankings
Scores 1-10 based on:
- Engagement (hook, real-life examples)
- Clarity (vocabulary, sentence structure)
- Structure (flow, organization)
- Accuracy (facts, alignment with source)
- Educational value (learning outcomes)

---

## Troubleshooting

### "Cannot find Tesseract"
```powershell
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"
# Close and reopen terminal
```

### "API key not set"
```powershell
$env:OPENAI_API_KEY="your-key"
# Or set permanently
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key", "User")
```

### "LM Studio connection refused"
- Ensure LM Studio is running
- Ensure a model is loaded
- Ensure server is on port 1234
- Check: `curl http://127.0.0.1:1234/v1/models`

### "OCR quality is poor"
Try increasing `--ocr-dpi-scale` (2.5 → 3.0 or 4.0):
```powershell
--ocr-dpi-scale 3.5 --tesseract-psm 4
```

---

## Notes

- **Phase 2 requires API keys** for paid models (OpenAI, Anthropic)
- **LM Studio is free** and can run offline
- **Phase 4 evaluation of scripts requires** paid API keys (for LLM judges)
- **Optional:** Use free evaluation-only mode with `--judge-model none` to skip LLM judges

---

## Example: Full Workflow with Free/Local Models

```powershell
# Prerequisites:
# - LM Studio running with Mistral 7B loaded
# - Tesseract installed

# Phase 1: Extract
.\.venv\Scripts\python.exe phase1_pdf_extraction.py \
  --pdf ncert_physics.pdf \
  --use-ocr --force-ocr

# Phase 2: Generate (LM Studio only - free)
.\.venv\Scripts\python.exe phase2_multi_llm_generation.py \
  --extracted-text extraction_outputs/extracted_text.txt \
  --lmstudio-model mistral

# Phase 3: Evaluate (metrics only - free)
.\.venv\Scripts\python.exe phase4_evaluation.py \
  --llm-outputs llm_outputs/multi_llm_outputs.json \
  --judge-model none
```

---

For questions or issues, run `python <phase>.py --help`
