# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py
from __future__ import annotations  # define out of order

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from expr import Expr
from loxfunction import LoxFunction
from token_class import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Visitor(ABC):
    @abstractmethod
    def visitBlockStmt(self, Stmt):
        pass

    @abstractmethod
    def visitClassStmt(self, Stmt):
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


class Block(Stmt):
    def __init__(self, statements: List[Stmt]):
        self.statements: List[Stmt] = statements

    def accept(self, visitor):
        return visitor.visitBlockStmt(self)


class Class(Stmt):
    def __init__(
        self, name: Token, superclass: Optional[Class], methods: Dict[str, LoxFunction]
    ):
        self.name: Token = name
        self.superclass: Optional[Class] = superclass
        self.methods: Dict[str, LoxFunction] = methods

    def accept(self, visitor):
        return visitor.visitClassStmt(self)


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)


class Function(Stmt):
    def __init__(self, name: Token, params: List[Token], body: List[Stmt]):
        self.name: Token = name
        self.params: List[Token] = params
        self.body: List[Stmt] = body

    def accept(self, visitor):
        return visitor.visitFunctionStmt(self)


class If(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt):
        self.condition: Expr = condition
        self.thenBranch: Stmt = thenBranch
        self.elseBranch: Stmt = elseBranch

    def accept(self, visitor):
        return visitor.visitIfStmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor):
        return visitor.visitPrintStmt(self)


class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr):
        self.keyword: Token = keyword
        self.value: Expr = value

    def accept(self, visitor):
        return visitor.visitReturnStmt(self)


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name: Token = name
        self.initializer: Expr = initializer

    def accept(self, visitor):
        return visitor.visitVarStmt(self)


class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition: Expr = condition
        self.body: Stmt = body

    def accept(self, visitor):
        return visitor.visitWhileStmt(self)
