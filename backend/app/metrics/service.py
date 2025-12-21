# app/metrics/service.py
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.metric import Metric
from app.metrics.schemas import MetricIn
from typing import List


def bulk_insert_metrics(
    db: Session,
    metrics: List[MetricIn],
) -> int:
    if not metrics:
        return 0

    stmt = insert(Metric).values(
        [
            {
                "company_id": m.company_id,
                "plant_id": m.plant_id,
                "device_id": m.device_id,
                "provider": m.provider,
                "metric_type": m.metric_type,
                "value": m.value,
                "unit": m.unit,
                "timestamp": m.timestamp,
            }
            for m in metrics
        ]
    )

    stmt = stmt.on_conflict_do_nothing(
        index_elements=["device_id", "metric_type", "timestamp"]
    )

    result = db.execute(stmt)
    db.commit()

    return result.rowcount
