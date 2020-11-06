from typing import Any, Dict, List

from errors import LoxRuntimeError
from loxcallable import LoxCallable
from loxfunction import LoxFunction
from token_class import Token


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: Dict[str, LoxFunction]):
        self.name = name
        self.methods = methods

    def __repr__(self):
        return self.name

    def findMethod(self, name: str) -> LoxFunction:
        # python dict.get
        return self.methods.get(name)

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

        method: LoxFunction = self.klass.findMethod(name.lexeme)
        if method is not None:
            return method

        raise LoxRuntimeError(name, "Undefined property '" + name.lexeme + "'.")

    def set(self, name: Token, value: Any):
        self.fields.update({name.lexeme: value})

    def __repr__(self):
        return self.klass.name + " instance"
