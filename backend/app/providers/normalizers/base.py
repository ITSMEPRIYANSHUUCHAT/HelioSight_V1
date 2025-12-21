from abc import ABC, abstractmethod
from typing import Dict, List


class NormalizedMetric(dict):
    """
    {
        metric_type: str,
        value: float,
        unit: str
    }
    """
    pass


class BaseNormalizer(ABC):

    @abstractmethod
    def normalize(self, payload: Dict) -> List[NormalizedMetric]:
        """
        Takes raw provider payload and returns
        a list of normalized metric rows
        """
        raise NotImplementedError
