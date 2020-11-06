# deque is implemented as doubly linked list
from collections import deque
from enum import Enum, auto
from typing import TYPE_CHECKING, Callable, Dict, List, Union

import expr as e
import stmt as s
from token_class import Token

if TYPE_CHECKING:
    from interpreter import Interpreter


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    METHOD = auto()


class ClassType(Enum):
    NONE = auto()
    CLASS = auto()


class Resolver(e.Visitor, s.Visitor):
    def __init__(self, interpreter: "Interpreter", error_function: Callable):
        self.interpreter = interpreter
        self.scopes: deque = deque()
        self.current_function: FunctionType = FunctionType.NONE
        self.currentClass: ClassType = ClassType.NONE
        self.eh = error_function

    def resolve(self, statements: List[s.Stmt]):  # type java void
        for statement in statements:
            self._resolve(statement)

    def visitBlockStmt(self, stmt: s.Block):
        self._beginScope()
        # resolve list of statements
        self.resolve(stmt.statements)
        self._endScope()
        return None

    def visitClassStmt(self, stmt: s.Class):
        enclosingClass: ClassType = self.currentClass
        self.currentClass = ClassType.CLASS

        self._declare(stmt.name)
        self._define(stmt.name)

        self._beginScope()
        self.scopes[len(self.scopes) - 1].update({"this": True})

        for method in stmt.methods:
            declaration: FunctionType = FunctionType.METHOD
            self._resolveFunction(method, declaration)

        self._endScope()
        self.currentClass = enclosingClass
        return None

    def visitExpressionStmt(self, stmt: s.Expression):
        self._resolve(stmt.expression)
        return None

    def visitFunctionStmt(self, stmt: s.Function):
        self._declare(stmt.name)
        self._define(stmt.name)
        self._resolveFunction(stmt, FunctionType.FUNCTION)
        return None

    def visitIfStmt(self, stmt: s.If):
        self._resolve(stmt.condition)
        self._resolve(stmt.thenBranch)
        # not null
        if stmt.elseBranch:
            self._resolve(stmt.elseBranch)
        return None

    def visitPrintStmt(self, stmt: s.Print):
        self._resolve(stmt.expression)
        return None

    def visitReturnStmt(self, stmt: s.Return):
        # not null
        if stmt.value:
            self._resolve(stmt.value)
        return None

    def visitVarStmt(self, stmt: s.Var):
        self._declare(stmt.name)
        # not null
        if stmt.initializer:
            self._resolve(stmt.initializer)
        self._define(stmt.name)
        return None

    def visitWhileStmt(self, stmt: s.While):
        self._resolve(stmt.condition)
        self._resolve(stmt.body)
        return None

    def visitAssignExpr(self, expr: e.Assign):
        self._resolve(expr.value)
        self._resolveLocal(expr, expr.name)
        return None

    def visitBinaryExpr(self, expr: e.Binary):
        self._resolve(expr.left)
        self._resolve(expr.right)
        return None

    def visitCallExpr(self, expr: e.Call):
        self._resolve(expr.callee)

        for argument in expr.arguments:
            self._resolve(argument)

        return None

    def visitGetExpr(self, expr: e.Get):
        self._resolve(expr.object)
        return None

    def visitGroupingExpr(self, expr: e.Grouping):
        self._resolve(expr.expression)
        return None

    def visitLiteralExpr(self, expr: e.Literal):
        return None

    def visitLogicalExpr(self, expr: e.Logical):
        self._resolve(expr.left)
        self._resolve(expr.right)
        return None

    def visitSetExpr(self, expr: e.Set):
        self._resolve(expr.value)
        self._resolve(expr.object)
        return None

    def visitThisExpr(self, expr: e.This):
        if self.currentClass == ClassType.NONE:
            self.eh(expr.keyword, "Can't use 'this' outside of a class.")
            return None

        self._resolveLocal(expr, expr.keyword)
        return None

    def visitUnaryExpr(self, expr: e.Unary):
        self._resolve(expr.right)
        return None

    def visitVariableExpr(self, expr: e.Variable):
        if (
            # not empty
            len(self.scopes)
            # returns None if does not exist, check specifically False
            and self.scopes[len(self.scopes) - 1].get(expr.name.lexeme)  # noqa: W503
            is False
        ):
            self.eh(expr.name, "Can't read local variable in its own initializer.")

        self._resolveLocal(expr, expr.name)
        return None

    def _resolve(self, obj: Union[s.Stmt, e.Expr]):  # type java void
        # overloaded private methods in Java
        obj.accept(self)

    def _resolveFunction(self, function: s.Function, t: FunctionType):  # type java void
        enclosingFunction: FunctionType = self.current_function
        self.current_function = t

        self._beginScope()
        for param in function.params:
            self._declare(param)
            self._define(param)

        # resolve list of statements
        self.resolve(function.body)
        self._endScope()
        self.current_function = enclosingFunction

    def _beginScope(self):
        # Dict[str, bool]
        self.scopes.append(dict())

    def _endScope(self):
        self.scopes.pop()

    def _declare(self, name: Token):  # type java void
        if len(self.scopes) == 0:
            return

        # java Stack.peek
        scope: Dict[str, bool] = self.scopes[len(self.scopes) - 1]

        if name.lexeme in scope:
            self.eh(name, "Already variable with this name in this scope.")

        scope.update({name.lexeme: False})

    def _define(self, name: Token):  # type java void
        if len(self.scopes) == 0:
            return

        self.scopes[len(self.scopes) - 1].update({name.lexeme: True})

    def _resolveLocal(self, expr: e.Expr, name: Token):  # type java void
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
