PYTHON=$(shell which python3)

# NAME=kalliope
# FULLNAME=kalliope-0.0.1
NAME=$(shell $(PYTHON) setup.py --name)
FULLNAME=$(shell $(PYTHON) setup.py --fullname)

SRCS=$(wildcard $(NAME)/*.py)
TESTS=$(wildcard tests/*.py)

.PHONY: all dist test clean distclean

all: dist
	

dist: test dist/$(FULLNAME).tar.gz
	

dist/$(FULLNAME).tar.gz: $(SRCS)
	$(PYTHON) setup.py sdist

test: .test-success
	

.test-success: $(SRCS) $(TESTS)
	@rm -f ".test-success"
	$(PYTHON) -m unittest -v
	@touch .test-success

clean:
	rm -rf "__pycache__"
	rm -rf "$(NAME)/__pycache__"
	rm -rf "test/__pycache__"

distclean: clean
	rm -rf "dist"
	rm -rf "$(NAME).egg-info"
	rm -f ".test-success"

