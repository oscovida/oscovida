# Makefile to help with updating of webpages

all: one two three four 

clean: 
	mkdir -p status
	rm -fv status/*
	python generate-webpage-clean-setup.py
	bash generate-webpage-clean-setup.sh


one: status/generate-individual-plots
two: status/generate-countries
three: status/copy-ipynb-files
four: status/pelican-publish
five: status/git-commit-push-wwwroot
six: status/git-commit-push-binder


status/generate-individual-plots:
	jupyter-nbconvert generate-individiual-plots.ipynb --execute && touch make-generate-individua
	touch status/generate-individual-plots

status/generate-countries:
	jupyter-nbconvert generate-countries.ipynb --execute --ExecutePreprocessor.timeout=600
	touch status/generate-countries


status/copy-ipynb-files:
	mkdir -p binder/ipynb
	rsync -auv wwwroot/ipynb/* binder/ipynb
	touch status/copy-ipynb-files	

status/pelican-publish:
	cd pelican && make publish
	touch status/pelican-publish


status/git-commit-push-wwwroot:
	cd wwwroot && git commit -m "updated $(shell date)" -a
  cd wwwroot && git push -v
	touch status/git-commit-wwwroot


status/git-commit-push-binder:
	cd binder && git commit -m "updated $(shell date)" -a
  cd binder && git push -v
	touch status/git-commit-binder

