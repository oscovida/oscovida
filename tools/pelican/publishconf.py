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
SITEURL = 'https://oscovida.github.io'
RELATIVE_URLS = True

FEED_ALL_ATOM = 'feeds/all.atom.xml'
# next line raises error when running 'make publish'
# CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = "oscovida"
#GOOGLE_ANALYTICS = ""
GOOGLE_ANALYTICS="UA-163845056-1"


########################


def inject_google_analytics_into_html_notebooks(GOOGLE_ANALYTICS):
    """embed google analytics script into html generated from notebooks

    (There are probably more elegant ways to do this when we convert from ipynb
    to html?)

    """

    # Google Analytics snippet from
    # https://developers.google.com/analytics/devguides/collection/analyticsjs

    snippet = """
    <!-- Google Analytics -->
    <script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', '""" + GOOGLE_ANALYTICS + """', 'auto');
    ga('send', 'pageview');
    </script>
    <!-- End Google Analytics -->"""

    files = os.listdir('../wwwroot/html')

    counter_injected = 0
    counter_untouched = 0
    print(f"Injecting Google Analytics snippet ... ", end="")
    for file in files:
        with open(os.path.join("../wwwroot/html", file), "tr") as f_in:
            content = f_in.read()

        # just a sanity check this is a file generated from a notebook
        nb_in_content = "<title>Notebook</title>" in content

        # we assume only one "</body>" in file
        body_correct_count = content.count("</body>") == 1

        # assume the snippet is not in there yet (in case we run this script
        # repeatedly)
        if (GOOGLE_ANALYTICS in content) or (not nb_in_content) or (not body_correct_count):
            # already injected
            counter_untouched += 1
        else:

            # if so, inject google analytics snippet before end of body:
            modified_content = content.replace("</body>", snippet + "\n</body>")

            with open(os.path.join("../wwwroot/html", file), "tw") as f_out:
                f_out.write(modified_content)

            counter_injected += 1

    assert len(files) == counter_untouched + counter_injected
    print(f"{counter_injected} files injected, " +
          f"and {counter_untouched} untouched")

# create html folder if it does not exist
os.system("mkdir -p ../wwwroot/html")

inject_google_analytics_into_html_notebooks(GOOGLE_ANALYTICS)



# copy notebooks from content/ipynb to ../wwwroot/ipynb
command = "rsync -auv content/ipynb/*ipynb ../wwwroot/ipynb"
print("Copy notebooks*ipynb from content/ipynb to wwwroot/ipynb:")
os.system(command)

