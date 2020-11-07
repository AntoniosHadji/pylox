.PHONY: generate debug build_tests test

generate:
	python3 tool/generate_ast.py

debug:
	DEBUG=1 python3 lox.py input.program

jlox:
	../craftinginterpreters/jlox input.program

build_tests:
	python3 tool/build_tests.py

test:
	python3 -m pytest -v
