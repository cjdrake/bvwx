.PHONY: help
help:
	@echo Usage: make [options] [target] ...
	@echo Valid targets:
	@echo     lint  - PyLint
	@echo     test  - PyTest
	@echo     prof  - PyTest with profile report
	@echo     cov   - PyTest with HTML coverage report

PYTHON := python
PYLINT := pylint
FLAKE8 := flake8
PYTEST := pytest

.PHONY: lint
lint:
	@$(PYLINT) src/bvwx tests
	@$(FLAKE8)

.PHONY: test
test:
	@$(PYTEST) --doctest-modules

.PHONY: prof
prof:
	@$(PYTEST) --doctest-modules --profile

.PHONY: cov
cov:
	@$(PYTEST) --doctest-modules --cov=src/bvwx --cov-branch --cov-report=html
