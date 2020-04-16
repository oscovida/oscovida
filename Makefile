# makefile used for testing

install:
	python3 -m pip install .[test]

dev-install:
	python3 -m pip install -U -e .[test]

test:
	python3 -m pytest -v

test-pycodestyle:
	python3 -m pycodestyle .

test-all: test test-pycodestyle

docker-build:
	docker build -t dockertestimage .

docker-test:
	@# docker run --rm dockertestimage -v $PWD:/io make test-all
	docker run --rm -it -v $(CWD):/io dockertestimage make test
