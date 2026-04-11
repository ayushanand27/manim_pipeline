import argparse
import json
import re
from pathlib import Path
from datetime import datetime

from backup_manager import snapshot_paths, write_restore_manifest


def evaluate_script(data):
    scenes = data.get("scenes", [])
    total_words = data.get("total_words", 0)
    return {
        "has_required_fields": all(k in data for k in ["topic", "grade", "duration_minutes", "total_words", "scenes", "real_life_example", "recap"]),
        "scene_count": len(scenes),
        "scene_count_ok": len(scenes) == 5,
        "word_count": total_words,
        "word_count_ok": isinstance(total_words, int) and 400 <= total_words <= 500,
    }


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def parse_plain_text_script(text: str) -> dict:
    lines = text.splitlines()
    data = {
        "topic": "",
        "grade": None,
        "duration_minutes": 3,
        "total_words": _word_count(text),
        "scenes": [],
        "real_life_example": "",
        "recap": "",
    }

    scene = None
    collecting = None

    def finish_scene() -> None:
        nonlocal scene
        if scene is not None:
            scene.setdefault("visuals", "")
            scene.setdefault("narration", "")
            data["scenes"].append(scene)
            scene = None

    def set_collecting(key: str, value: str) -> None:
        nonlocal collecting
        collecting = key
        data[key] = value.strip()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        title_match = re.match(r"^TITLE:\s*(.+)$", stripped, re.I)
        grade_match = re.match(r"^GRADE:\s*(\d+)", stripped, re.I)
        duration_match = re.match(r"^DURATION:\s*(\d+)", stripped, re.I)
        scene_match = re.match(r"^SCENE\s+(\d+)\s*:\s*(.*)$", stripped, re.I)
        visuals_match = re.match(r"^VISUALS:\s*(.*)$", stripped, re.I)
        narration_match = re.match(r"^NARRATION:\s*(.*)$", stripped, re.I)
        real_life_match = re.match(r"^REAL[- ]LIFE EXAMPLE:\s*(.*)$", stripped, re.I)
        recap_match = re.match(r"^RECAP:\s*(.*)$", stripped, re.I)

        if title_match:
            data["topic"] = title_match.group(1).strip()
            collecting = None
            continue
        if grade_match:
            data["grade"] = int(grade_match.group(1))
            collecting = None
            continue
        if duration_match:
            data["duration_minutes"] = int(duration_match.group(1))
            collecting = None
            continue
        if scene_match:
            finish_scene()
            scene = {
                "scene_number": int(scene_match.group(1)),
                "title": scene_match.group(2).strip() or f"Scene {scene_match.group(1)}",
                "duration_seconds": None,
                "visuals": "",
                "narration": "",
            }
            collecting = None
            continue
        if visuals_match and scene is not None:
            scene["visuals"] = visuals_match.group(1).strip()
            collecting = "scene_visuals"
            continue
        if narration_match and scene is not None:
            scene["narration"] = narration_match.group(1).strip()
            collecting = "scene_narration"
            continue
        if real_life_match:
            finish_scene()
            set_collecting("real_life_example", real_life_match.group(1))
            continue
        if recap_match:
            finish_scene()
            set_collecting("recap", recap_match.group(1))
            continue

        if scene is not None and collecting == "scene_visuals":
            scene["visuals"] = (scene["visuals"] + " " + stripped).strip()
            continue
        if scene is not None and collecting == "scene_narration":
            scene["narration"] = (scene["narration"] + " " + stripped).strip()
            continue
        if collecting in {"real_life_example", "recap"}:
            data[collecting] = (data[collecting] + " " + stripped).strip()

    finish_scene()

    if data["total_words"] == 0:
        data["total_words"] = _word_count(text)
    if data["grade"] is None:
        data["grade"] = 0

    return data


def load_script_output(path: Path) -> dict:
    raw_text = path.read_text(encoding="utf-8")
    try:
        loaded = json.loads(raw_text)
    except json.JSONDecodeError:
        return parse_plain_text_script(raw_text)

    if isinstance(loaded, dict):
        return loaded
    raise ValueError("Model output must be a JSON object or a structured plain-text script")


def render_report(results: dict[str, dict]) -> str:
    passed = 0
    total = len(results)
    lines = ["MODEL EVALUATION REPORT", "=" * 60]

    for path, result in results.items():
        lines.append(f"\nFILE: {path}")
        if "error" in result:
            lines.append(f"STATUS: ERROR")
            lines.append(f"DETAILS: {result['error']}")
            continue

        file_pass = bool(result.get("has_required_fields")) and bool(result.get("scene_count_ok")) and bool(result.get("word_count_ok"))
        if file_pass:
            passed += 1

        lines.append(f"STATUS: {'PASS' if file_pass else 'REVIEW'}")
        lines.append(f"HAS_REQUIRED_FIELDS: {result.get('has_required_fields')}")
        lines.append(f"SCENE_COUNT: {result.get('scene_count')} (need 5)")
        lines.append(f"SCENE_COUNT_OK: {result.get('scene_count_ok')}")
        lines.append(f"WORD_COUNT: {result.get('word_count')} (need 400-500)")
        lines.append(f"WORD_COUNT_OK: {result.get('word_count_ok')}")

    lines.append("\nSUMMARY")
    lines.append("=" * 60)
    lines.append(f"TOTAL_FILES: {total}")
    lines.append(f"PASSED: {passed}")
    lines.append(f"REVIEW: {total - passed}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Evaluate LLM script outputs")
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--output", default="test_results/model_evaluation.txt")
    args = parser.parse_args()

    results = {}
    for f in args.inputs:
        p = Path(f)
        try:
            data = load_script_output(p)
            results[str(p)] = evaluate_script(data)
        except Exception as exc:
            results[str(p)] = {"error": str(exc)}

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    report = render_report(results)
    out.write_text(report, encoding="utf-8")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ts_out = out.parent / f"model_evaluation_{ts}.txt"
    ts_out.write_text(report, encoding="utf-8")

    project_root = Path.cwd()
    snapshot_paths(
        project_root,
        [
            "llm_outputs",
            "test_results",
            "extraction_outputs",
            "ncert_extracts",
        ],
        label="phase4_eval",
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

    print(f"Saved: {out}")
    print(f"Timestamped: {ts_out}")


if __name__ == "__main__":
    main()
