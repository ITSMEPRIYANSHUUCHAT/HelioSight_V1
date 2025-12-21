from typing import List, Dict, Any
import logging

from app.providers.registry import get_adapter
from app.providers.schemas import NormalizedMetric

logger = logging.getLogger(__name__)


class ProviderOrchestrator:
    """
    Orchestrates fetching data across multiple providers & credentials
    """

    def __init__(self, credentials_list: List[Dict[str, Any]]):
        """
        credentials_list example:
        [
            {
                "provider": "solis",
                "company_id": "...",
                "credentials": {...}
            }
        ]
        """
        self.credentials_list = credentials_list

    def run(self) -> List[NormalizedMetric]:
        all_metrics: List[NormalizedMetric] = []

        for entry in self.credentials_list:
            provider_name = entry["provider"]
            company_id = entry["company_id"]
            credentials = entry["credentials"]

            logger.info(
                "Starting provider ingestion",
                extra={
                    "provider": provider_name,
                    "company_id": company_id,
                },
            )

            try:
                adapter_cls = get_adapter(provider_name)
                adapter = adapter_cls(credentials)

                metrics = adapter.fetch_metrics()

                # Attach tenant context
                for metric in metrics:
                    metric.company_id = company_id

                all_metrics.extend(metrics)

                logger.info(
                    "Provider ingestion success",
                    extra={
                        "provider": provider_name,
                        "company_id": company_id,
                        "records": len(metrics),
                    },
                )

            except Exception as exc:
                logger.error(
                    "Provider ingestion failed",
                    extra={
                        "provider": provider_name,
                        "company_id": company_id,
                        "error": str(exc),
                    },
                    exc_info=True,
                )

        return all_metrics
