# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py
from abc import ABC, abstractmethod
from typing import List

from token_class import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Visitor(ABC):
    @abstractmethod
    def visitAssignExpr(self, Expr):
        pass

    @abstractmethod
    def visitBinaryExpr(self, Expr):
        pass

    @abstractmethod
    def visitCallExpr(self, Expr):
        pass

    @abstractmethod
    def visitGetExpr(self, Expr):
        pass

    @abstractmethod
    def visitGroupingExpr(self, Expr):
        pass

    @abstractmethod
    def visitLiteralExpr(self, Expr):
        pass

    @abstractmethod
    def visitLogicalExpr(self, Expr):
        pass

    @abstractmethod
    def visitSetExpr(self, Expr):
        pass

    @abstractmethod
    def visitUnaryExpr(self, Expr):
        pass

    @abstractmethod
    def visitVariableExpr(self, Expr):
        pass


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name: Token = name
        self.value: Expr = value

    def accept(self, visitor):
        return visitor.visitAssignExpr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]):
        self.callee: Expr = callee
        self.paren: Token = paren
        self.arguments: List[Expr] = arguments

    def accept(self, visitor):
        return visitor.visitCallExpr(self)


class Get(Expr):
    def __init__(self, object: Expr, name: Token):
        self.object: Expr = object
        self.name: Token = name

    def accept(self, visitor):
        return visitor.visitGetExpr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value: object):
        self.value: object = value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)


class Set(Expr):
    def __init__(self, object: Expr, name: Token, value: Expr):
        self.object: Expr = object
        self.name: Token = name
        self.value: Expr = value

    def accept(self, visitor):
        return visitor.visitSetExpr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name: Token = name

    def accept(self, visitor):
        return visitor.visitVariableExpr(self)
