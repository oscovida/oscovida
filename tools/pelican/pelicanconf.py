#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'OSCOVIDA team'
SITENAME = 'OSCOVIDA: Open Science COVID Analysis'
SITEURL = 'https://oscovida.github.io'

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
LINKS = (("PaNOSC project", "https://panosc.eu"),
         )
         # ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('PaNOSC', 'https://twitter.com/Panosc_eu'),
          ('ProfCompMod', 'https://twitter.com/ProfCompMod'))
          #('Email','oscovidaproject@gmail.com'))
#          ('Open Science COVID Analysis', 'https://twitter.com/OSCOVIDAproject'))

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

TAGS_SAVE_AS = 'tags/index.html'
CATEGORIES_SAVE_AS = 'categories/index.html'
ARCHIVES_SAVE_AS = 'archives/index.html'


COPYRIGHT = """You are welcome to share and use the materials here. See <a href="http://oscovida.github.io/license.html">license</a> for details."""

COPYRIGHT = """Unless contrary mentioned, the content of this site is published under a <a rel='license'
href='https://creativecommons.org/licenses/by/4.0/'>Creative Commons
Attribution 4.0 International license</a>. See <a href="http://oscovida.github.io/license.html">license</a> for details."""

# The software is licensed under  <a href="https://github.com/fangohr/coronavirus-2020/blob/master/LICENSE">BSD 3-clause license</a>.

DISCLAIMER = """Plots, data and software here are provided <a href="https://github.com/fangohr/coronavirus-2020/blob/master/LICENSE#L20">as-is without any warranties</a> by volunteers. Use the material at your own risk. See <a href="http://oscovida.github.io/license.html">license</a> for details."""





