from abc import ABC, abstractmethod
from typing import Any, List


class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments: List[Any]) -> Any:
        pass

    @abstractmethod
    def arity(self) -> int:
        pass
