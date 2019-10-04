ifneq (,)
.error This Makefile requires GNU Make.
endif

.PHONY: all lint-files lint-json lint-python _pull-files _pull-json _pull-python

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
	@echo "lint-all     Lint all targets below"
	@echo "lint-files   Lint and test all files"
	@echo "lint-json    Lint JSON files"
	@echo "lint-python  Lint Python files"


lint-all:
	@$(MAKE) --no-print-directory lint-files
	@$(MAKE) --no-print-directory lint-json
	@$(MAKE) --no-print-directory lint-python


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


lint-python: _pull-python
	@echo "################################################################################"
	@echo "# Python lint"
	@echo "################################################################################"
	@docker run --rm -v ${PWD}:/data cytopia/pycodestyle .


# --------------------------------------------------------------------------------
# Helper Targets
# --------------------------------------------------------------------------------
_pull-files:
	@docker pull cytopia/file-lint:$(FL_VERSION)


_pull-json:
	@docker pull cytopia/jsonlint:$(JL_VERSION)


_pull-python:
	@docker pull cytopia/pycodestyle:latest
