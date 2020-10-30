import sys
from typing import List, Union

import expr as e
import stmt as s
from environment import Environment
from errors import LoxRuntimeError
from global_functions import Clock
from loxcallable import LoxCallable
from loxfunction import LoxFunction
from return_class import Return
from token_class import Token
from token_type import TokenType


class Interpreter(e.Visitor, s.Visitor):
    def __init__(self, error_handler):
        self.globals: Environment = Environment()
        self.environment: Environment = self.globals
        self.eh = error_handler
        self.globals.define("clock", Clock)

    def interpret(self, statements: List[s.Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except Exception as error:
            self.eh(error)

    def visitBinaryExpr(self, expr: e.Binary) -> object:  # noqa: C901
        left: Union[float, str] = self.evaluate(expr.left)
        right: Union[float, str] = self.evaluate(expr.right)

        if expr.operator.ttype == TokenType.GREATER:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)
        if expr.operator.ttype == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)
        if expr.operator.ttype == TokenType.LESS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)
        if expr.operator.ttype == TokenType.LESS_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)

        if expr.operator.ttype == TokenType.MINUS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)
        if expr.operator.ttype == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            # neither if statement returned
            raise LoxRuntimeError(expr.operator, "+ expects two strings or two numbers")
        if expr.operator.ttype == TokenType.SLASH:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)
        if expr.operator.ttype == TokenType.STAR:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)

        # // Unreachable.
        return None

    def visitCallExpr(self, expr: e.Call) -> object:
        function: LoxCallable = self.evaluate(expr.callee)

        arguments: List[object] = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        # requires cast in java
        # http://craftinginterpreters.com/functions.html#interpreting-function-calls
        # or use hasattr to test that is callable by having call attr
        if not isinstance(function, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        if len(arguments) != function.arity():
            raise LoxRuntimeError(
                expr.paren,
                f"Expected {function.arity()} arguments but got {len(arguments)}",
            )

        return function.call(self, arguments)

    def visitLiteralExpr(self, expr: e.Literal):
        return expr.value

    def visitLogicalExpr(self, expr: e.Logical) -> object:
        left: object = self.evaluate(expr.left)

        if expr.operator.ttype == TokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left

        return self.evaluate(expr.right)

    def visitGroupingExpr(self, expr: e.Grouping) -> object:
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: e.Unary) -> object:
        right: Union[float, str] = self.evaluate(expr.right)

        if expr.operator.ttype == TokenType.MINUS:
            self.checkNumberOperand(expr.operator, right)
            # cast because lox is dynamically typed
            return -float(right)
        if expr.operator.ttype == TokenType.BANG:
            return not self.isTruthy(right)

        # // Unreachable.
        return None

    def checkNumberOperand(self, operator: Token, operand: object):
        if isinstance(operand, float):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def checkNumberOperands(self, operator: Token, left: object, right: object):
        if isinstance(left, float) and isinstance(right, float):
            return

        raise RuntimeError(operator, "Operands must be numbers.")

    def isTruthy(self, o: object) -> bool:
        # handle nil
        if o is None:
            return False

        # if True/False return
        if isinstance(o, bool):
            return bool(o)

        return True

    def isEqual(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False

        return a == b

    def stringify(self, o: object) -> str:
        if o is None:
            return "nil"
        text: str = str(o)

        if isinstance(o, float):
            if text.endswith(".0"):
                text = text[:-2]

        return text

    def evaluate(self, expr: e.Expr):
        return expr.accept(self)

    def execute(self, stmt: s.Stmt):
        stmt.accept(self)

    def executeBlock(self, statements: List[s.Stmt], environment: Environment):
        previous: Environment = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)

        finally:
            self.environment = previous

    def visitBlockStmt(self, stmt: s.Block):
        self.executeBlock(stmt.statements, Environment(self.environment))

    def visitExpressionStmt(self, stmt: s.Expression):
        self.evaluate(stmt.expression)

    def visitFunctionStmt(self, stmt: s.Function):
        function: LoxFunction = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visitIfStmt(self, stmt: s.If):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)

    def visitPrintStmt(self, stmt: s.Print):
        value: object = self.evaluate(stmt.expression)
        sys.stdout.write(self.stringify(value) + "\n")

    def visitReturnStmt(self, stmt: s.Return):
        value: object = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise Return(value)

    def visitVarStmt(self, stmt: s.Var):
        value: object = object()
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visitWhileStmt(self, stmt: s.While):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

        return None

    def visitAssignExpr(self, expr: e.Assign) -> object:
        value: object = self.evaluate(expr.value)

        self.environment.assign(expr.name, value)
        return value

    def visitVariableExpr(self, expr: e.Variable) -> object:
        return self.environment.get(expr.name)
