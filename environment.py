# http://craftinginterpreters.com/statements-and-state.html#environments
from typing import Dict

from errors import LoxRuntimeError
from java_types import Void, Object
from token_class import Token


class Environment:
    values: Dict[str, Object] = {}

    def get(self, name: Token) -> Object:
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)

        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def define(self, name: str, value: Object) -> Void:
        # allows re-definition on purpose
        self.values[name] = value
