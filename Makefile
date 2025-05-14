# Sets the minimum test coverage percentage required to pass the tests
TEST_COVERAGE_THRESHOLD=0

default: help

.PHONY: install-deps
install-deps: # Installs prerequisite dependencies required for project installation
	pip3 install uv

.PHONY: install
install: # Synchronizes project dependencies
	uv sync

.PHONY: format
format: # Formats the code
	uv run black .
	uv run isort --profile black .

.PHONY: format-check
format-check: # Checks if the code is formatted according to formatter rules
	uv run black --check --diff .
	uv run isort --check --diff --profile black .

.PHONY: lint
lint: # Runs linter to check for code quality issues
	uv run flake8 .

.PHONY: test
test: # Runs unit and integrations tests
	uv run coverage erase
	uv run coverage run -m pytest

.PHONY: coverage
coverage: # Runs unit and integrations tests
	uv run coverage report -m --fail-under=$(TEST_COVERAGE_THRESHOLD)

.PHONY: help
help: # Displays help page
	@grep -E '^[a-zA-Z0-9 -]+:.*#' $(MAKEFILE_LIST) | sort | while read -r l; do \
		printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; \
	done
