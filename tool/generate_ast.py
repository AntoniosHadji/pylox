import pathlib
import sys
from typing import List, TextIO

import black
import isort


def main():
    print(sys.argv)

    if len(sys.argv) == 2:
        outputDir: str = sys.argv.pop(1)
    else:
        # use current directory if not given
        p = pathlib.Path(__file__).resolve().parent
        remove = sys.argv[0].rsplit("/", maxsplit=1)[0]
        outputDir: str = str(p).replace(remove, "")

    defineAst(
        outputDir,
        "Expr",
        [
            "Assign   : Token name, Expr value",
            "Binary   : Expr left, Token operator, Expr right",
            "Call     : Expr callee, Token paren, List[Expr] arguments",
            "Get      : Expr object, Token name",
            "Grouping : Expr expression",
            "Literal  : object value",
            "Logical  : Expr left, Token operator, Expr right",
            "Set      : Expr object, Token name, Expr value",
            "Super    : Token keyword, Token method",
            "This     : Token keyword",
            "Unary    : Token operator, Expr right",
            "Variable : Token name",
        ],
    )
    defineAst(
        outputDir,
        "Stmt",
        [
            "Block      : List[Stmt] statements",
            "Class      : Token name, Optional[Class] superclass, List[LoxFunction] methods",  # noqa E501
            "Expression : Expr expression",
            "Function   : Token name, List[Token] params, List[Stmt] body",
            "If         : Expr condition, Stmt thenBranch, Stmt elseBranch",
            "Print      : Expr expression",
            "Return     : Token keyword, Expr value",
            "Var        : Token name, Expr initializer",
            "While      : Expr condition, Stmt body",
        ],
    )


def defineAst(outputDir: str, baseName: str, types: List[str]):
    path: str = outputDir + "/" + baseName.lower() + ".py"
    className: str

    with open(path, "w") as f:
        # imports
        f.write("# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py\n")
        # f.write("from dataclasses import dataclass\n")
        if baseName.lower() == "stmt":
            f.write("from __future__ import annotations  # define out of order\n")
            f.write("from expr import Expr\n")
            f.write("from typing import Optional, Dict\n")
            f.write("from loxfunction import LoxFunction\n")
        f.write("from abc import ABC, abstractmethod\n")
        f.write("from token_class import Token\n")
        f.write("from typing import List\n")
        f.write("\n\n")

        # base class for AST classes
        # base class created first so it can be used as parameter to visitor methods
        f.write(f"class {baseName}(ABC):\n")
        f.write("    @abstractmethod\n")
        f.write("    def accept(self, visitor):\n")
        f.write("        raise NotImplementedError\n")
        f.write("\n\n")

        # Visitor class
        f.write("class Visitor(ABC):\n")
        for t in types:
            f.write("    @abstractmethod\n")
            className = t.split(":")[0].strip()
            # baseName added as parameter for python conversion
            f.write(f"    def visit{className}{baseName}(self, {baseName}):\n")
            f.write("        raise NotImplementedError\n")
        f.write("\n\n")

        # The AST classes.
        for t in types:
            className = t.split(":")[0].strip()
            fields: str = t.split(":")[1].strip()
            defineType(f, baseName, className, fields)


def defineType(writer: TextIO, baseName: str, className: str, fieldList: str):
    # writer.write("@dataclass(frozen=True)\n")
    writer.write("class " + className + "(" + baseName + "):\n")

    # // Store parameters in fields.
    fields: List[str] = fieldList.split(", ")
    writer.write("    def __init__(self")
    for field in fields:
        name: str = field.split(" ")[1]
        field_type: str = field.split(" ")[0]
        # writer.write(f"    {name}: {field_type}\n")
        writer.write(f", {name}: {field_type}")
    writer.write("):\n")
    for field in fields:
        name: str = field.split(" ")[1]
        field_type: str = field.split(" ")[0]
        writer.write(f"        self.{name}: {field_type} = {name}\n")

    writer.write("\n")
    writer.write("    def accept(self, visitor):\n")
    writer.write(f"        return visitor.visit{className}{baseName}(self)\n")
    writer.write("\n\n")


if __name__ == "__main__":
    main()

    p = pathlib.Path(__file__).resolve().parent.parent / "expr.py"
    print(p)
    print(
        black.format_file_in_place(
            src=p,
            fast=False,
            mode=black.Mode(target_versions={black.TargetVersion.PY38}),
            write_back=black.WriteBack.YES,
        )
    )
    print(isort.file(p))

    p = pathlib.Path(__file__).resolve().parent.parent / "stmt.py"
    print(p)
    print(
        black.format_file_in_place(
            src=p,
            fast=False,
            mode=black.Mode(target_versions={black.TargetVersion.PY38}),
            write_back=black.WriteBack.YES,
        )
    )
    print(isort.file(p))
