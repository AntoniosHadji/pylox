from typing import Callable, List

import stmt
from expr import Binary, Expr, Grouping, Literal, Unary
from token_class import Token
from token_type import TokenType


class Parser:
    current: int = 0

    class ParserError(BaseException):
        pass

    def __init__(self, tokens: List[Token], error_function: Callable):
        self.tokens = tokens
        self.errorToken = error_function

    def parse(self) -> List[stmt.Stmt]:
        statements: List[stmt.Stmt] = []
        while not self.isAtEnd():
            statements.append(self.statement())

        return statements

    def expression(self) -> Expr:
        return self.equality()

    def statement(self) -> stmt.Stmt:
        if self.match(TokenType.PRINT):
            return self.printStatement()

        return self.expressionStatement()

    def printStatement(self) -> stmt.Stmt:
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)

    def expressionStatement(self) -> stmt.Stmt:
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return stmt.Expression(expr)

    def equality(self) -> Expr:
        # anything of higher precedence is returned without executing loop
        expr: Expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        # TODO: you could create a helper method for parsing a left-associative
        # series of binary operators given a list of token types and an operand
        # method handle to simplify this redundant code.
        expr: Expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        # anything of higher precedence is returned without executing loop
        expr: Expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        # anything of higher precedence is returned without executing loop
        expr: Expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True

        return False

    def consume(self, t: TokenType, message: str) -> Token:
        if self.check(t):
            return self.advance()

        raise self.error(self.peek(), message)

    def check(self, t: TokenType) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().ttype == t

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def isAtEnd(self) -> bool:
        return self.peek().ttype == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def error(self, token: Token, message: str) -> ParserError:
        self.errorToken(token, message)
        return self.ParserError()

    def synchronize(self) -> None:
        self.advance()

        while not self.isAtEnd():
            if self.previous().ttype == TokenType.SEMICOLON:
                return

            if self.peek().ttype in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self.advance()
