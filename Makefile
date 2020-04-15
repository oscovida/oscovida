# makefile used for testing

install:
	python3 -m pip install .[test]

dev-install:
	python3 -m pip install -U -e .[test]

test:
	python3 -m pytest -v

test-pycodestyle:
	python3 -m pycodestyle --filename=.*.py --show-pep8

test-all: test test-pycodestyle
