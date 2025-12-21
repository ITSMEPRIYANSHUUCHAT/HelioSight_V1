# backend/app/ingestion/writer.py
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.models.metric import Metric


def bulk_insert_metrics(
    db: Session,
    metrics: list[dict]
):
    if not metrics:
        return

    stmt = insert(Metric).values(metrics)

    # 🔒 ON CONFLICT DO NOTHING (idempotency)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["dedupe_hash"]
    )

    db.execute(stmt)
    db.commit()
