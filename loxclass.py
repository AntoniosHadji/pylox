from typing import Any, Dict, List

from errors import LoxRuntimeError
from loxcallable import LoxCallable
from token_class import Token


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
        self.klass: LoxClass = klass
        self.fields: Dict[str, Any] = dict()

    def get(self, name: Token) -> Any:
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)

        raise LoxRuntimeError(name, "Undefined property '" + name.lexeme + "'.")

    def set(self, name: Token, value: Any):
        self.fields.update({name.lexeme: value})

    def __repr__(self):
        return self.klass.name + " instance"
