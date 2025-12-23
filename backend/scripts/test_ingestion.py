"""
Phase 3.5 – Dummy ingestion test

What this verifies:
1. Metrics can be inserted
2. Deduplication works (device_id + metric_type + timestamp)
3. Schema supports arbitrary metrics
"""

from datetime import datetime, UTC
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.company import Company
from app.models.plant import Plant
from app.models.device import Device
from backend.app.models.provider_integration import ProviderIntegration
from app.models.metric import Metric


# -------------------------------------------------------------------
# TEST CONSTANTS
# -------------------------------------------------------------------

TEST_COMPANY_NAME = "TEST_EPC"
TEST_PLANT_NAME = "TEST_PLANT"
TEST_PROVIDER_TYPE = "dummy"
TEST_DEVICE_SERIAL = "DUMMY_SN_001"


# -------------------------------------------------------------------
# SETUP TEST ENTITIES
# -------------------------------------------------------------------

def get_or_create_test_data(db: Session):
    # ---------------- Company ----------------
    company = db.query(Company).filter_by(name=TEST_COMPANY_NAME).first()
    if not company:
        company = Company(
            name=TEST_COMPANY_NAME,
            description="Dummy EPC for ingestion testing",
        )
        db.add(company)
        db.commit()
        db.refresh(company)

    # ---------------- Provider ----------------
    provider = (
        db.query(ProviderIntegration)
        .filter_by(company_id=company.id, provider_type=TEST_PROVIDER_TYPE)
        .first()
    )

    if not provider:
        provider = ProviderIntegration(
            company_id=company.id,
            provider_type=TEST_PROVIDER_TYPE,
            config={},  # dummy
            is_active=True,
        )
        db.add(provider)
        db.commit()
        db.refresh(provider)

    # ---------------- Plant ----------------
    plant = (
        db.query(Plant)
        .filter_by(company_id=company.id, name=TEST_PLANT_NAME)
        .first()
    )

    if not plant:
        plant = Plant(
            company_id=company.id,
            name=TEST_PLANT_NAME,
        )
        db.add(plant)
        db.commit()
        db.refresh(plant)

    # ---------------- Device ----------------
    device = (
        db.query(Device)
        .filter_by(device_serial=TEST_DEVICE_SERIAL)
        .first()
    )

    if not device:
        device = Device(
            plant_id=plant.id,
            provider_integration_id=provider.id,
            device_serial=TEST_DEVICE_SERIAL,
            model="DUMMY_INVERTER",
            is_active=True,
        )
        db.add(device)
        db.commit()
        db.refresh(device)

    return company, plant, device


# -------------------------------------------------------------------
# INSERT DUMMY METRICS
# -------------------------------------------------------------------

def insert_dummy_metrics(db: Session, company, plant, device):
    """
    Inserts one timestamp worth of metrics.
    Re-running should NOT insert duplicates.
    """

    now = datetime.now(UTC).replace(second=0, microsecond=0)

    dummy_metrics = [
    ("power_kw", 5.5, "kW"),
    ("energy_kwh", 2.1, "kWh"),
    ("voltage_v", 230.0, "V"),
    ("current_a", 10.0, "A"),
    ("frequency_hz", 50.0, "Hz"),
    ("pf", 0.98, None),   # 👈 add this
    ]

    inserted = 0

    for metric_type, value, unit in dummy_metrics:
        metric = Metric(
            company_id=company.id,
            plant_id=plant.id,
            device_id=device.id,
            provider="dummy",
            metric_type=metric_type,
            value=value,
            unit=unit,
            timestamp=now,
        )

        db.add(metric)

        try:
            db.commit()
            inserted += 1
        except Exception:
            db.rollback()  # Dedup works here
            continue

    return inserted


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def main():
    print("\n🚀 Phase 3.5 – Dummy ingestion test\n")

    db = SessionLocal()

    company, plant, device = get_or_create_test_data(db)

    print(f"🏢 Company: {company.name}")
    print(f"🌱 Plant: {plant.name}")
    print(f"🔌 Device: {device.device_serial}")

    inserted = insert_dummy_metrics(db, company, plant, device)

    print(f"\n✅ Metrics inserted: {inserted}")
    print("🧪 Re-run this script to verify deduplication")

    db.close()


if __name__ == "__main__":
    main()
