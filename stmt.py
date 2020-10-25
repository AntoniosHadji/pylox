# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py
from dataclasses import dataclass
from abc import ABC, abstractmethod

from token_class import Token
from typing import List
from expr import Expr


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
    def visitFunctionStmt(self, Stmt):
        pass

    @abstractmethod
    def visitIfStmt(self, Stmt):
        pass

    @abstractmethod
    def visitPrintStmt(self, Stmt):
        pass

    @abstractmethod
    def visitReturnStmt(self, Stmt):
        pass

    @abstractmethod
    def visitVarStmt(self, Stmt):
        pass

    @abstractmethod
    def visitWhileStmt(self, Stmt):
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
class Function(Stmt):
    name: Token
    params: List[Token]
    body: List[Stmt]

    def accept(self, visitor):
        return visitor.visitFunctionStmt(self)


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
class Return(Stmt):
    keyword: Token
    value: Expr

    def accept(self, visitor):
        return visitor.visitReturnStmt(self)


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept(self, visitor):
        return visitor.visitVarStmt(self)


@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

    def accept(self, visitor):
        return visitor.visitWhileStmt(self)
