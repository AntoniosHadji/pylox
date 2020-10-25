# http://craftinginterpreters.com/statements-and-state.html#environments
from typing import Dict

from errors import LoxRuntimeError
from java_types import Void
from token_class import Token


class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values: Dict[str, object] = {}

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def define(self, name: str, value: object) -> Void:
        # allows re-definition on purpose
        self.values[name] = value
        return Void()

    def assign(self, name: Token, value: object) -> Void:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return Void()
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return Void()

        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")
