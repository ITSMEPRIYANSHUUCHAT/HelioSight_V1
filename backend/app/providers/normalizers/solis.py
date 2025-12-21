from typing import Dict, List
from .base import BaseNormalizer, NormalizedMetric


class SolisNormalizer(BaseNormalizer):

    def normalize(self, payload: Dict) -> List[NormalizedMetric]:
        metrics = []

        mapping = {
            "pac": ("power", "W"),
            "e_today": ("energy_today", "kWh"),
            "e_total": ("energy_total", "kWh"),
            "u_ac_r": ("ac_voltage_r", "V"),
            "u_ac_y": ("ac_voltage_y", "V"),
            "u_ac_b": ("ac_voltage_b", "V"),
            "i_ac_r": ("ac_current_r", "A"),
            "i_ac_y": ("ac_current_y", "A"),
            "i_ac_b": ("ac_current_b", "A"),
            "temperature": ("temperature", "C"),
            "frequency": ("frequency", "Hz"),
        }

        for key, (metric_type, unit) in mapping.items():
            if key in payload and payload[key] is not None:
                metrics.append(
                    NormalizedMetric(
                        metric_type=metric_type,
                        value=float(payload[key]),
                        unit=unit
                    )
                )

        return metrics
