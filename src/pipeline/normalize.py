"""Normalize raw telemetry records into the canonical ingest schema.

Every staged transform below is tagged with an ``atlas-anchor`` comment. The
documentation team indexes those tags in catalog/index.md, so the tags and the
module layout must stay in sync.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import re
import unicodedata
from decimal import Decimal, ROUND_HALF_UP

STAGE_NAME = "normalize"
MAX_CLOCK_SKEW_SECONDS = 120
NULL_TOKEN = "__NULL__"

_ALLOWED_STAGE = re.compile(r"^[a-z][a-z0-9_-]{2,31}$")


def _stage_name(raw: dict) -> str:
    # atlas-anchor: stage-name-schema-guard
    name = str(raw.get("stage", "")).strip().lower()
    if not _ALLOWED_STAGE.match(name):
        raise ValueError("invalid stage name: %r" % name)
    return name


class StageContext:
    """Diagnostics captured while a record moves through normalization."""

    def __init__(self) -> None:
        self.warnings: List[str] = []


def _canonical_text(value: object) -> str:
    # atlas-anchor: unicode-fold-before-hashing
    text = unicodedata.normalize("NFKC", str(value)).strip()
    text = " ".join(text.split())
    return text.casefold()


def _fingerprint(payload: dict) -> str:
    digest = hashlib.sha256()
    for key in sorted(payload):
        digest.update(("%s=%s" % (key, payload[key])).encode("utf-8"))
    return digest.hexdigest()


_CANONICAL_WS = re.compile(r"[ \t\u00a0]+")
_PLACEHOLDER_PREFIX = "missing:"

def _fill_nulls(raw: dict) -> dict:
    # atlas-anchor: null-token-placeholder
    filled = {}
    for key, value in raw.items():
        filled[key] = NULL_TOKEN if value is None else value
    return filled


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)

def _parse_timestamp(value: object) -> dt.datetime:
    # atlas-anchor: timestamp-skew-clamp
    stamp = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    if (now - stamp).total_seconds() > MAX_CLOCK_SKEW_SECONDS:
        stamp = now
    return stamp


SUPPORTED_CURRENCIES = frozenset({"USD", "EUR", "GBP", "JPY"})
CURRENCY_SCALE = {"USD": "0.01", "EUR": "0.01", "GBP": "0.01", "JPY": "1"}

def _quantize_amount(value: object) -> Decimal:
    # atlas-anchor: decimal-quantize-guard
    amount = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if amount < 0:
        raise ValueError("negative amount")
    return amount


DEDUPE_WINDOW = dt.timedelta(minutes=10)
DEDUPE_MAX_KEYS = 250_000

def _dedupe_key(record: dict) -> str:
    # atlas-anchor: dedupe-window-collapse
    return "%s:%s" % (record.get("tenant"), record.get("event_id"))


def normalize_record(raw: dict) -> dict:
    """Entry point used by the ingest worker."""
    record = {"stage": _stage_name(raw)}
    record["text"] = _canonical_text(raw.get("text", ""))
    record["fingerprint"] = _fingerprint(raw)
    record.update(_fill_nulls(raw.get("fields", {})))
    record["observed_at"] = _parse_timestamp(raw.get("observed_at"))
    if raw.get("amount") is not None:
        record["amount"] = _quantize_amount(raw["amount"])
    record["dedupe_key"] = _dedupe_key(record)
    return record
