import errors
from token_class import Token
from token_type import TokenType


class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source):
        self.source = source
        self.tokens = list()
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self):
        while not self.isAtEnd():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.scanToken()

        # last token in token list, end of input
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self):  # noqa: C901
        c = self.advance()
        if c == "(":
            self.addToken(TokenType.LEFT_PAREN)
        elif c == ")":
            self.addToken(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.addToken(TokenType.LEFT_BRACE)
        elif c == "}":
            self.addToken(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.addToken(TokenType.COMMA)
        elif c == ".":
            self.addToken(TokenType.DOT)
        elif c == "-":
            self.addToken(TokenType.MINUS)
        elif c == "+":
            self.addToken(TokenType.PLUS)
        elif c == ";":
            self.addToken(TokenType.SEMICOLON)
        elif c == "*":
            self.addToken(TokenType.STAR)
        elif c == "!":
            self.addToken(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.addToken(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
        elif c == "<":
            self.addToken(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self.addToken(
                TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            )
        elif c == "/":
            if self.match("/"):
                # // A comment goes until the end of the line.
                while self.peek() != "\n" and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)

        elif c in [" ", "\r", "\t"]:
            # ignore whitespace
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.handle_string()
        else:
            if self.isDigit(c):
                self.number()
            elif self.isAlpha(c):
                self.identifier()
            else:
                errors.error(self.line, "Unexpected Character")

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        ttype = self.keywords.get(text)
        if ttype is None:
            ttype = TokenType.IDENTIFIER

        self.addToken(ttype)

    def isDigit(self, c: str):
        return c >= "0" and c <= "9"

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()

        # // Look for a fractional part.
        if self.peek() == "." and self.isDigit(self.peekNext()):
            # // Consume the "."
            self.advance()

        while self.isDigit(self.peek()):
            self.advance()

        self.addToken(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def handle_string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
                self.advance()

        if self.isAtEnd():
            errors.error(self.line, "Unterminated string.")
            return

        # // The closing "
        self.advance()

        # // Trim the surrounding quotes.
        value = self.source[self.start + 1 : self.current - 1]
        self.addToken(TokenType.STRING, value)

    def match(self, expected):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def isAlpha(self, c):
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def isAtEnd(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def addToken(self, ttype: TokenType, literal: dict = {}):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(ttype, text, literal, self.line))
