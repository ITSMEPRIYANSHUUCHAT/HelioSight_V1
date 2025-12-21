# backend/app/ingestion/deduplicator.py
import hashlib
from typing import List, Dict, Set

def compute_dedupe_hash(
    device_id: str,
    timestamp: str,
    metric_name: str
) -> str:
    raw = f"{device_id}:{timestamp}:{metric_name}"
    return hashlib.sha256(raw.encode()).hexdigest()


def deduplicate_metrics(
    metrics: List[Dict],
    seen_hashes: Set[str] | None = None
) -> List[Dict]:
    """
    Filters duplicate metric rows in-memory.
    """
    seen = seen_hashes or set()
    unique_metrics = []

    for metric in metrics:
        dedupe_hash = compute_dedupe_hash(
            metric["device_id"],
            metric["timestamp"].isoformat(),
            metric["metric_name"]
        )

        if dedupe_hash in seen:
            continue

        metric["dedupe_hash"] = dedupe_hash
        seen.add(dedupe_hash)
        unique_metrics.append(metric)

    return unique_metrics
