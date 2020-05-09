Title: Frequently Asked Questions (FAQ)
Date: 2020-04-09 19:00
slug: faq
tags: Data, About, FAQ


# What about errors in the data?

* The data we have available is likely to be inaccurate:
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
  
  - For some plots, we have omitted data lines or points because there were not
    enough numbers and data points to estimate anything.
    
  - Some data points appear random or as outliers - for some we understand the
    reasons, for others not.
    
* It is possible we have made errors in our processing of the numbers. The
  source code is available for anyone to check. (Please feedback any
  observations.)

# How do you justify the smoothing of the data?

Smoothing is carried out by introducing a rolling mean (or [moving
average](https://en.wikipedia.org/wiki/Moving_average)) over a particular time
window. By doing this we reduce the influence of short-term fluctuations and
help to emphasise phenomena that take place over longer periods of time.

In the COVID19 numbers treated here, we often use an moving average over 7 days.
The underlying assumption is that the natural time time scale of changes in the
infection rate is of the order of weeks (i.e. longer than the interval over
which we average). The choice of 7 days has the additional advantage that we
always all days of the week: in many countries the reported infections and
deaths fluctuate within a week (for example with a reduction of reported cases
during the weekend or in the beginning of the week). By averaging over a whole
week, we can suppress that systematic variation. The infections [in
Germany](html/Germany.html) show such oscillations with a frequency of a week.

