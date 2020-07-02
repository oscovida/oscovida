Curve your city / country
=========================

Useful plots:

-   \[X\] total deaths in log scale
-   \[X\] total cases in log scale
-   \[X\] new cases per day (normal scale)
-   \[X\] new deaths per day (normal scale)
-   \[X\] doubling time on these plots
    -   based on day-to-day difference is probably too noisy
        -   average over last n days?
        -   or fit exponential function through n days to get one data
            point?
        -   rolling average works well
-   \[ \] also show data in numbers per million (or per 1000?) - needs
    population data (for Germany, this is probably available already in
    the downloaded table) -> https://github.com/oscovida/oscovida/issues/65
-   \[ \] show ratio of deaths to recorded cases?

Germany
-------

-   \[ \] show data split into age groups and gender
-   \[ \] check that sum over all states in Germany is similar to total
    data for Germany
-   \[X\] check metadata and our interpretation of data sets
-   \[ \] what other data is there from Robert Koch?

Other topics
============

-   fewer reported cases over the weekends? Often a dip on
    Sunday/Monday/Tuesday, at lest in Germany -\> Fourier transform to
    confirm? -> https://oscovida.github.io/2020-05-10-notebook-Weekly-fluctuations-in-data-from-Germany.html

-   Compare countries and strategies
    -   compare with China, Italy and other countries
        -   fit model function to china data, so we can fit it to other
            data and compare?
            -   sigmoidal

        -\> estimate total infect / deaths?
