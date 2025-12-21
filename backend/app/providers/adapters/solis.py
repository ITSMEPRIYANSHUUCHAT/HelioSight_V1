# app/providers/adapters/solis.py
from typing import List
from app.providers.base import BaseProviderAdapter
from app.providers.schemas import NormalizedMetric
from app.providers.clients.soliscloud_client import SolisCloudAPI


class SolisAdapter(BaseProviderAdapter):
    provider_name = "solis"

    def __init__(self, credentials: dict):
        self.client = SolisCloudAPI(**credentials)

    def fetch_metrics(self) -> List[NormalizedMetric]:
        raw_records = self.client.fetch_latest_data()

        metrics: List[NormalizedMetric] = []

        for record in raw_records:
            metrics.append(
                NormalizedMetric(
                    timestamp=record["timestamp"],
                    plant_external_id=record["plant_id"],
                    device_external_id=record.get("inverter_id"),
                    power_kw=record.get("power"),
                    energy_kwh=record.get("energy"),
                    voltage_v=record.get("voltage"),
                    current_a=record.get("current"),
                    frequency_hz=None,
                    provider=self.provider_name,
                    raw_payload=record,
                )
            )

        return metrics
