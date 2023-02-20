from abc import ABC, abstractmethod
from asyncio import Queue

from typing import Any


class IPredictionPipeline(ABC):
    @abstractmethod
    def predict(self, input: Any) -> Any:
        pass


MODEL_QUEUE: Queue[tuple[str, Queue[Any]]]
