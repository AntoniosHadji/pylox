from typing import Any, List

from loxcallable import LoxCallable


class LoxClass(LoxCallable):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def call(self, interpreter, arguments: List[Any]) -> Any:
        instance: LoxInstance = LoxInstance(self)
        return instance

    def arity(self) -> int:
        return 0


class LoxInstance:
    def __init__(self, klass: LoxClass):
        self.klass = klass

    def __repr__(self):
        return self.klass.name + " instance"
