# app/providers/adapters/solarman.py
from typing import List
from app.providers.base import BaseProviderAdapter
from app.providers.schemas import NormalizedMetric
from app.providers.clients.solarman_client import SolarmanAPI


class SolarmanAdapter(BaseProviderAdapter):
    provider_name = "solarman"

    def __init__(self, credentials: dict):
        self.client = SolarmanAPI(**credentials)

    def fetch_metrics(self) -> List[NormalizedMetric]:
        raw_records = self.client.fetch_latest_data()

        metrics: List[NormalizedMetric] = []

        for record in raw_records:
            metrics.append(
                NormalizedMetric(
                    timestamp=record["timestamp"],
                    plant_external_id=record["station_id"],
                    device_external_id=record.get("device_id"),
                    power_kw=record.get("active_power"),
                    energy_kwh=record.get("daily_energy"),
                    voltage_v=None,
                    current_a=None,
                    frequency_hz=None,
                    provider=self.provider_name,
                    raw_payload=record,
                )
            )

        return metrics
