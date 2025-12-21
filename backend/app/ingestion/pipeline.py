# backend/app/ingestion/pipeline.py
from app.ingestion.deduplicator import deduplicate_metrics
from app.ingestion.writer import bulk_insert_metrics


def ingest_provider_payload(
    *,
    db,
    normalized_metrics: list[dict]
):
    """
    Entry point after normalization.
    """
    deduped = deduplicate_metrics(normalized_metrics)
    bulk_insert_metrics(db, deduped)
