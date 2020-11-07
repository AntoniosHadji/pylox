.PHONY: generate debug build_tests test

generate:
	python3 tool/generate_ast.py

debug:
	DEBUG=1 python3 lox.py input.program

jlox:
	../craftinginterpreters/jlox input.program

build_tests:
	python3 tool/build_tests.py

test: build_tests
	python3 -m pytest -v \
		--ignore=tests/dataclass_test.py \
		--ignore=tests/benchmark/ \
		--deselect=tests/for/test_for.py::test_closure_in_body \
		--deselect=tests/function/test_function.py::test_mutual_recursion \
		--deselect=tests/limit/test_limit.py::test_stack_overflow \
		--deselect=tests/number/test_number.py::test_nan_equality \
		--deselect=tests/return/test_return.py::test_at_top_level \
		--deselect=tests/while/test_while.py::test_closure_in_body
