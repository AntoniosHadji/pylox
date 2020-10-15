import sys


def error(line: int, message: str) -> None:
    report(line, "", message)


def report(line: int, where: str, message: str):
    sys.stderr.write("[line " + str(line) + "] Error" + where + ": " + message + "\n")
    global hadError
    hadError = True
