"""Unified data hub for a better understanding of COVID-19.
For more information check README.md.

Reference: https://covid19datahub.io/

This is a fork of the covid19dh Python interface from here:
https://github.com/covid19datahub/Python

Changes made include:
- caching to disk
- setting dataframe index to the date
- black formatting
- type annotation
"""

from .main import *
from .cite import *
