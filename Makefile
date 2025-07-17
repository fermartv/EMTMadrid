.DEFAULT_GOAL := help 

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

pre-requirements:
	@scripts/pre-requirements.sh

.PHONY: local-setup
local-setup: pre-requirements ## Sets up the local environment (e.g. install git hooks)
	scripts/local-setup.sh
	make install

.PHONY: install
install: pre-requirements ## Install the app packages
	uv python install 3.13.2
	uv python pin 3.13.2
	uv sync --no-install-project

.PHONY: update
update: pre-requirements ## Updates the app packages
	uv lock --upgrade

.PHONY: add-dev-package
add-dev-package: pre-requirements ## Installs a new package in the app. ex: make add-dev-package package=XXX
	uv add --dev $(package)
	uv sync

.PHONY: add-package
add-package: pre-requirements ## Installs a new package in the app. ex: make add-package package=XXX
	uv add $(package)
	uv sync

.PHONY: run-example
run-example: pre-requirements ## Runs the basic example
	uv run example/basic_usage_example.py

.PHONY: check-typing
check-typing: pre-requirements  ## Run a static analyzer over the code to find issues
	uv run ty check .

.PHONY: check-lint
check-lint: pre-requirements ## Checks the code style
	uv run ruff check

.PHONY: check-format
check-format: pre-requirements  ## Check format python code
	uv run ruff format --check

checks: check-typing check-lint check-format ## Run all checks

.PHONY: lint
lint: pre-requirements ## Lints the code format
	uv run ruff check --fix

.PHONY: format
format: pre-requirements  ## Format python code
	uv run ruff format

.PHONY: test
test:  ## Run tests.
	uv run pytest tests -ra

.PHONY: test-coverage
test-coverage:  ## Run tests.
	uv run pytest tests -ra --cov=emt_madrid --cov-report=html

.PHONY: test-gitflow-actions
test-gitflow-actions:  ## Test CI actions.
	act --container-architecture linux/amd64

.PHONY: pre-commit
pre-commit: pre-requirements checks test test-gitflow-actions