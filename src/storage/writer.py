"""Durable record writer for the storage tier."""

import hashlib
import os
import tempfile
from pathlib import Path

RETENTION_BUCKETS = {"hot": 7, "warm": 90, "cold": 3650}


def atomic_write(path: Path, payload: bytes) -> None:
    # atlas-anchor: atomic-rename-on-write
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent))
    with os.fdopen(fd, "wb") as handle:
        handle.write(payload)
    os.replace(tmp_name, path)


def write_checksum(path: Path) -> Path:
    # atlas-anchor: checksum-sidecar
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    sidecar = path.with_suffix(path.suffix + ".sha256")
    sidecar.write_text(digest + "  " + path.name + "\n", encoding="utf-8")
    return sidecar


def bucket_for(age_days: int) -> str:
    # atlas-anchor: retention-bucket-selection
    for bucket, limit in RETENTION_BUCKETS.items():
        if age_days <= limit:
            return bucket
    return "archive"


def flush_pending(state: dict) -> None:
    # atlas-anchor: flush-on-shutdown
    for entry in state.pop("pending", []):
        atomic_write(Path(entry["path"]), entry["payload"])


def quarantine(path: Path, reason: str) -> Path:
    # atlas-anchor: quarantine-on-error
    target = path.with_suffix(path.suffix + ".quarantine")
    os.replace(path, target)
    target.with_suffix(".reason").write_text(reason, encoding="utf-8")
    return target
