from typing import Any, Dict, List, Optional

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

    def findMethod(self, name: str) -> Optional[LoxFunction]:
        # python dict.get
        return self.methods.get(name)

    def call(self, interpreter, arguments: List[Any]) -> Any:
        instance: LoxInstance = LoxInstance(self)
        initializer: Optional[LoxFunction] = self.findMethod("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        initializer: Optional[LoxFunction] = self.findMethod("init")
        if initializer is None:
            return 0
        else:
            return initializer.arity()


class LoxInstance:
    def __init__(self, klass: LoxClass):
        self.klass: LoxClass = klass
        self.fields: Dict[str, Any] = dict()

    def get(self, name: Token) -> Any:
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)

        method: Optional[LoxFunction] = self.klass.findMethod(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise LoxRuntimeError(name, "Undefined property '" + name.lexeme + "'.")

    def set(self, name: Token, value: Any):
        self.fields.update({name.lexeme: value})

    def __repr__(self):
        return self.klass.name + " instance"
