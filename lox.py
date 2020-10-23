import sys
from parser import Parser
from typing import List

import stmt
from interpreter import Interpreter, LoxRuntimeError
from scanner import Scanner
from token_class import Token
from token_type import TokenType

hadError: bool = False
hadRuntimeError: bool = False


def runFile(name: str):
    print(f"exec file: {name}")
    with open(name, "r") as f:
        lines = f.read()

    run(lines)
    if hadError:
        sys.exit(65)
    if hadRuntimeError:
        sys.exit(70)


def runPrompt():
    global hadError
    print("start lox prompt:")
    while True:
        sys.stdout.write("\n> ")
        try:
            line = input()
        except EOFError:
            # CTRL-D
            break
        if line == "":
            break
        run(line)
        hadError = False


def run(line: str):
    import pdb

    # pdb.set_trace()
    scanner: Scanner = Scanner(line, error_scan)
    tokens: List[Token] = scanner.scanTokens()
    parser: Parser = Parser(tokens, error_parse)
    statements: List[stmt.Stmt] = parser.parse()

    # // Stop if there was a syntax error.
    if hadError:
        return

    # for t in tokens:
    #     print(t)
    # sys.stdout.write(ASTPrinter().pprint(expression))
    Interpreter(runtimeError).interpret(statements)


def error_scan(line: int, message: str) -> None:
    report(line, "", message)


def error_parse(token: Token, message: str) -> None:
    if token.ttype == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)


def runtimeError(error: LoxRuntimeError):
    sys.stderr.write(f"{error}\n")
    if all([hasattr(error, "message"), hasattr(error, "token")]):
        if hasattr(error.token, "line"):
            sys.stderr.write(f"{error.message}\n[line {error.token.line}]")

    global hadRuntimeError
    hadRuntimeError = True


def report(line: int, where: str, message: str):
    sys.stderr.write("[line " + str(line) + "] Error" + where + ": " + message + "\n")
    global hadError
    hadError = True


if __name__ == "__main__":

    args = sys.argv
    # remove script name
    args.pop(0)
    if len(args) > 1:
        sys.stdout.write("Usage: jlox [script]\n")
        sys.exit(64)
    elif len(args) == 1:
        runFile(args[0])
    else:
        runPrompt()
