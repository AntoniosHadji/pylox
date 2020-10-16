import sys

from token_class import Token
from token_type import TokenType


def error(line: int, message: str) -> None:
    report(line, "", message)


def errorToken(token: Token, message: str) -> None:
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, " at '" + token.lexeme + "'", message)


def report(line: int, where: str, message: str):
    sys.stderr.write("[line " + str(line) + "] Error" + where + ": " + message + "\n")
    global hadError
    hadError = True
