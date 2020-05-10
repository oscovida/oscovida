# Pelican

## Installation

pip install pelican[markdown]

## set up

mkdir pelican
pelican-quickstart

Answers:

 Where do you want to create your new web site? [.] 
> What will be the title of this web site? Open Science COVID19 Tracker
> Who will be the author of this web site? OSCT team
> What will be the default language of this web site? [en] 
> Do you want to specify a URL prefix? e.g., https://example.com   (Y/n) n
> Do you want to enable article pagination? (Y/n) n
> What is your time zone? [Europe/Paris] 
> Do you want to generate a tasks.py/Makefile to automate generation and publishing? (Y/n) 
> Do you want to upload your website using FTP? (y/N) 
> Do you want to upload your website using SSH? (y/N) 
> Do you want to upload your website using Dropbox? (y/N) 
> Do you want to upload your website using S3? (y/N) 
> Do you want to upload your website using Rackspace Cloud Files? (y/N) 
> Do you want to upload your website using GitHub Pages? (y/N) 
Done. Your new project is available at /Users/fangohr/git/coronavirus-2020-pelican/tools/pelican



## use

make html

-> create static html

make regenerate (or make serve)

-> creates static html on demand, and serves pages at localhost:8000


# Pelican themes

## install

git clone --recursive https://github.com/getpelican/pelican-themes ~/pelican-themes


# Which files to place where?

- normal articles in `pelican/content`
- static pages in `pelican/content/pages`
- Jupyter Notebooks that should become an article in `pelican/content/ipynb`
  - files in there are automatically copied to ../wwwroot/ipynb as part of `make
    publish` (code in `publishconf.ipy``)

