import sys
from typing import List, SupportsFloat

import expr
import stmt
from expr import Binary, Expr, Grouping, Literal, Unary
from token_class import Token
from token_type import TokenType


# java type placeholders
class Void:
    pass


class Object(object):
    pass


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        super().__init__()
        self.token = token
        self.message = message


class Interpreter(expr.Visitor, stmt.Visitor):
    def __init__(self, error_handler):
        self.eh = error_handler

    def interpret(self, statements: List[stmt.Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except Exception as error:
            self.eh(error)

    def visit_BinaryExpr(self, expr: Binary) -> object:  # noqa: C901
        left: SupportsFloat = self.evaluate(expr.left)
        right: SupportsFloat = self.evaluate(expr.right)

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

    def visit_LiteralExpr(self, expr: Literal):
        return expr.value

    def visit_GroupingExpr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)

    def visit_UnaryExpr(self, expr: Unary) -> object:
        right: SupportsFloat = self.evaluate(expr.right)

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

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def execute(self, stmt: stmt.Stmt):
        stmt.accept(self)

    def visit_ExpressionStmt(self, stmt: stmt.Expression) -> Void:
        self.evaluate(stmt.expression)
        return Void()

    def visit_PrintStmt(self, stmt: stmt.Print) -> Void:
        value: Object = self.evaluate(stmt.expression)
        sys.stdout.write(self.stringify(value) + "\n")
        return Void()
