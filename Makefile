# makefile used for testing

install:
	python3 -m pip install .[test]

dev-install:
	python3 -m pip install -U -e .[test]
	python3 -m pip install notebook

dev-install-upgrade-depedencies:
	python3 -m pip install --upgrade --upgrade-strategy eager -e .[test]

test:
	python3 -m pytest -v --cov=oscovida

test-pelican:
	cd tools && jupyter-nbconvert --execute generate-individiual-plots.ipynb
	cd tools/pelican && make html

test-html-creation:
	@echo "This is a slow test."
	@#cd tools && jupyter-nbconvert --ExecutePreprocessor.timeout=180 --execute --to html test-plots-for-all-regions.ipynb
	@# cd tools && jupyter-nbconvert --ExecutePreprocessor.timeout=180 --execute --to html generate-countries.ipynb
	cd tools && python test_figure_creation.py


test-pycodestyle:
	python3 -m pycodestyle .

test-all: test test-pycodestyle

docker-build:
	docker build -t dockertestimage .

docker-test:
	@# docker run --rm dockertestimage -v $PWD:/io make test-all
	docker run --rm -it -v $(CWD):/io dockertestimage make test
