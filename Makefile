.PHONY: help docs test clean init build

NOSE2_VERSION=$(shell grep '^__version__' nose2/_version.py | cut -d '"' -f2)

help:
	@echo 'Easy setup for local nose2 development'
	@echo 'make help    Show this help'
	@echo 'make docs    Build docs'
	@echo 'make test    Test nose2'
	@echo 'make clean   Cleanup'

.venv:
	virtualenv --python python3 .venv
	.venv/bin/pip install -U tox twine

test: .venv
	.venv/bin/tox
docs: .venv
	.venv/bin/tox -e docs

build: .venv
	rm -rf dist/
	.venv/bin/python setup.py sdist bdist_wheel

release: build
	.venv/bin/twine upload dist/*
	git tag -s "$(NOSE2_VERSION)" -m "v$(NOSE2_VERSION)"


clean:
	$(MAKE) -C docs/ clean
	rm -rf .venv
