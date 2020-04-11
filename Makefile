PYTHON?=python3

test:
	$(PYTHON) -m pytest -v

test-pycodestyle:
	$(PYTHON) -m pycodestyle --filename=*.py .

test-all: test test-pycodestyle

docker-build:
	docker build -f tools/docker/Dockerfile -t dockertestimage .

docker-test:
	@# docker run --rm dockertestimage -v $PWD:/io make test-all
	docker run --rm -it -v $PWD:/io dockertestimage make test

travis:
	make docker-build
	make docker-test





