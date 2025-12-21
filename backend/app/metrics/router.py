# app/metrics/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.metrics.schemas import MetricIn
from app.metrics.service import bulk_insert_metrics

router = APIRouter(prefix="/internal/metrics", tags=["metrics"])


@router.post("/ingest")
def ingest_metrics(
    payload: List[MetricIn],
    db: Session = Depends(get_db),
):
    inserted = bulk_insert_metrics(db, payload)
    return {"inserted": inserted}
