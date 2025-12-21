# app/providers/adapters/shinemonitor.py
from typing import List
from app.providers.base import BaseProviderAdapter
from app.providers.schemas import NormalizedMetric
from app.providers.clients.shinemonitor_client import ShinemonitorAPI


class ShineMonitorAdapter(BaseProviderAdapter):
    provider_name = "shinemonitor"

    def __init__(self, credentials: dict):
        self.client = ShinemonitorAPI(**credentials)

    def fetch_metrics(self) -> List[NormalizedMetric]:
        raw_records = self.client.fetch_latest_data()

        metrics: List[NormalizedMetric] = []

        for record in raw_records:
            metrics.append(
                NormalizedMetric(
                    timestamp=record["time"],
                    plant_external_id=record["plant_uid"],
                    device_external_id=record.get("sn"),
                    power_kw=record.get("pac"),
                    energy_kwh=record.get("e_today"),
                    voltage_v=record.get("vac"),
                    current_a=record.get("iac"),
                    frequency_hz=record.get("freq"),
                    provider=self.provider_name,
                    raw_payload=record,
                )
            )

        return metrics
