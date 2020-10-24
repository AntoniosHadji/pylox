# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py
from dataclasses import dataclass
from abc import ABC, abstractmethod

from token_class import Token
from expr import Expr
from typing import List


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Visitor(ABC):
    @abstractmethod
    def visitBlockStmt(self, Stmt):
        pass

    @abstractmethod
    def visitExpressionStmt(self, Stmt):
        pass

    @abstractmethod
    def visitIfStmt(self, Stmt):
        pass

    @abstractmethod
    def visitPrintStmt(self, Stmt):
        pass

    @abstractmethod
    def visitVarStmt(self, Stmt):
        pass


@dataclass
class Block(Stmt):
    statements: List[Stmt]

    def accept(self, visitor):
        return visitor.visitBlockStmt(self)


@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)


@dataclass
class If(Stmt):
    condition: Expr
    thenBranch: Stmt
    elseBranch: Stmt

    def accept(self, visitor):
        return visitor.visitIfStmt(self)


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
