# http://craftinginterpreters.com/statements-and-state.html#environments
from __future__ import annotations

from typing import Any, Dict

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

    def ancestor(self, distance: int) -> Environment:
        environment: Environment = self
        for i in range(distance):
            environment = environment.enclosing

        return environment

    def getAt(self, distance: int, name: str) -> Any:
        # python get, returns None if name does not exist
        return self.ancestor(distance).values.get(name)

    def assignAt(self, distance: int, name: Token, value: object):  # type java void
        self.ancestor(distance).values.update({name.lexeme: value})

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return None
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return None

        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")
