#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://oscovida.github.io/'
RELATIVE_URLS = True

FEED_ALL_ATOM = 'feeds/all.atom.xml'
# next line raises error when running 'make publish'
# CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "oscovida"
#GOOGLE_ANALYTICS = ""
GOOGLE_ANALYTICS="UA-163845056-1"
