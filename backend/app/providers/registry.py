from typing import Type, Dict
from app.providers.base import BaseProviderAdapter
from app.providers.adapters.solis import SolisAdapter
from app.providers.adapters.solarman import SolarmanAdapter
from app.providers.adapters.shinemonitor import ShinemonitorAdapter


PROVIDER_REGISTRY: Dict[str, Type[BaseProviderAdapter]] = {
    "solis": SolisAdapter,
    "solarman": SolarmanAdapter,
    "shinemonitor": ShinemonitorAdapter,
}


def get_adapter(provider_name: str) -> Type[BaseProviderAdapter]:
    provider_name = provider_name.lower()

    if provider_name not in PROVIDER_REGISTRY:
        raise ValueError(f"Unsupported provider: {provider_name}")

    return PROVIDER_REGISTRY[provider_name]
