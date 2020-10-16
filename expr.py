# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py
from dataclasses import dataclass
from abc import ABC, abstractmethod

from token_class import Token


class Visitor(ABC):
    @abstractmethod
    def visit_BinaryExpr(self):
        pass

    @abstractmethod
    def visit_GroupingExpr(self):
        pass

    @abstractmethod
    def visit_LiteralExpr(self):
        pass

    @abstractmethod
    def visit_UnaryExpr(self):
        pass


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_BinaryExpr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor):
        return visitor.visit_GroupingExpr(self)


@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor):
        return visitor.visit_LiteralExpr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor):
        return visitor.visit_UnaryExpr(self)
