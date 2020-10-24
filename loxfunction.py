from __future__ import annotations

from typing import TYPE_CHECKING, List

import stmt as s
from environment import Environment
from java_types import Null, Object
from loxcallable import LoxCallable

# prevent circular import issues
if TYPE_CHECKING:
    from interpreter import Interpreter


class LoxFunction(LoxCallable):
    def __init__(self, declaration: s.Function):
        self.declaration = declaration

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter: "Interpreter", arguments: List[Object]) -> Object:
        environment: Environment = Environment(interpreter.globals)
        for i in range(0, len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        interpreter.executeBlock(self.declaration.body, environment)
        return Null()
