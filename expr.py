# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py
from dataclasses import dataclass
from abc import ABC, abstractmethod

from token_class import Token
from typing import List


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
    def visitGroupingExpr(self, Expr):
        pass

    @abstractmethod
    def visitLiteralExpr(self, Expr):
        pass

    @abstractmethod
    def visitLogicalExpr(self, Expr):
        pass

    @abstractmethod
    def visitUnaryExpr(self, Expr):
        pass

    @abstractmethod
    def visitVariableExpr(self, Expr):
        pass


@dataclass(frozen=True)
class Assign(Expr):
    name: Token
    value: Expr

    def accept(self, visitor):
        return visitor.visitAssignExpr(self)


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


@dataclass(frozen=True)
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: List[Expr]

    def accept(self, visitor):
        return visitor.visitCallExpr(self)


@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


@dataclass(frozen=True)
class Literal(Expr):
    value: object

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


@dataclass(frozen=True)
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)


@dataclass(frozen=True)
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)


@dataclass(frozen=True)
class Variable(Expr):
    name: Token

    def accept(self, visitor):
        return visitor.visitVariableExpr(self)
