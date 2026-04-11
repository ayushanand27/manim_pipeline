import json
import shutil
from datetime import datetime
from pathlib import Path


def timestamp_now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_recovery_root(project_root: Path) -> Path:
    recovery_root = project_root / ".recovery"
    recovery_root.mkdir(parents=True, exist_ok=True)
    return recovery_root


def snapshot_paths(project_root: Path, relative_paths: list[str], label: str) -> Path:
    recovery_root = ensure_recovery_root(project_root)
    snap_dir = recovery_root / "snapshots" / f"{timestamp_now()}_{label}"
    snap_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for rel in relative_paths:
        src = project_root / rel
        if not src.exists():
            continue
        dst = snap_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
        copied.append(rel)

    (snap_dir / "_snapshot_meta.json").write_text(
        json.dumps({"label": label, "copied": copied}, indent=2), encoding="utf-8"
    )
    return snap_dir


def write_restore_manifest(project_root: Path, relative_paths: list[str]) -> Path:
    recovery_root = ensure_recovery_root(project_root)
    manifest_path = recovery_root / "latest_restore_manifest.json"

    files = []
    for rel in relative_paths:
        p = project_root / rel
        files.append(
            {
                "path": rel,
                "exists": p.exists(),
                "type": "dir" if p.is_dir() else "file" if p.exists() else "missing",
            }
        )

    manifest = {
        "generated_at": timestamp_now(),
        "project_root": str(project_root),
        "tracked_outputs": files,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def restore_from_snapshot(project_root: Path, snapshot_dir: Path) -> None:
    if not snapshot_dir.exists():
        raise FileNotFoundError(f"Snapshot not found: {snapshot_dir}")

    for item in snapshot_dir.iterdir():
        if item.name == "_snapshot_meta.json":
            continue
        dst = project_root / item.name
        if item.is_dir():
            shutil.copytree(item, dst, dirs_exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dst)
