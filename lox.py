import os
import sys

from scanner import Scanner

hadError = False


def runFile(name: str):
    print("exec file")
    with open(name, "r") as f:
        lines = f.read()

    print(type(lines))
    run(lines)
    if hadError:
        sys.exit(65)


def runPrompt():
    global hadError
    print("start prompt")
    while True:
        sys.stdout.write("> ")
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        run(line)
        hadError = False


def run(line: str):
    print("exec code")
    print(line)

    scanner = Scanner(line)
    tokens: list = scanner.scanTokens()
    for t in tokens:
        print(t)


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
