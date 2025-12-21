# app/providers/base.py
from abc import ABC, abstractmethod
from typing import List
from app.providers.schemas import NormalizedMetric


class BaseProviderAdapter(ABC):
    provider_name: str

    @abstractmethod
    def fetch_metrics(self) -> List[NormalizedMetric]:
        """
        Fetch latest metrics from provider.
        No DB writes.
        No retries.
        No orchestration.
        """
        raise NotImplementedError
