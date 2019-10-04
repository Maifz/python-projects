ifneq (,)
.error This Makefile requires GNU Make.
endif

.PHONY: lint

lint:
	docker run --rm -v ${PWD}:/data cytopia/pycodestyle .
