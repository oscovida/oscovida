Software engineering: things to do
==================================

General
-------

-   \[ \] PEP8 coronavirus.py (and other files)
-   \[X\] write test that attempts to generate plots for all countries
    in Johns Hopkins data -> `tools/test-plots-for-all-regions.ipynb`
-   \[X\] write test that attempts to generate plots for all countries
    in RKI data -> `test-plots-for-all-regions.ipynb`
-   \[ \] unit tests
-   \[X\] turn python code into package
-   \[ \] set up basic continuous integration (Travis?)
    -   possible system test could be
        -   \[X\] running of `overview` function for a number of
            countries
        -   \[ \] populating html from
            template-country.ipynb/template-germany.ipynb for a few
            countries /regions
        -   \[X\] set up travis
-   \[ \] tidy up code
    -   \[ \] function names, interfaces, documentation
        -   for example rename data fetch and get functions according to
            where the data comes from
    -   \[ \] split plotting routines into (i) calculation of entities, and 
            (ii) plotting
-   \[ \] make python package available via pip - what name? coronavirus? oscovida?
-   \[ \] tidy up urls: german URLS are sanitised (using sanitise() but world countries are not)
    - watch link to automatic figure creation in generate-individual-plots.ipynb

Webpage generation
------------------

-   \[ \] add binderlink to index page (something like \"binder\" behind
    each entry?)
-   \[ \] style webpages
    -   \[X\] more modern font?
    -   \[ \] with PaNOSC logo
-   \[ \] Germany: add overview plots for each Bundesland:
    -   For Hamburg, there is only one entry in the table (Hamburg, SK
        Hamburg), so we have this
    -   Would be nice to get a similar summary for Bayern
        -   getting the data is easy: we can use germany~getregion~()
            which will take the sum automatically if no subregion is
            provided
        -   the task is to integrate this into the index-germany.html
            file
            -   probably best at the beginning of
                <https://fangohr.github.io/coronavirus/index-germany.html>
                as a separate section \"Overview Bundeslaender\"
-   \[X\] make webpage generation faster
    -   takes about one hour at the moment (\~8 seconds per page, in
        total about 180+410 \~ 600 pages)
    -   can we parallelise?
-   \[ \] make webpage generation into a service (cronjob?) to run once
    a day and update webpages automatically
-   \[ \] document and refactor everything
-   \[ \] Embed google analytics snippet in html of notebooks (in `html/*`)

Binder
-------
-   \[ \] split Binder repository for ipynb files from html repository:
    - html repo is pretty big, poor binder needs to clone this every time it is used
-   \[ \] remove inconsolata font from coronavirus.py, or install in binder (so
    that no font warning is reported when executing the notebook on binder)

Bugs
----

-   \[X\] adjust plot size to make sure headline shows in svg/pdf files
    when saved -> latest matplotlib version seems to do this automatically
-   \[ \] the daily changes in log scale plot shows strips in
    y-direction, for example
    <https://fangohr.github.io/coronavirus/Germany-Baden-W%C3%BCrttemberg-LK-Alb-Donau-Kreis.html>
    What is this? (accidentally dropping rows inplace?)
-   \[X\] Pelican rendering: tag links in
    https://fangohr.github.io/coronavirus/germany.html don't work (needs to use
    absolute URL in pelicanconf.py? Path is wrong by "coronavirus")

Functionality
------------

-   \[ \] for tables in country over view pages, drop the rows with zeros at the beginning. [HIGH, SMALL]
-   \[ \] show states for Germany in beginning of https://fangohr.github.io/coronavirus/germany.html [HIGH
-   \[ \] The Johns Hopkins data has regional data for some countries (UK,
    France, US). Where available, it would be good to show those as regions, in
    addition to one page that shows a sum of all of these numbers.) [HIGH]
-   \[ \] offer links to detailes pages for countries / regions with highest numers
-   \[ \] make lines smoother, for example growth, doubling time
    -  \[ \] base data on integrated feature (for example smoothed line for daily cases), rather that day-to-day values which fluctuate
    -  \[ \] allow rolling averages if some data points are missing
-   \[ \] use plotly instead of matplotlib for more interactive
    experience in static html?
-   \[X\] decide on name for project and host somewhere more official (Hans) [HIGH]


Web page content
======================

- \[X\] add license for content and code
- \[X\] add data from other countries


See also [ideas.md](ideas.md).

Low priority / crazy?
=====================



