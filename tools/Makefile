# Makefile to help with updating of webpages


all: one two three four five six seven

all1: one two three four
all2: five six seven

clean: 
	mkdir -p status
	rm -fv status/*
	python generate-webpage-clean-setup.py
	bash generate-webpage-clean-setup.sh


one: status/generate-individual-plots
two: status/generate-countries
three: status/copy-ipynb-files
four: status/pelican-publish
five: status/git-commit-push-binder
six: status/git-commit-push-wwwroot
seven: status/trigger-binder-build


status/generate-individual-plots:
	jupyter-nbconvert generate-individiual-plots.ipynb --execute 
	touch status/generate-individual-plots

status/generate-countries:
	jupyter-nbconvert generate-countries.ipynb --execute --ExecutePreprocessor.timeout=600
	touch status/generate-countries


status/copy-ipynb-files: status/generate-countries
	mkdir -p binder/ipynb
	rsync -auv wwwroot/ipynb/* binder/ipynb
	touch status/copy-ipynb-files	

status/pelican-publish: status/generate-individual-plots status/generate-countries status/copy-ipynb-files
	cd pelican && make publish
	touch status/pelican-publish


status/git-commit-push-wwwroot:
	@echo "We should check here we have no new files?"
  # see for example https://stackoverflow.com/questions/5139290/how-to-check-if-theres-nothing-to-be-committed-in-the-current-branch
  # new files could show up if a new country starts reporting numbers, or
  # if a new pelican article is written
	cd wwwroot && git commit -m "updated $(shell date)" -a
	cd wwwroot && git push -v
	touch status/git-commit-push-wwwroot


status/git-commit-push-binder:
	@echo "We should check here we have no new files"
	@# cd binder && git add *
	cd binder && git commit -m "updated $(shell date)" -a
	cd binder && git push -v
	touch status/git-commit-push-binder


status/trigger-binder-build:
	$(shell open https://mybinder.org/v2/gh/oscovida/binder/master?filepath=ipynb/US.ipynb)
	touch status/trigger-binder-build
