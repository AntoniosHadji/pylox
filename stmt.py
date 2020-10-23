# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py
from dataclasses import dataclass
from abc import ABC, abstractmethod

from token_class import Token
from expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Visitor(ABC):
    @abstractmethod
    def visitExpressionStmt(self, Stmt):
        pass

    @abstractmethod
    def visitPrintStmt(self, Stmt):
        pass

    @abstractmethod
    def visitVarStmt(self, Stmt):
        pass


@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)


@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor):
        return visitor.visitPrintStmt(self)


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept(self, visitor):
        return visitor.visitVarStmt(self)
