.PHONY: generate debug

generate:
	python3 tool/generate_ast.py

debug:
	DEBUG=1 python3 lox.py input.program

jlox:
	../craftinginterpreters/jlox input.program
