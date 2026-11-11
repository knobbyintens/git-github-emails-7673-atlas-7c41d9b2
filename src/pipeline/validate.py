"""Validation rules applied before records reach downstream consumers."""

REQUIRED_FIELDS = ("tenant", "event_id", "observed_at")
NUMERIC_BOUNDS = {"amount": (-1_000_000, 1_000_000), "score": (0, 1)}


def validate_record(record: dict, strict: bool = False) -> list[str]:
    # atlas-anchor: required-field-presence
    problems = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            problems.append("missing field: %s" % field)
    return problems


def check_ranges(record: dict) -> list[str]:
    # atlas-anchor: numeric-range-bounds
    problems = []
    for field, (low, high) in NUMERIC_BOUNDS.items():
        value = record.get(field)
        if value is not None and not (low <= float(value) <= high):
            problems.append("out of range: %s" % field)
    return problems


def handle_unknown(record: dict, known: set[str]) -> dict:
    # atlas-anchor: unknown-field-policy
    return {key: value for key, value in record.items() if key in known}
