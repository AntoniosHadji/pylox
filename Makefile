.PHONY: generate debug build_tests test

help: ## Prints help for targets with comments
	@grep -E '^[a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

generate: ## Regenarate statement and expression classes
	python3 tool/generate_ast.py

debug: ## Run lox.py with python debugger enabled
	DEBUG=1 python3 lox.py input.program

build_tests: ## rebuild tests
	python3 tool/build_tests.py

test: ## execute test suite
	python3 -m pytest -v --cov-report term --cov=. \
		--ignore=tests/dataclass_test.py \
		--ignore=tests/benchmark/ \
		--deselect=tests/for/test_for.py::test_closure_in_body \
		--deselect=tests/function/test_function.py::test_mutual_recursion \
		--deselect=tests/limit/test_limit.py::test_stack_overflow \
		--deselect=tests/number/test_number.py::test_nan_equality \
		--deselect=tests/return/test_return.py::test_at_top_level \
		--deselect=tests/while/test_while.py::test_closure_in_body

broken:  ## run failing tests
	python3 -m pytest -v \
		tests/limit/test_limit.py::test_stack_overflow \
		tests/number/test_number.py::test_nan_equality \
		tests/return/test_return.py::test_at_top_level \
		tests/while/test_while.py::test_closure_in_body \

broken_zero:  ## run failing tests that work in jlox
	python3 -m pytest -v \
		tests/function/test_function.py::test_mutual_recursion \
		tests/for/test_for.py::test_closure_in_body



# maximum recursion depth exceeded in comparison
# --deselect=tests/function/test_function.py::test_mutual_recursion \
