# makefile used for testing

install:
	python3 -m pip install .[test]

dev-install:
	python3 -m pip install -U -e .[test]
	python3 -m pip install notebook

dev-install-upgrade-depedencies:
	python3 -m pip install --upgrade --upgrade-strategy eager -e .[test]

test:
	python3 -m pytest -v --showlocals --capture=no --cov=oscovida

# execute notebooks to ensure they work
test-nbval:
	python3 -m pytest --nbval-lax tools/pelican/content

test-pelican:
	cd tools && python3 -m nbconvert --execute --inplace generate-individiual-plots.ipynb
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


# rsync notebooks to binder repository; needs to be called manually
# when new notebooks are added to tools/pelican/content/ipynb
sync-to-binder-repo:
	@# we assume the binder repo is at ../oscovida-binder relative to
	@# this directory
	rsync -auv tools/pelican/content/ipynb/*.ipynb ../oscovida-binder/ipynb
