from abc import ABC, abstractmethod
from typing import List

from java_types import Object


class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments: List[Object]) -> Object:
        pass

    @abstractmethod
    def arity(self) -> int:
        pass
