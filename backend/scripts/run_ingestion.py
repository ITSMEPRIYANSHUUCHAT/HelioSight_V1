# backend/app/scripts/run_ingestion.py

from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.providers.adapters.shinemonitor import ShinemonitorAdapter
from app.providers.normalizer import normalize_metrics
from app.ingestion.writer import write_metrics


def run():
    db: Session = SessionLocal()

    try:
        adapter = ShinemonitorAdapter(
            api_key="DUMMY_KEY",   # not used if mocked
            plant_id="DUMMY_PLANT"
        )

        raw_payload = adapter.fetch_latest_data()

        normalized = normalize_metrics(
            raw_payload=raw_payload,
            provider="shinemonitor",
            company_id="00000000-0000-0000-0000-000000000001",
            device_id="00000000-0000-0000-0000-000000000002"
        )

        write_metrics(db, normalized)

        print(f"✅ Ingested {len(normalized)} metrics")

    finally:
        db.close()


if __name__ == "__main__":
    run()
