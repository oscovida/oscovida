#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'OSCOVIDA team'
SITENAME = 'OSCOVIDA: Open Science COVID Analysis'
SITEURL = 'https://oscovida.github.io'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'


USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = "All"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = [("Home", "index.html"),
             ("All regions", "all-regions.html"),
             ("Countries", "countries.html"),
             ("Germany", "germany.html"),
             ("US", "us.html"),
             ("Hungary", "hungary.html"),
             ("Articles", "category-all.html"),
             ("Analysis", "tag-analysis"),
             ("About", "tag-about.html")]

OUTPUT_PATH = "../wwwroot"


# Blogroll
FAVICON_LINKS = False  # Favicon retrieval is broken (HF, April 2020)
LINKS = (("OSCOVIDA project", "http://oscovida.github.io"),
         ("PaNOSC project", "http://www.panosc.eu"),
         ('OSCOVIDA', 'mailto:oscovidaproject@gmail.com'), )
         # ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Open Science COVID Analysis', 'https://twitter.com/OSCOVIDAproject'),
          ('PaNOSC', 'https://twitter.com/Panosc_eu'),
          ('ProfCompMod', 'https://twitter.com/ProfCompMod'))
          #('Email','oscovidaproject@gmail.com'))

DEFAULT_PAGINATION = False

STATIC_PATHS = ['content/pages', 'content/news', 'content/ipynb']
# ARTICLE_PATHS = ['content']

# THEME = "/Users/fangohr/pelican-themes/bootstrap2"
THEME = "themes/plumage"

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Plugins (follow guidance https://janakiev.com/blog/pelican-jupyter/)
MARKUP = ('md', 'rst', 'ipynb')

from pelican_jupyter import markup as nb_markup
PLUGINS = [nb_markup]

IGNORE_FILES = [".ipynb_checkpoints"]  
# HF: Relative URLS: this seems to work; needs more testing

LOAD_CONTENT_CACHE = False

# See
# https://github.com/kdeldycke/kevin-deldycke-blog/blob/master/pelicanconf.py
# for more config options for the plumage theme
# Taken from there:

# Deactivate author URLs
AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False

# Define where to save Tags, and categories
# Use of subdirectories can link to confusion when following links within the webpage,
# so we stick to a one directory level scheme here for now.
TAG_SAVE_AS = 'tag-{slug}.html'
TAG_URL = 'tag-{slug}.html'
CATEGORY_SAVE_AS = "category-{slug}.html"
CATEGORY_URL = "category-{slug}.html"

# used by 'Browse content by', entry is omitted if set to False (see
# themes/plumage/templates/base.html)
ARCHIVES_SAVE_AS = 'archives-index.html'
TAGS_SAVE_AS = 'tags-index.html'
CATEGORIES_SAVE_AS = 'categories-index.html'
CATEGORIES_SAVE_AS = False

COPYRIGHT = """Unless contrary mentioned, the content of this site is published under a <a rel='license'
href='https://creativecommons.org/licenses/by/4.0/'>Creative Commons
Attribution 4.0 International license</a>. See <a href="http://oscovida.github.io/license.html">license</a> for details."""

DISCLAIMER = """Plots, data and software here are provided <a href="https://github.com/oscovida/oscovida/blob/master/LICENSE#L20">as-is without any warranties</a> by volunteers. Use the material at your own risk. See <a href="http://oscovida.github.io/license.html">license</a> for details."""





