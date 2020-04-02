[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fangohr/coronavirus-2020/master?filepath=index.ipynb)

# COVID2019 - how effective are our measures to slow down the virus?

## Available materials

* Plots (discussion to be added), see [index.ipynb](https://nbviewer.jupyter.org/github/fangohr/coronavirus-2020/blob/master/index.ipynb) and scroll down, an example for South Korea is shown below

* Jupyter notebooks that create these plots and make the data available in pandas dataframes.

* Ability to [execute the notebooks in the cloud, to modify them, or inspect the trends in other countries](https://nbviewer.jupyter.org/github/fangohr/coronavirus-2020/blob/master/index.ipynb) and scroll down, an example for South Korea is shown below)

## Data source

- We use [data](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data) from the Johns Hopkins university 

## Motivation

### Understanding the situation

The reporting in the media on the #COVID19 situation is often not providing
sufficient context to interpret the numbers: During March and April, we hear
many reports about how many people have been confirmed to be infected by the
virus, or have died. The relevant questions are though: how do these numbers
compare to yesterday, and the week before? Can we see if the containment
measures of people staying at home, schools and universities closing etc are
showing any effect and if so, how strong is it? What can we learn from countries
that have managed to reduce the number of new infections?

With the plots and data available here, we hope to contribute to this.

Discussion and contributions are welcome.

### Enable citizen science

* The [source code](https://github.com/fangohr/coronavirus-2020) that creates the plots is available here, can be inspected, downloaded, modified and improved.

* Using Jupyter Notebooks and the https://mybinder.org project, anyone with a webbrowser can execute the source (to create the same or new plots) from within a webbrowser, by clicking [this link](https://nbviewer.jupyter.org/github/fangohr/coronavirus-2020/blob/master/index.ipynb).

## Plans

* Extend this to provide data for Landkreise within Germany

* Further plots to compare progress of the virus in different regions

* Make plots more interactive (plotly?)

## Discussion of example plots

![south-korea data](figures/Korea--South.svg)

* Discussion of plots from the top (number 1) to the bottom (number 4)

### Plot 1: accumulated cases and deaths as function of time
* shows how many people have been confirmed to be infected as a function of time 
* y-axis is logarithmic
* these numbers are generally reported in the media
* they can only grow 
* the interesting question is: how fast do they grow

### Plot 2: daily changes in cases
* shows how many new confirmed cases are reported per day, shown as bars
* blue lines shows a seven day (rolling) average over the bar - this produces smoother data, and in particular
  removes the effect of the weekend which seems to affect reporting of numbers in some countries
* [want to see this going down]

### Plot 3: daily changes in deaths
* shows how many new deaths were reported each day
* red lin shows a seven day (rolling) average over the bar - this produces smoother data, and in particular
  removes the effect of the weekend which seems to affect reporting of numbers in some countries
* [mention delay to infections]

### Plot 4:
* to be written
