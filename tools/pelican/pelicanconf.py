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
         ('You can modify those links in your config file', '#'),)

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
