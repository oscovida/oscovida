#!/usr/bin/env bash

# CD to this scripts directory
scriptDir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")
cd $scriptDir

# Paths should be relative to where this script is
jupyter-nbconvert ../generate-individiual-plots.ipynb --execute
jupyter nbconvert --ExecutePreprocessor.timeout=600 --inplace --to notebook --execute ../pelican/content/ipynb/14-day-incidence-germany.ipynb
jupyter nbconvert --ExecutePreprocessor.timeout=600 --inplace --to notebook --execute ../pelican/content/ipynb/14-day-incidence.ipynb
