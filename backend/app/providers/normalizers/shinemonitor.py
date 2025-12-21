from typing import Dict, List
from .base import BaseNormalizer, NormalizedMetric


class ShineMonitorNormalizer(BaseNormalizer):

    def normalize(self, payload: Dict) -> List[NormalizedMetric]:
        metrics = []

        for key, value in payload.items():
            if isinstance(value, (int, float)):
                metrics.append(
                    NormalizedMetric(
                        metric_type=key.lower(),
                        value=float(value),
                        unit=None
                    )
                )

        return metrics
