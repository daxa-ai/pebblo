# Default target executed when no arguments are given to make.
all: help

################################################
# BUILD AND INSTALL
################################################
clean:
    # Remove build artifacts
	rm -rf build dist
    # Remove generated files
	find . -type d -name "*\.egg\-info" | xargs rm -rf
    # Remove Python bytecode files
	find . -name __pycache__ | xargs rm -rf

build: clean
	# Ensure the build module is installed
	pip install build
	# Run the build command
	python -m build --wheel

install: build
	pip install --force-reinstall dist/*.whl

################################################
# TESTS
################################################

# Define a variable for the test file path.
TEST_FILE ?= tests/

test:
	pytest $(TEST_FILE) --durations=10

tests:
	pytest $(TEST_FILE) --durations=10

################################################
# LINT
################################################
PYTHON_FILES=.
MYPY_CACHE=.mypy_cache

lint:
	ruff check .
	ruff format . --diff
	ruff check --select I .
	mkdir -p $(MYPY_CACHE) && mypy --install-types --non-interactive $(PYTHON_FILES) --cache-dir $(MYPY_CACHE) --exclude build/ --exclude pebblo_saferetriever --check-untyped-defs || true

lint-fix:
	ruff check . --fix
	ruff format

spell_check:
	codespell --toml pyproject.toml

################################################
# FORMAT
################################################
# define target for format(all the files)
format: PYTHON_FILES=.
# define target for format_diff(only the changed files)
format_diff: PYTHON_FILES=$(shell git diff --relative= --name-only --diff-filter=d main '*.py' '*.ipynb')

format format_diff:
	[ "$(PYTHON_FILES)" = "" ] || ruff check $(PYTHON_FILES) --fix
	[ "$(PYTHON_FILES)" = "" ] || ruff format $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || ruff check --select I --fix $(PYTHON_FILES)

################################################
# HELP
################################################
help:
	@echo '----'
	@echo 'clean                        - remove build artifacts'
	@echo 'build                        - build the package'
	@echo 'install                      - install the package'
	@echo '-- TESTS --'
	@echo 'test                         - run unit tests'
	@echo 'tests                        - run unit tests'
	@echo 'test TEST_FILE=<test_file>   - run all tests in file'
	@echo 'tests TEST_FILE=<test_file>  - run all tests in file'
	@echo '-- LINTING --'
	@echo 'lint                         - run linters'
	@echo 'spell_check                  - run codespell on the project'
	@echo 'format                       - run code formatters'
	@echo 'format_diff                  - run code formatters on changed files'


.PHONY: all clean build install test tests help lint spell_check
