# control the py version used to install tox
# use like
#   NOSE2_PYTHON_VERSION=python3.6 make docs
NOSE2_PYTHON_VERSION?=python
VIRTUALENV=.venv-$(NOSE2_PYTHON_VERSION)

.PHONY: help docs test clean

help:
	@echo 'Easy setup for local nose2 development'
	@echo 'make help    Show this help'
	@echo 'make docs    Build docs'
	@echo 'make test    Test nose2'
	@echo 'make clean   Cleanup'

$(VIRTUALENV)/bin/tox:
	virtualenv --python "$(NOSE2_PYTHON_VERSION)" $(VIRTUALENV)
	$(VIRTUALENV)/bin/pip install tox==2.9.1

test: $(VIRTUALENV)/bin/tox
	$(VIRTUALENV)/bin/tox
docs: $(VIRTUALENV)/bin/tox
	$(VIRTUALENV)/bin/tox -e docs

clean:
	$(MAKE) -C docs/ clean
	rm -rf .venv-*
