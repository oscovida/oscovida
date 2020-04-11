Software engineering: things to do
==================================

General
-------

-   \[ \] PEP8 coronavirus.py (and other files)
-   \[ \] write test that attempts to generate plots for all countries
    in Johns Hopkins data
-   \[ \] write test that attempts to generate plots for all countries
    in RKI data
-   \[ \] unit tests
-   \[ \] set up basic continuous integration (Travis?)
    -   possible system test could be
        -   \[ \] running of `overview` function for a number of
            countries
        -   \[ \] populating html from
            template-country.ipynb/template-germany.ipynb for a few
            countries /regions
-   \[ \] tidy up code
    -   \[ \] function names, interfaces, documentation
        -   for example rename data fetch and get functions according to
            where the data comes from
    -   \[ \] split plotting routines into (i) calculation of entities, and 
            (ii) plotting

Webpage generation
------------------

-   \[ \] add binderlink to index page (something like \"binder\" behind
    each entry?)
-   \[ \] style webpages
    -   more modern font?
    -   with PaNOSC logo
    - partly done with pelican
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
-   \[ \] make webpage generation faster
    -   takes about one hour at the moment (\~8 seconds per page, in
        total about 180+410 \~ 600 pages)
    -   can we parallelise?
-   \[ \] make webpage generation into a service (cronjob?) to run once
    a day and update webpages automatically
-   \[ \] document and refactor everything

Bugs
====

-   \[ \] adjust plot size to make sure headline shows in svg/pdf files
    when saved
-   \[ \] the daily changes in log scale plot shows strips in
    y-direction, for example
    <https://fangohr.github.io/coronavirus/Germany-Baden-W%C3%BCrttemberg-LK-Alb-Donau-Kreis.html>
    What is this? (accidentally dropping rows inplace?)
-   \[ \] Pelican rendering: tag links in
    https://fangohr.github.io/coronavirus/germany.html don't work (needs to use
    absolute URL in pelicanconf.py? Path is wrong by "coronavirus")

Functionality
=============

-   \[ \] use plotly instead of matplotlib for more interactive
    experience in static html?
-   \[ \] The Johns Hopkins data has regional data for some countries (UK,
    France, US). Where available, it would be good to show those as regions, in
    addition to one page that shows a sum of all of these numbers.
-   \[ \] for tables in country over view pages, drop the rows with zeros at the beginning.

See also [ideas.md](ideas.md).

Low priority / crazy?
=====================

-   \[ \] select data set by clicking on landkreis? (possible? Use
    voila?)

