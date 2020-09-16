#!/usr/bin/env bash

# CD to this scripts directory
scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")
cd $scriptDir

# Paths should be relative to where this script is
python -m nbconvert --execute --inplace ../generate-individiual-plots.ipynb
python -m nbconvert --execute --inplace --ExecutePreprocessor.timeout=600 ../pelican/content/ipynb/14-day-incidence-germany.ipynb
python -m nbconvert --execute --inplace --ExecutePreprocessor.timeout=600 ../pelican/content/ipynb/14-day-incidence.ipynb
python -m nbconvert --execute --inplace --ExecutePreprocessor.timeout=600 ../pelican/content/ipynb/2020-are-summer-holidays-triggering-rising-cases.ipynb
