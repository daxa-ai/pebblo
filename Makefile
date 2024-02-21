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
	python -m build --wheel

install: build
	pip install --force-reinstall dist/*.whl

################################################
# TESTS
################################################

# Define a variable for the test file path.
TEST_FILE ?= tests/

test:
	pytest $(TEST_FILE)

tests:
	pytest $(TEST_FILE)

################################################
# LINT
################################################
PYTHON_FILES=.
MYPY_CACHE=.mypy_cache

lint:
	ruff check .
	ruff format . --diff
	ruff --select I .
	mkdir -p $(MYPY_CACHE) && mypy --install-types --non-interactive $(PYTHON_FILES) --cache-dir $(MYPY_CACHE)

spell_check:
	codespell --toml pyproject.toml
################################################
# FORMAT
################################################

format:
	ruff check . --fix

################################################
# HELP
################################################
help:
	@echo '----'
	@echo 'clean                        - remove build artifacts'
	@echo 'build                        - build the package'
	@echo 'install                      - install the package'
	@echo 'test                         - run unit tests'
	@echo 'tests                        - run unit tests'
	@echo 'test TEST_FILE=<test_file>   - run all tests in file'
	@echo 'tests TEST_FILE=<test_file>  - run all tests in file'


.PHONY: all clean build install test tests help lint spell_check
