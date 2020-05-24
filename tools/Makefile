# Makefile to help with updating of webpages

all: one two four 

clean: 
	mkdir -p status
	rm -fv status/*
	python generate-webpage-clean-setup.py
	bash python generate-webpage-clean-setup.sh


one: status/generate-individual-plots
two: status/generate-countries
three: status/copy-ipynb-files
four: status/pelican-publish
five: status/git-commit
six: status/git-push


status/generate-individual-plots:
	jupyter-nbconvert generate-individiual-plots.ipynb --execute && touch make-generate-individua
	touch status/generate-individual-plots

status/generate-countries:
	jupyter-nbconvert generate-countries.ipynb --execute --ExecutePreprocessor.timeout=600
	touch status/generate-countries



status/copy-ipynb-files:
	@echo "Still needs to be written"

status/pelican-publish:
	cd pelican && make publish
	touch status/pelican-publish


status/git-commit:
	cd wwwroot && git commit -m "updated $(shell date)" -a
	touch status/git-commit

status/git-push:
	cd wwwroot && git push
	touch status/git-push


