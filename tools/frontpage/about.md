
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/oscovida/oscovida/master?filepath=index.ipynb)

Dashboard: [![Voila](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/oscovida/oscovida/master?urlpath=voila%2Frender%2Fdashboard.ipynb)

# Coronavirus 2020 - how effective are our measures to slow down the virus?

## Available materials

* [Plots and basic data tables for all countries for which the Johns Hopkins University provides data](https://fangohr.github.io/coronavirus/index-world.html)

* [Plots and basic data tables for all "Kreise" in Germany (based on data from Robert Koch Institute)](https://fangohr.github.io/coronavirus/index-germany.html)

* Selected Plots for strongly affected countries (discussion below), see
[index.ipynb](https://github.com/oscovida/oscovida/blob/master/index.ipynb)
([faster version if it works](https://nbviewer.jupyter.org/github/oscovida/oscovida/blob/master/index.ipynb))

* An example plot for South Korea is shown below, followed by a brief discussion/description of the different plots.

* All of the plots and tables can be recomputed using the Binder service (link
  in each webpage, or use [go here and select the relevant notebook
  yourself](https://mybinder.org/v2/gh/fangohr/coronavirus/master).

## Data source and processing

- We use data 
  from the [Johns Hopkins university](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data)
  for countries, 
- and from the [German Robert Koch Insitute (RKI)](https://npgeo-corona-npgeo-de.hub.arcgis.com/)
  for data within Germany.
- All computational steps and code are available [here](https://github.com/oscovida/oscovida/blob/master/oscovida.py) -- contributions and corrections welcome.

## Motivation

### Understanding the situation

The reporting in the media on the #COVID19 situation is not always providing
sufficient context to interpret the numbers: we hear many news reports about how
many people have been confirmed to be infected by the virus, or have died on a
particular day.

The relevant questions are though: how do these numbers compare to yesterday,
and the week before? Can we see and understand how quickly infections are
spreading? Can we see if the containment measures of people staying at home,
schools and universities closing etc are showing any effect and if so, how
strong is it? What can we learn from countries that have managed to reduce the
number of new infections? 

With the plots and data available here, we hope to contribute to this.

Discussion and contributions are welcome.

### Preparing for later stages of the outbreaks

Once the epidemic growth of infections is brought under control, we will need to
find a fine balance between measures (such as social distancing, closure of
schools, restaurants, shops, etc) and permitting work and live as was possible
before the pandemic to avoid repeated exponential growth of infections. 

We can start to see this in the data for countries such as China and South
Korea. We need to learn to better read these data. It will be essential to
monitor such indicators for some time (months or years?) to come.

### Enable citizen science

* The [source code](https://github.com/oscovida/oscovida) that creates
  the plots is available here, can be inspected, downloaded, modified and
  improved.

* Using [Jupyter Notebooks](https://jupyter.org/) and the [MyBinder
  project](https://mybinder.org) project, anyone with a web browser can execute
  the source (to create the same or new plots) from within a web browser, by
  clicking [this link](https://mybinder.org/v2/gh/fangohr/coronavirus/master).

## Plans and contributions

Contributions are welcome

* We gather some [ideas](https://github.com/oscovida/oscovida/blob/master/ideas.md) for further analysis and features that would be nice
  or useful.

* For those with programming and software engineering skills, there is a
  document [info.md](https://github.com/oscovida/oscovida/blob/master/info.md) with
  more details about the project and a [todo list](https://github.com/oscovida/oscovida/blob/master/todo.md).

* Bugs and ideas can be reported as a ["New issue"](https://github.com/oscovida/oscovida/blob/master/issues) -- a github
  account is necessary.

# Discussion of example plots

![south-korea data](figures/Korea--South.svg)
![south-korea data 2](figures/Korea--South2.svg)

* Discussion of plots from the top (number 1) to the bottom (number 7)

### Plot 1: accumulated cases and deaths as function of time
* Shows how many people have been confirmed to be infected (blue) or have died (red) as a function of time.
* The y-axis is logarithmic, that means from one grid line to the next, the
  value represented increases by a factor of 10. (Axis labels: 10<sup>2</sup>=
  100, 10<sup>3</sup>= 1000, 10<sup>4</sup>= 10000, and so on).
* These numbers are generally reported in the media.
* These numbers can only grow.
* The interesting question is: how fast do they grow?

### Plot 2: daily changes in cases
* Shows how many new confirmed cases are reported per day, shown as blue bars.
* Blue lines shows a seven day (rolling) average over the bar data - this
  produces smoother data, and in particular removes the effect of the weekend
  (in some countries reported numbers drop during and just after the weekend)
* We would like to see these numbers of daily changes decrease from day to day.
  The faster they go down the better. 
* For the data of South Korea, we can see that the peak of new infections was
  around 1st March 2020, and following that the number of new infections
  decreased to around 100 per day for the second half of March.

### Plot 3: daily changes in deaths
* Red bars shows how many new deaths were reported for each day.
* Red line shows a seven day (rolling) average over the bar data.
* The number of deaths is expected to follow the number of infections with some
  time delay, and reduced by a fraction (the [case fatality
  rate](https://en.wikipedia.org/wiki/Case_fatality_rate)).

### Plot 4: growth factors
* The growth factor is the ratio of new cases (or deaths) today relative to new
  cases (or deaths) yesterday
* Blue (red) dots show these ratios for cases (deaths), and are computed as the
  ratio over a week to reduce noise
* The solid line is a 7-day rolling mean over these points to provide smoother data.
* As long as the growth value is greater than 1.0, the number of new infections
  is increasing
* If the growth value would is exactly 1.0, we have the same number of new
  infections every day
* The growth factor needs to be below 1.0 for the spread to slow down.
* As this number is computed on the relative change from yesterday to today, we
  can get high fluctuations where the numbers of new cases and deaths is small
  (imagine there was 1 case yesterday, and 7 cases today, this would give a
  growth factor of 7). 

### Plot 5: Doubling times
* This plot computes the doubling time of the cases (blue) and deaths (red),
  assuming that the growth of cases and deaths as shown in plot 1 is
  exponential.
  
  * in more detail, we compute the doubling period from one day to the next and
    show this as transparent dots.
    
    If a value of 3 is shown, this means that at that point in time, it took 3
    days for the numbers of cases (or deaths) to double.
     
  * the solid line is a 7-day rolling mean over these data points and provides
    more robust guidance.
    
* Looking at the solid lines, we may be able to assess the spread of the virus. 

  * For many countries, in the early stages of the outbreak, this doubling time
    for confirmed infections (blue line) is somewhere around 2 to 3 days.
  
  * As the spread of infections is reduced (by schools closing, people
    exercising social distancing, staying at home, etc), the growth rate of the
    exponential function becomes smaller, and correspondingly the doubling time 
    increases. 
    
  * We would like to see the doubling time to get larger, as this an indication
    that the growth of infections and deaths is decreasing.
  
  * Hopefully, we can learn from other countries, what kind of doubling period
    has to be achieved, to control the number of infected people.
  
* The example data for South Korea shows that the doubling time grows from
  around 3 days to around 60 days as the number of daily new infections (plot 2)
  decreases.
  
  * as the doubling period reaches 60, the number of daily new infections
    stabilises around 100.
    
  * There is no red curve for the doubling time of deaths as there have
    been too few deaths to be useful for the analysis.


### Plot 6: Comparison of daily new cases with other countries

* X-axis shows the number of days since a particular number of new cases per day
  (such as 10) have occurred in that country, and the y-axis the number of new
  cases for that day.
  
* We see that countries follow similar paths, with the common properties that
  the curve increases until the number of cases per day peaks, and then the
  curve comes down again.
  
* The y-axis is logarithmic.

* Due to the logarithmic y-axis, this visualisation can help to understand at
  what stage in the outbreak an area is (despite the different size of the
  countries and numbers of cases).
  
* The curve shows as 7-day rolling mean to provide a smoother line than the
  noisier individual data points (in particular with fewer cases per day). This
  leads to non-integer values.
  
### Plot 7: Comparison of daily new deaths with other countries

* As Plot 6, but for deaths not cases. For South Korea, there are not enough
  deaths per day to show a meaningful line here.


# What about errors in the data?

* The data we have available is likely to be in accurate:
  - Infections can only be confirmed if they are being tested: the more testing
    takes place, the more infected people can be found. Asymptomatic individuals
    may not be tested if tests are prioritised for severely sick, health workers
    or those showing symptoms.
  - Tests may be inaccurate and report false positives or false negatives.
  - Deaths may be easier to detect than infections, but may also be inaccurate.
  - The reporting of cases and deaths may not take place during weekends, or
    there may be delays for other reasons.
  
* Despite the errors in the data, we can try to learn something from it as long
  as we remember the data is not representing the full truth of the situation
  but just the measurement that we have available.
  
  * For some plots, we have omitted data lines or points because there were not
    enough numbers and data points to estimate anything.
    
  * Some data points appear random or as outliers - for some we understand the
    reasons, for others not.
    
* It is possible we have made errors in our processing of the numbers. The
  source code is available for anyone to check. (Please feedback any
  observations.)



# Disclaimer

The plots and code here has been put together by volunteers who have no training
in epidemiology. THere are likely to be errors in the processing. You are welcome
to use the material at your own risk. The [license is available](https://github.com/oscovida/oscovida/blob/master/LICENSE).


# Acknowledgements

- Johns Hopkins University provides data for countries
- Robert Koch Institute provides data for within Germany
- Open source and scientific computing community for the data tools
- Github for hosting repository and html files
- Project Jupyter for the Notebook and Binder service
- The H2020 project Photon and Neutron Open Science Cloud ([PaNOSC](https://www.panosc.eu/))
