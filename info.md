Info on data sources, repository and software details
========================================================

Data for Germany from Robert Koch Institute
----------------------------------------------------

- From <https://npgeo-corona-npgeo-de.hub.arcgis.com/> -\> Menu top
  left -\> \"Data\", scroll down to \"RKI Corona Landkreise\" data
  set, -\> select interesting data set -\>
  - RKI Corona Bundesländer
  - RKI COVID19 -\>  "Download der Daten als CSV"
  - leading to this page: https://www.arcgis.com/home/item.html?id=f10774f1c63e40168479a1feb6c7ca74
  - there seem to be multiple options to get to the data. One of them is the "URL" in the rigth column,
  - which points to https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data

- outdated as of 6 June 2020:
  - Download button (below image, on the right) -\> Full Data set
    -\> Spreadsheet This provides a link to a csv file, but with a
    URL that includes a hash. As of 9 April, this is
    <https://opendata.arcgis.com/datasets/ef4b445a53c1406892257fe63129a8ea_0.csv>


Overall set up of directory structure and software
==================================================

Directory structure for repository
<https://github.com/oscovida/oscovida>:

oscovida (root dir of repository)
-----------------------------------------


- [info.md](info.md) : this file, provides overview of current setup
- [todo.md](todo.md) : things that need doing (programming/software
  engineering/data analysis)
- [ideas.md](ideas.md): things that could be done; might need some evaluation
  first
- [Dockerfile](Dockerfile): Dockerfile that allow execution of tests in
  container (could also be used for production)
- [Makefile](Makefile): useful targets for tests and installation


oscovida/oscovida
----------------------------

contains oscovida package as the source required to create the plots

- notebooks will import from this package
- this is the authoritative copy of the oscovida module


oscovida/tools
----------------------

contains tools to create static webpages at
<https://oscovida.github.io>, (repository to host webpages is
<https://github.com/oscovida/oscovida.github.io>)

in particular:

- generate-countries.ipynb Notebook that creates all the static
  webpages for the world, and Germany, and US states

- template-country.ipynb (used for world countries)
- template-germany.ipynb (used for Germany)
- template-US.ipynb (used for US states)

oscovida/tools/wwwroot
------------------------------

- rootdirectory of <https://oscovida.github.io/index.html> and
  repository

- files that are added to the repository
  <https://github.com/oscovida/oscovida>, and then pushed, will
  show up at <https://oscovida.github.io/index.html> a few minutes
  later

- we use a separate repository (I.e. different from code repo) out of
  fear that it may grow quickly in size. At that point, we can create
  a new repository under the same name, as the history is pretty
  irrelevant: this is only to serve the most recent data in static
  html files.

- The total size of html file for world and Germany is around 300MB,
  but the .git directory is smaller.

- files in the `html` directory are created from notebooks. The notebooks are
  stored in the `ipynb` subdirectory.

- The files committed to the webpages repository must contain the most recent
  `oscovida` in the `ipynb` subdirectory and `requirements.txt` as those
  are needed by binder to execute the notebooks.

- By also committing the `cachedir`, people don\'t need to re-fetch the
  data on the binder service (fetching of the German data set varies
  between 1s and 60 seconds).

oscovida/tools/oscovida.github.io
---------------------------------

This direcotory contains two files (``post-generate.sh`` and ``pre-generate,sh``)
which act as hooks to run commands before and after the website generation is ran
by the oscovida.github.io repository. Currently this is used to re-execute specific
individual notebooks every day alongside the report generation.

