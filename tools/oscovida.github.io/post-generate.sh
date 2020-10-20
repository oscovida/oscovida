#!/usr/bin/env bash

# CD to this scripts directory
scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")
cd $scriptDir

# Paths should be relative to where this script is
python -m nbconvert --execute --inplace ../generate-individiual-plots.ipynb
python -m nbconvert --execute --inplace --ExecutePreprocessor.timeout=600 ../pelican/content/ipynb/14-day-incidence-germany.ipynb
python -m nbconvert --execute --inplace --ExecutePreprocessor.timeout=600 ../pelican/content/ipynb/14-day-incidence.ipynb
python -m nbconvert --execute --inplace --ExecutePreprocessor.timeout=600 ../pelican/content/ipynb/2020-are-summer-holidays-triggering-rising-cases.ipynb

# The incidence rate pages have period and case encoded in the URL, but we want
# a generic link available to these pages, so here we make a symlink to allow
# for a generic url:
cd ../wwwroot
rm -f ./germany-incidence-rate.html
ln -s ./germany-incidence-rate-7day-50cases.html ./germany-incidence-rate.html || true
rm -f ./countries-incidence-rate.html
ln -s ./countries-incidence-rate-7day-50cases.html ./countries-incidence-rate.html|| true
cd $scriptDir
