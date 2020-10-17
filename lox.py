import sys
from parser import Parser
from typing import Union

from astprinter import ASTPrinter
from expr import Expr
from scanner import Scanner
from token_class import Token
from token_type import TokenType

hadError: bool = False


def runFile(name: str):
    print(f"exec file: {name}")
    with open(name, "r") as f:
        lines = f.read()

    run(lines)
    if hadError:
        sys.exit(65)


def runPrompt():
    global hadError
    print("start prompt")
    while True:
        sys.stdout.write("\n> ")
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        run(line)
        hadError = False


def run(line: str):
    scanner = Scanner(line, error_scan)
    tokens: list = scanner.scanTokens()
    for t in tokens:
        print(t)

    parser: Parser = Parser(tokens, error_parse)
    expression: Union[Expr, None] = parser.parse()

    # // Stop if there was a syntax error.
    if hadError:
        return

    sys.stdout.write(ASTPrinter().pprint(expression))


def error_scan(line: int, message: str) -> None:
    report(line, "", message)


def error_parse(token: Token, message: str) -> None:
    if token.ttype == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)


def report(line: int, where: str, message: str):
    sys.stderr.write("[line " + str(line) + "] Error" + where + ": " + message + "\n")
    global hadError
    hadError = True


if __name__ == "__main__":

    args = sys.argv
    print(args.pop(0))
    if len(args) > 1:
        sys.stdout.write("Usage: jlox [script]\n")
        sys.exit(64)
    elif len(args) == 1:
        runFile(args[0])
    else:
        runPrompt()
