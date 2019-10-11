ifneq (,)
.error This Makefile requires GNU Make.
endif

.PHONY: all autoformat lint-files lint-json lint-python-black lint-python-pycodestyle lint-python-pydocstyle _pull-files _pull-json _pull-python-black _pull-python-pycodestyle _pull-python-pydocstyle

# --------------------------------------------------------------------------------
# File-lint configuration
# --------------------------------------------------------------------------------
FL_VERSION = 0.2
FL_IGNORES = .git/,.github/,.idea/


# --------------------------------------------------------------------------------
# Jsonlin configuration
# --------------------------------------------------------------------------------
JL_VERSION = 1.6.0-0.4
JL_IGNORES = .idea/*


# --------------------------------------------------------------------------------
# Targets
# --------------------------------------------------------------------------------
help:
	@echo "autoformat               Autoformat Python files according to black"
	@echo "lint-all                 Lint all targets below"
	@echo "lint-files               Lint and test all files"
	@echo "lint-json                Lint JSON files"
	@echo "lint-python-pycodestyle  Lint Python files against pycodestyleodestyle"
	@echo "lint-python-pydocstyle   Lint Python files against pydocstyleocstyle"
	@echo "lint-python-black        Lint Python files against black (code formatter)"


autoformat: _pull-python-black
	docker run --rm -v ${PWD}:/data cytopia/black -l 100 .


lint-all:
	@$(MAKE) --no-print-directory lint-files
	@$(MAKE) --no-print-directory lint-json
	@$(MAKE) --no-print-directory lint-python-pycodestyle
	@$(MAKE) --no-print-directory lint-python-pydocstyle
	@$(MAKE) --no-print-directory lint-python-black


lint-files: _pull-files
	@echo "################################################################################"
	@echo "# File lint"
	@echo "################################################################################"
	@docker run --rm -v ${PWD}:/data cytopia/file-lint:$(FL_VERSION) file-cr --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm -v ${PWD}:/data cytopia/file-lint:$(FL_VERSION) file-crlf --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm -v ${PWD}:/data cytopia/file-lint:$(FL_VERSION) file-trailing-single-newline --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm -v ${PWD}:/data cytopia/file-lint:$(FL_VERSION) file-trailing-space --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm -v ${PWD}:/data cytopia/file-lint:$(FL_VERSION) file-utf8 --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm -v ${PWD}:/data cytopia/file-lint:$(FL_VERSION) file-utf8-bom --text --ignore '$(FL_IGNORES)' --path .
	@echo


lint-json: _pull-json
	@echo "################################################################################"
	@echo "# JSON lint"
	@echo "################################################################################"
	@if docker run --rm -v "${PWD}:/data:ro" cytopia/jsonlint:$(JL_VERSION) \
		-t '  ' -i '$(JL_IGNORES)' '*.json'; then \
		echo "OK"; \
	else \
		echo "Failed"; \
		exit 1; \
	fi;
	@echo


lint-python-black: _pull-python-black
	@echo "################################################################################"
	@echo "# Python code formatting (black)"
	@echo "################################################################################"
	@docker run --rm -v ${PWD}:/data cytopia/black --diff --check -l 100 .
	@echo


lint-python-pycodestyle: _pull-python-pycodestyle
	@echo "################################################################################"
	@echo "# Python lint (pycodestyle)"
	@echo "################################################################################"
	@docker run --rm -v ${PWD}:/data cytopia/pycodestyle .
	@echo


lint-python-pydocstyle: _pull-python-pydocstyle
	@echo "################################################################################"
	@echo "# Python lint (pydocstyle)"
	@echo "################################################################################"
	@docker run --rm -v ${PWD}:/data cytopia/pydocstyle .
	@echo


# --------------------------------------------------------------------------------
# Helper Targets
# --------------------------------------------------------------------------------
_pull-files:
	@docker pull cytopia/file-lint:$(FL_VERSION) >/dev/null


_pull-json:
	@docker pull cytopia/jsonlint:$(JL_VERSION) >/dev/null


_pull-python-black:
	@docker pull cytopia/black:latest >/dev/null


_pull-python-pycodestyle:
	@docker pull cytopia/pycodestyle:latest >/dev/null


_pull-python-pydocstyle:
	@docker pull cytopia/pydocstyle:latest >/dev/null
