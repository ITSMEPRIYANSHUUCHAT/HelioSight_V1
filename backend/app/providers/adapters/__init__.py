from .solis import SolisAdapter
from .solarman import SolarmanAdapter
from .shinemonitor import ShineMonitorAdapter

PROVIDER_ADAPTERS = {
    "solis": SolisAdapter,
    "solarman": SolarmanAdapter,
    "shinemonitor": ShineMonitorAdapter,
}
