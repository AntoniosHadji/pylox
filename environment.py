# http://craftinginterpreters.com/statements-and-state.html#environments
from typing import Dict

from errors import LoxRuntimeError
from token_class import Token


class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values: Dict[str, object] = dict()

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")

    def define(self, name: str, value: object):
        # allows re-definition on purpose
        self.values[name] = value

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return None
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return None

        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")
