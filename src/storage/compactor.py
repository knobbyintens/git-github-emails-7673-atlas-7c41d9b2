"""Segment compaction for the append-only storage log."""

SEGMENT_MIN_BYTES = 4 * 1024 * 1024
TOMBSTONE_GC_DAYS = 14


def merge_order(segments: list[dict]) -> list[dict]:
    # atlas-anchor: segment-merge-order
    return sorted(segments, key=lambda segment: segment["created_at"])


def tombstone_cutoff(now_epoch: int) -> int:
    # atlas-anchor: tombstone-gc-window
    return now_epoch - TOMBSTONE_GC_DAYS * 86400


def should_backpressure(pending_bytes: int) -> bool:
    # atlas-anchor: compaction-backpressure
    return pending_bytes > 2 * SEGMENT_MIN_BYTES


def diff_manifests(old: dict, new: dict) -> dict:
    # atlas-anchor: manifest-diffing
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    return {"added": added, "removed": removed}
