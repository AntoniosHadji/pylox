from typing import Callable, List

import expr as e
import stmt as s
from token_class import Token
from token_type import TokenType


class Parser:
    current: int = 0

    class ParserError(BaseException):
        pass

    def __init__(self, tokens: List[Token], error_function: Callable):
        self.tokens = tokens
        self.errorToken = error_function

    def parse(self) -> List[s.Stmt]:
        statements: List[s.Stmt] = []
        while not self.isAtEnd():
            statements.append(self.declaration())

        return statements

    def expression(self) -> e.Expr:
        return self.assignment()

    def declaration(self) -> s.Stmt:
        try:
            if self.match(TokenType.CLASS):
                return self.classDeclaration()
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except self.ParserError:
            self.synchronize()
            return None

    def classDeclaration(self) -> s.Stmt:
        name: Token = self.consume(TokenType.IDENTIFIER, "Expect class name.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")

        methods: List[s.Function] = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")

        return s.Class(name, methods)

    def statement(self) -> s.Stmt:
        if self.match(TokenType.FOR):
            return self.forStatement()
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.RETURN):
            return self.returnStatement()
        if self.match(TokenType.WHILE):
            return self.whileStatement()
        if self.match(TokenType.LEFT_BRACE):
            return s.Block(self.block())

        return self.expressionStatement()

    def forStatement(self) -> s.Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: s.Stmt = self.statement()

        # not null
        if increment:
            body = s.Block([body, s.Expression(increment)])

        # is null
        if condition is None:
            condition = e.Literal(True)
        body = s.While(condition, body)

        # not null
        if initializer:
            body = s.Block([initializer, body])

        return body

    def ifStatement(self) -> s.Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition: e.Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        thenBranch: s.Stmt = self.statement()
        elseBranch: s.Stmt = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()

        return s.If(condition, thenBranch, elseBranch)

    def printStatement(self) -> s.Stmt:
        value: e.Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return s.Print(value)

    def returnStatement(self) -> s.Stmt:
        keyword: Token = self.previous()
        value: e.Expr = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return s.Return(keyword, value)

    def varDeclaration(self) -> s.Stmt:
        name: Token = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        if self.match(TokenType.EQUAL):
            initializer: e.Expr = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return s.Var(name, initializer)

    def whileStatement(self) -> s.Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition: e.Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body: s.Stmt = self.statement()

        return s.While(condition, body)

    def expressionStatement(self) -> s.Stmt:
        expr: e.Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return s.Expression(expr)

    def function(self, kind: str) -> s.Function:
        name: Token = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters: List[Token] = []
        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(
                self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
            )
            while self.match(TokenType.COMMA):
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")

                parameters.append(
                    self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
                )

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        # block assumes this has already been consumed
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before {kind} body.")
        body: List[s.Stmt] = self.block()
        return s.Function(name, parameters, body)

    def block(self) -> List[s.Stmt]:
        statements: List[s.Stmt] = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self) -> e.Expr:
        expr: e.Expr = self._or()

        if self.match(TokenType.EQUAL):
            equals: Token = self.previous()
            value: e.Expr = self.assignment()

            if isinstance(expr, e.Variable):
                name: Token = expr.name
                return e.Assign(name, value)
            elif isinstance(expr, e.Get):
                get: e.Get = expr
                return e.Set(get.object, get.name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    # underscore to prevent colliding with python builtin or
    def _or(self) -> e.Expr:
        expr: e.Expr = self._and()

        while self.match(TokenType.OR):
            operator: Token = self.previous()
            right: e.Expr = self._and()
            expr = e.Logical(expr, operator, right)

        return expr

    # underscore to prevent colliding with python builtin and
    def _and(self) -> e.Expr:
        expr: e.Expr = self.equality()

        while self.match(TokenType.AND):
            operator: Token = self.previous()
            right: e.Expr = self.equality()
            expr = e.Logical(expr, operator, right)

        return expr

    def equality(self) -> e.Expr:
        # anything of higher precedence is returned without executing loop
        expr: e.Expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: e.Expr = self.comparison()
            expr = e.Binary(expr, operator, right)

        return expr

    def comparison(self) -> e.Expr:
        # TODO: you could create a helper method for parsing a left-associative
        # series of binary operators given a list of token types and an operand
        # method handle to simplify this redundant code.
        expr: e.Expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator: Token = self.previous()
            right: e.Expr = self.term()
            expr = e.Binary(expr, operator, right)

        return expr

    def term(self) -> e.Expr:
        # anything of higher precedence is returned without executing loop
        expr: e.Expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self.previous()
            right: e.Expr = self.factor()
            expr = e.Binary(expr, operator, right)

        return expr

    def factor(self) -> e.Expr:
        # anything of higher precedence is returned without executing loop
        expr: e.Expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator: Token = self.previous()
            right: e.Expr = self.unary()
            expr = e.Binary(expr, operator, right)

        return expr

    def unary(self) -> e.Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: e.Expr = self.unary()
            return e.Unary(operator, right)
        return self.call()

    def finishCall(self, callee: e.Expr) -> e.Expr:
        arguments: List[e.Expr] = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                # java has hard 255 limit, c suggests support for at least 127
                if len(arguments) >= 255:
                    # report error but don't halt
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())

        paren: Token = self.consume(
            TokenType.RIGHT_PAREN, "Expect ')' after arguments."
        )

        return e.Call(callee, paren, arguments)

    def call(self) -> e.Expr:
        expr: e.Expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)
            elif self.match(TokenType.DOT):
                name: Token = self.consume(
                    TokenType.IDENTIFIER, "Expect property name after '.'."
                )
                expr: e.Get = e.Get(expr, name)
            else:
                break

        return expr

    def primary(self) -> e.Expr:
        if self.match(TokenType.FALSE):
            return e.Literal(False)
        if self.match(TokenType.TRUE):
            return e.Literal(True)
        if self.match(TokenType.NIL):
            return e.Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return e.Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return e.Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr: e.Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return e.Grouping(expr)

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
