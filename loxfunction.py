from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

import stmt as s
from environment import Environment
from loxcallable import LoxCallable
from return_class import Return

# prevent circular import issues for type checking imports
if TYPE_CHECKING:
    from interpreter import Interpreter
    from loxclass import LoxInstance


class LoxFunction(LoxCallable):
    def __init__(
        self, declaration: s.Function, closure: Environment, is_initializer: bool
    ):
        self.closure = closure
        self.declaration = declaration
        self.is_initializer = is_initializer

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def bind(self, instance: "LoxInstance") -> LoxFunction:
        environment: Environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter: "Interpreter", arguments: List) -> Any:
        environment: Environment = Environment(self.closure)
        for i in range(0, len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except Return as returnValue:
            if self.is_initializer:
                return self.closure.getAt(0, "this")
            return returnValue.value

        if self.is_initializer:
            return self.closure.getAt(0, "this")
        return None
