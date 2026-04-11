import argparse
import json
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
        "word_count_ok": isinstance(total_words, int) and 350 <= total_words <= 550,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate LLM script outputs")
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--output", default="test_results/model_evaluation.json")
    args = parser.parse_args()

    results = {}
    for f in args.inputs:
        p = Path(f)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            results[str(p)] = evaluate_script(data)
        except Exception as exc:
            results[str(p)] = {"error": str(exc)}

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ts_out = out.parent / f"model_evaluation_{ts}.json"
    ts_out.write_text(json.dumps(results, indent=2), encoding="utf-8")

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
