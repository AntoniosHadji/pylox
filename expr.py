# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py
from dataclasses import dataclass
from abc import ABC, abstractmethod

from token_class import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Visitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, Expr):
        pass

    @abstractmethod
    def visitGroupingExpr(self, Expr):
        pass

    @abstractmethod
    def visitLiteralExpr(self, Expr):
        pass

    @abstractmethod
    def visitUnaryExpr(self, Expr):
        pass

    @abstractmethod
    def visitVariableExpr(self, Expr):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)


@dataclass
class Variable(Expr):
    name: Token

    def accept(self, visitor):
        return visitor.visitVariableExpr(self)
