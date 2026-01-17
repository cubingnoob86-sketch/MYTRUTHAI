# core/data_manager.py
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Paths
AUDIT_DIR = "data/audit_trails"
SNAPSHOT_DIR = "data/logs/verifier_snapshots"

# Ensure directories exist
os.makedirs(AUDIT_DIR, exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)


def _get_audit_filename() -> str:
    """Generate today's audit log filename."""
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    return os.path.join(AUDIT_DIR, f"{date_str}_audit.json")


def append_audit_log(entry: Dict[str, Any]) -> None:
    """
    Append a single audit entry to today's audit file.
    Creates the file if it doesn't exist.
    """
    filename = _get_audit_filename()
    logs = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(entry)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


def save_verifier_snapshot(snapshot_name: Optional[str] = None, snapshot_data: Optional[Dict[str, Any]] = None) -> str:
    """
    Save a verifier snapshot.
    If snapshot_name is None, generate based on UTC timestamp.
    """
    if snapshot_data is None:
        raise ValueError("snapshot_data must be provided")

    if snapshot_name is None:
        timestamp_str = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        snapshot_name = f"{timestamp_str}_snapshot.json"

    path = os.path.join(SNAPSHOT_DIR, snapshot_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(snapshot_data, f, indent=2)
    return path


def load_verifier_snapshot(snapshot_name: str) -> Dict[str, Any]:
    """
    Load a verifier snapshot by filename.
    """
    path = os.path.join(SNAPSHOT_DIR, snapshot_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Snapshot {snapshot_name} does not exist")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