More information on how this works can be found in 
[the readme file in that directory](https://github.com/oscovida/oscovida/blob/master/tools/oscovida.github.io/readme.md)

oscovida/tools/wwwroot/ipynb
------------------------------------

Directory that keeps the files required for Binder, so that people can
re-execute notebooks.

Plan: create an extra repository just for these `*ipynb` files, so that creating
a container for Binder doesn't need to clone the big repository that contains
all the html files. This is realised with the next section:

oscovida/tools/binder
------------------------------

- repository <https://github.com/oscovida/binder>

- this started (24 May 2020) as a copy of the oscovida/tools/wwwroot/ipynb
  directory, but in a separate repository to make the binder start up time shorter
  (because this repo is faster to clone than the massive wwwroot one.)

- for now, we rsync everything from oscovida/tools/wwwroot/ipynb to
  oscovida/tools/binder/ipynb

  In the long run, we could consider to write ipynb files directly into the
  binder directory.

- The files committed to the webpages repository must contain the most recent
  `oscovida` in the `ipynb` subdirectory and `requirements.txt` and
  `apt.txt` as those are needed by binder to execute the notebooks.

- By also committing the `cachedir`, people don\'t need to re-fetch the data on
  the binder service (fetching of the German data set varies between 1s and 60
  seconds). The downside is that the data will grow stale over time.
  (At the moment, 25May 2020, we don't copy the cachedir into the binder directory.)


oscovida/tools/pelican
-----------------------------------

Base directory of Pelican (static html generator) package.

- run `make html` here to create html in `../wwwroot`. Use this for development.
- run `make publish` here to create html that is meant to be pushed to the
  website:
  - `make publish` executes the settings is `publishconf.py` after having
  executed `pelicanconf.py`. As such, we get absolute URL in feeds, we get
  feeds with links to new articles. It also adds the google analytics tracker
  that we don't want for development, and javascript to enable disqus. (Not
  sure if we want the latter, but we might as well set it up while there is no
  traffic on the page, and then deactivate if we don't want it.)

  `make publish` also copies `ipynb` files into the
  oscovida/tools/wwwroot/ipynb directory.

- the `generate-countries.ipynb` notebook creates files `germany.md` and
  `world.md` (and more) in pelican/contents

- `tools/pelican/contents`:
  - keeps markdown or rstfiles that pelican will turn into articles automatically

- `tools/pelican/contents/pages`:
  - keeps static files (such as the welcome page), will also be turned to html

- `tools/pelican/contents/ipynb`:
  - contains notebooks that are rendered as normal articles by pelican



oscovida/archive
------------------------

- files for history interest - can be removed soon. There were
  initially interesting to look up some things tried before.

oscovida/dev
--------------------

- collection of items that are work in progress or a useful reference for
  developers.


Setting up a local installation for development
===============================================

1. clone git@github.com:oscovida/oscovida.git into your chosen directory
   X. This provides the source code.

2. Get the repository that keeps the static webpages (using github pages)
   `cd tools && git clone git@github.com:oscovida/oscovida.github.io.git wwwroot`

3. Get the binder repository:
   `cd tools && git clone git@github.com:oscovida/binder.git binder`

Procedure to update data and webpages (manual)
==============================================

[see below for automatic version]

4. update notebooks by running (in X/tools):

  - the report_generators tool, see `python -m report_generators.cli --help` for
    help
  - `python3 -m report_generators.cli --regions=all --workers=max` updates all
    (~600) pages using with max workers

  - jupyter-notebook generate-individual-plots.html:
  - updates image on home page (with one country out of the top 10)
  - updates plots on https://oscovida.github.io/plots.html with current data

5. in X/tools/pelican, run ``make html` to update html pages (to develop), `make
   publish` for the final version

   - if you want to see results, use `make serve` and open `http://localhost:8000`

6. in `wwwroot`, run `git add *; git commit *`, then `git push`

7. updates should appear at https://oscovida.github.io a few minutes later

8. in `binder`, run `git add *; git commit *`, then `git push`

Procedure to update data and webpages (automatic)
=================================================

After pip-installing `oscovida`, cd to the `tools` directory, and from there you
can use the `report_generators` module to execute the notebooks.

The [GitHub Workflow](https://github.com/oscovida/oscovida.github.io/blob/master/.github/workflows/update-webpages.yml)
used to automatically generate the oscovida website can be used to see how to
manually generate it. The steps would be:

```
#  Set up repositories
git clone git@github.com/oscovida/oscovida
git clone git@github.com/oscovida/oscovida.github.io ./oscovida/tools/wwwroot

#  Set up environment
python -m venv .venv
source .venv/bin/activate
pip install .

#  Generate reports
pushd tools
python3 -m report_generators.cli --regions=all --force --workers=max --log-level=INFO --log-file=./wwwroot/report-gen.log
popd

#  Generate individual plots
pushd tools
jupyter-nbconvert generate-individiual-plots.ipynb --execute
popd

#  Update HTML pages
pushd tools/pelican
make publish
popd
```

You can save this as a script and run it, however generating the entire website
may take a while depending on your core count. If you are contributing to the
project you should use the `--debug` flag to only generate 10 reports per region
instead of all the 600+ reports.



Report Generators CLI Help
==========================

```
❯ python -m report_generators.cli --help
Usage: cli.py [OPTIONS]

  Command Line Interface used to batch-generate and execute Jupyter notebook
  reports for oscovida.

Options:
  -r, --regions [countries|germany|usa|hungary|all-regions-md|all]
                                  Region(s) to generate reports for.

  --workers TEXT                  Number of workers to use, `auto` uses
                                  nproc-2, set to 1 or False to use a single
                                  process.

  --wwwroot TEXT                  Root directory for www content.

  --create-wwwroot                Create wwwroot directory if it does not
                                  exist.

  --kernel-name TEXT              Create wwwroot directory if it does not
                                  exist.

  --disable-pbar                  Disable progress bar, print logging output
                                  instead.

  --log-level [CRITICAL|ERROR|WARNING|INFO|DEBUG]
                                  Log level.

  --log-file TEXT                 Log file path.

  --force                         Force notebook re-execution even if recently
                                  executed.

  --debug                         Enable debug mode, only generates reports
                                  for the first 10 regions and sets the log
                                  level to `INFO`.

  --help                          Show this message and exit.
```

Related resources
=================

-   <https://nextstrain.org/ncov>
-   Jupyter notebooks as templates: <https://covid19dashboards.com/> One
  of these is
  -   <https://covid19dashboards.com/compare-country-death-trajectories/>
    -   nice comparison of trajectories
      -   would be good to have per state or \'Landkreis\'
