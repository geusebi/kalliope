.PHONY: tests

all: tests

tests:
	python3 -m unittest -v tests

