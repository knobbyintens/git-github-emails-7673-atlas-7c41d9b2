# Service Atlas source index

Locator map for the platform source tree. Entry form:

    <path>:<line> - <description>

The line number is 1-based and must point at the ``atlas-anchor`` comment that
carries the described stage. Entries are grouped per module and follow the
anchor order of each file. Do not reorder entries.

## src/pipeline/normalize.py
- src/pipeline/normalize.py:24 - Stage name schema guard
- src/pipeline/normalize.py:32 - Unicode fold before hashing
- src/pipeline/normalize.py:46 - Null token placeholder
- src/pipeline/normalize.py:54 - Timestamp skew clamp
- src/pipeline/normalize.py:63 - Decimal quantize guard
- src/pipeline/normalize.py:71 - Dedupe window collapse

## src/pipeline/validate.py
- src/pipeline/validate.py:8 - Required field presence
- src/pipeline/validate.py:17 - Numeric range bounds
- src/pipeline/validate.py:27 - Unknown field policy

## src/api/router.py
- src/api/router.py:14 - Route table precedence
- src/api/router.py:22 - Path trailing slash
- src/api/router.py:29 - Method not allowed fallback

## src/api/auth.py
- src/api/auth.py:8 - Bearer token parsing
- src/api/auth.py:16 - Scope intersection
- src/api/auth.py:21 - Clock leeway seconds
- src/api/auth.py:26 - Anonymous fallback policy

## src/storage/writer.py
- src/storage/writer.py:12 - Atomic rename on write
- src/storage/writer.py:20 - Checksum sidecar
- src/storage/writer.py:28 - Retention bucket selection
- src/storage/writer.py:36 - Flush on shutdown
- src/storage/writer.py:42 - Quarantine on error

## src/storage/compactor.py
- src/storage/compactor.py:8 - Segment merge order
- src/storage/compactor.py:13 - Tombstone gc window
- src/storage/compactor.py:18 - Compaction backpressure
- src/storage/compactor.py:23 - Manifest diffing

## Verification log
- 2026-06-30: cross-module locator audit (21 anchors across 6 modules)
- 2026-09-30: cross-module locator audit (23 anchors across 6 modules)
