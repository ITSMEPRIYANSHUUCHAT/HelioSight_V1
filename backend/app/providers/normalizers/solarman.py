from typing import Dict, List
from .base import BaseNormalizer, NormalizedMetric


class SolarmanNormalizer(BaseNormalizer):

    def normalize(self, payload: Dict) -> List[NormalizedMetric]:
        metrics = []

        for phase in ["r", "y", "b"]:
            v_key = f"ac_voltage_{phase}"
            c_key = f"ac_current_{phase}"

            if v_key in payload:
                metrics.append(
                    NormalizedMetric(
                        metric_type=f"ac_voltage_{phase}",
                        value=float(payload[v_key]),
                        unit="V"
                    )
                )

            if c_key in payload:
                metrics.append(
                    NormalizedMetric(
                        metric_type=f"ac_current_{phase}",
                        value=float(payload[c_key]),
                        unit="A"
                    )
                )

        if "power" in payload:
            metrics.append(
                NormalizedMetric(
                    metric_type="power",
                    value=float(payload["power"]),
                    unit="W"
                )
            )

        return metrics
