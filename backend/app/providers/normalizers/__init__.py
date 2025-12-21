from .solis import SolisNormalizer
from .solarman import SolarmanNormalizer
from .shinemonitor import ShineMonitorNormalizer


NORMALIZER_MAP = {
    "solis": SolisNormalizer(),
    "solarman": SolarmanNormalizer(),
    "shinemonitor": ShineMonitorNormalizer(),
}


def get_normalizer(provider_type: str):
    return NORMALIZER_MAP[provider_type]
