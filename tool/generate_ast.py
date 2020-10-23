import pathlib
import sys
from typing import List, TextIO

import black


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
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : object value",
            "Unary    : Token operator, Expr right",
            "Variable : Token name",
        ],
    )
    defineAst(
        outputDir,
        "Stmt",
        [
            "Expression : Expr expression",
            "Print      : Expr expression",
            "Var        : Token name, Expr initializer",
        ],
    )


def defineAst(outputDir: str, baseName: str, types: List[str]):
    path: str = outputDir + "/" + baseName.lower() + ".py"
    className: str

    with open(path, "w") as f:
        # imports
        f.write("# AUTO-GENERATED: do not edit.  look at ./tool/generate_ast.py\n")
        f.write("from dataclasses import dataclass\n")
        f.write("from abc import ABC, abstractmethod\n")
        f.write("\n")
        f.write("from token_class import Token\n")
        if baseName.lower() == "stmt":
            f.write("from expr import Expr\n")
        f.write("\n\n")

        # base class for AST classes
        # base class created first so it can be used as parameter to visitor methods
        f.write(f"class {baseName}(ABC):\n")
        f.write("    @abstractmethod\n")
        f.write("    def accept(self, visitor):\n")
        f.write("        pass\n")
        f.write("\n\n")

        # Visitor class
        f.write("class Visitor(ABC):\n")
        for t in types:
            f.write("    @abstractmethod\n")
            className = t.split(":")[0].strip()
            # baseName added as parameter for python conversion
            f.write(f"    def visit{className}{baseName}(self, {baseName}):\n")
            f.write("        pass\n")
        f.write("\n\n")

        # The AST classes.
        for t in types:
            className = t.split(":")[0].strip()
            fields: str = t.split(":")[1].strip()
            defineType(f, baseName, className, fields)


def defineType(writer: TextIO, baseName: str, className: str, fieldList: str):
    writer.write("@dataclass\n")
    writer.write("class " + className + "(" + baseName + "):\n")

    # // Store parameters in fields.
    fields: List[str] = fieldList.split(", ")
    for field in fields:
        name: str = field.split(" ")[1]
        field_type: str = field.split(" ")[0]
        writer.write(f"    {name}: {field_type}\n")
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
