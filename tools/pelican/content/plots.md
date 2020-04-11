Title: Standard Plots
Date: 2020-04-09 19:00
category: About
slug: plots
tags: data, plots


We discuss the plots from the top (number 1) to the bottom (number 7) that are
available for [every country](pages/world).

### Plot 1: accumulated cases and deaths as function of time

![south-korea data]({attach}fig-south-korea1.png)

* Shows how many people have been confirmed to be infected (blue) or have died (red) as a function of time.
* The y-axis is logarithmic, that means from one grid line to the next, the
  value represented increases by a factor of 10. (Axis labels: 10<sup>2</sup>=
  100, 10<sup>3</sup>= 1000, 10<sup>4</sup>= 10000, and so on).
* These numbers are generally reported in the media.
* These numbers can only grow.
* The interesting question is: how fast do they grow?

### Plot 2: daily changes in cases
![south-korea data]({attach}fig-south-korea2.png)

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
![south-korea data]({attach}fig-south-korea3.png)

* Red bars shows how many new deaths were reported for each day.
* Red line shows a seven day (rolling) average over the bar data.
* The number of deaths is expected to follow the number of infections with some
  time delay, and reduced by a fraction (the [case fatality
  rate](https://en.wikipedia.org/wiki/Case_fatality_rate)).

### Plot 4: growth factors
![south-korea data]({attach}fig-south-korea4.png)

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
![south-korea data]({attach}fig-south-korea5.png)

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
![south-korea data]({attach}fig-south-korea6.png)

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
![south-korea data]({attach}fig-south-korea7.png)

* As Plot 6, but for deaths not cases. For South Korea, there are not enough
  deaths per day to show a meaningful line here.



