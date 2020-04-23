Standard Plots
==============

:Date: 2020-04-09 19:00
:slug: plots
:tags: About, Data, Plots

We discuss the plots from the top (number 1) to the bottom (number 7)
that are available for `every country <world.html>`__.

Plot 1: accumulated cases and deaths as function of time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <img src="{attach}fig-south-korea1.svg" alt="South Korea data">

-  Shows how many people have been confirmed to be infected (blue) or
   have died (red) as a function of time.
-  The y-axis is logarithmic, that means from one grid line to the next,
   the value represented increases by a factor of 10. (Axis labels: 102=
   100, 103= 1000, 104= 10000, and so on).
-  These numbers are generally reported in the media.
-  These numbers can only grow.
-  The interesting question is: how fast do they grow?

Plot 2: daily changes in cases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <img src="{attach}fig-south-korea2.svg" alt="South Korea data">

-  Shows how many new confirmed cases are reported per day, shown as
   blue bars.
-  Blue lines show a seven day (rolling) average over the bar data
   (using a Gaussian window with a standard deviation of 3 days) - this
   produces smoother data. It also helps to remove the effect of the
   weekend (in some countries reported numbers drop during and just
   after the weekend)
-  We would like to see these numbers of daily changes decrease from day
   to day. The faster they go down the better. Ideally their reach 0.
-  For the data of South Korea, we can see that the peak of new
   infections was around 1st March 2020, and following that the number
   of new infections decreased to around 100 per day for the second half
   of March, before the numbers started to decrease further.

Plot 3: daily changes in deaths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <img src="{attach}fig-south-korea3.svg" alt="South Korea data">


-  Red bars shows how many new deaths were reported for each day.
-  Red line shows a seven day (rolling) average over the bar data.
-  The number of deaths is expected to follow the number of infections
   with some time delay, and reduced by a fraction (the `case fatality
   rate <https://en.wikipedia.org/wiki/Case_fatality_rate>`__).

Plot 4: growth factors
~~~~~~~~~~~~~~~~~~~~~~


.. raw:: html

    <img src="{attach}fig-south-korea4.svg" alt="South Korea data">


-  The growth factor is the ratio of new cases (or deaths) today
   relative to new cases (or deaths) yesterday
-  Blue (red) dots show these ratios for cases (deaths), and are
   computed based on the smoothed data shown in plot 2 and 3.
-  The solid line is a 7-day rolling mean over these points to provide
   smoother data.
-  As long as the growth value is greater than 1.0, the number of new
   infections is increasing.
-  If the growth value is exactly 1.0, then we have the same number of
   new infections every day.
-  The growth factor needs to be below 1.0 for the spread to slow down.
-  As the growth factor does not depend on the total number of new
   cases/deaths (but only on the relative change from yesterday to
   today), we can get high fluctuations where the numbers of new cases
   and deaths is small (imagine there was 1 case yesterday, and 7 cases
   today, this would give a growth factor of 7). In short: where the
   number of daily new cases/deaths is small, the growth factor can
   appear to change quickly.
-  **We can use the growth factor as a measure of success for the virus
   containment**: as long as the growth factor is below 1.0, the spread
   is slowing down. If the growth factor is greater than one, the number
   of newly infected people is increasing from day to day; this must be
   avoided.

Plot 5: Doubling times
~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <img src="{attach}fig-south-korea5.svg" alt="South Korea data">

-  This plot computes the doubling time of the cases (blue) and deaths
   (red), assuming that the growth of cases and deaths as shown in plot
   1 is exponential.

   -  In more detail, we compute the doubling period from one day to the
      next and show this as transparent dots.

      If a value of 3 is shown, this means that at that point in time,
      it took 3 days for the numbers of cases (or deaths) to double.

   -  The solid line is a 7-day rolling mean over these data points and
      provides more robust guidance.

-  Looking at the solid lines, we may be able to assess the spread of
   the virus.

   -  For many countries, in the early stages of the outbreak, this
      doubling time for confirmed infections (blue line) is somewhere
      around 2 to 3 days.

   -  As the spread of infections is reduced (by schools closing, people
      exercising social distancing, staying at home, etc), the growth
      rate of the exponential function becomes smaller, and
      correspondingly the doubling time increases.

   -  We would like to see the doubling time to get larger, as this an
      indication that the growth of infections and deaths is decreasing.

   -  Hopefully, we can learn from other countries, what kind of
      doubling period has to be achieved, to control the number of
      infected people.

-  The example data for South Korea shows that the doubling time grows
   from around 3 days to around 60 days as the number of daily new
   infections (plot 2) decreases.

   -  as the doubling period reaches 60, the number of daily new
      infections stabilises around 100.

   -  There is no red curve for the doubling time of deaths as there
      have been too few deaths to be useful for the analysis.

Plot 6: Comparison of daily new cases with other countries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <img src="{attach}fig-south-korea6.svg" alt="South Korea data">


   south-korea data

-  X-axis shows the number of days since a particular number of new
   cases per day (such as 10) have occurred in that country, and the
   y-axis the number of new cases for that day.

-  We see that countries follow similar paths, with the common
   properties that the curve increases until the number of cases per day
   peaks, and then the curve comes down again.

-  The y-axis is logarithmic.

-  Due to the logarithmic y-axis, this visualisation can help to
   understand at what stage in the outbreak an area is (despite the
   different size of the countries and numbers of cases).

-  The curve shows as 7-day rolling mean to provide a smoother line than
   the noisier individual data points (in particular with fewer cases
   per day). This leads to non-integer values.

Plot 7: Comparison of daily new deaths with other countries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <img src="{attach}fig-south-korea7.svg" alt="South Korea data">

-  As Plot 6, but for deaths not cases. For South Korea, there are not
   enough deaths per day to show a meaningful line here.
