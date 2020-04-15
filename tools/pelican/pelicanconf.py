#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'OSCA team'
SITENAME = 'OSCA (Open Science COVID19 Analysis)'
SITEURL = 'https://fangohr.github.io/coronavirus'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

OUTPUT_PATH = "../wwwroot"

# Blogroll
LINKS = (("PaNOSC project", "http://panosc.eu"),
         )
         # ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('PaNOSC', 'https://twitter.com/Panosc_eu'),
          ('ProfCompMod', 'https://twitter.com/ProfCompMod'))          

DEFAULT_PAGINATION = False

STATIC_PATHS = ['content/pages']
# ARTICLE_PATHS = ['content']

# THEME = "/Users/fangohr/pelican-themes/bootstrap2"
THEME = "themes/plumage"

#DISPLAY_CATEGORIES_ON_MENU = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# HF: Relative URLS: this seems to work; needs more testing

LOAD_CONTENT_CACHE = False

# See
# https://github.com/kdeldycke/kevin-deldycke-blog/blob/master/pelicanconf.py
# for more config options for the plumage theme
# Taken from there:

# Deactivate author URLs
AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False

COPYRIGHT = """Add License"""

DISCLAIMER = """Plots, data and software here has been put together by volunteers who have
no training in epidemiology. There are likely to be errors in the processing.
You are welcome to use the material at your own risk. The
<a href='https://github.com/fangohr/coronavirus-2020/blob/master/LICENSE'> license is
available</a>."""

# """Unless contrary mentioned, the content of this site is published
# under a <a rel='license'
# href='https://creativecommons.org/licenses/by-nc-sa/4.0/'>Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International license</a>."""
