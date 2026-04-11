import argparse
from pathlib import Path

from backup_manager import restore_from_snapshot


def latest_snapshot(project_root: Path):
    snaps = sorted((project_root / ".recovery" / "snapshots").glob("*"))
    if not snaps:
        return None
    return snaps[-1]


def main() -> None:
    parser = argparse.ArgumentParser(description="One-command restore from latest snapshot")
    parser.add_argument("--snapshot", default=None, help="Optional explicit snapshot directory")
    args = parser.parse_args()

    project_root = Path.cwd()
    snap = Path(args.snapshot) if args.snapshot else latest_snapshot(project_root)
    if snap is None:
        raise FileNotFoundError("No snapshots found under .recovery/snapshots")

    restore_from_snapshot(project_root, snap)
    print(f"Restored from snapshot: {snap}")


if __name__ == "__main__":
    main()
