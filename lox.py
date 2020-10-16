import os
import sys
from parser import Parser

from astprinter import ASTPrinter
from expr import Expr
from scanner import Scanner

hadError = False


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
    scanner = Scanner(line)
    tokens: list = scanner.scanTokens()
    for t in tokens:
        print(t)

    parser: Parser = Parser(tokens)
    expression: Expr = parser.parse()

    # // Stop if there was a syntax error.
    if hadError:
        return

    sys.stdout.write(ASTPrinter().pprint(expression))


if __name__ == "__main__":

    args = os.sys.argv
    print(args.pop(0))
    if len(args) > 1:
        sys.stdout.write("Usage: jlox [script]\n")
        sys.exit(64)
    elif len(args) == 1:
        runFile(args[0])
    else:
        runPrompt()
