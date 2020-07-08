Reproduction number 
===================

:date: 2020-05-03 10:00
:slug: reproduction-number
:tags: About, Data, Plots

A much more `detailed discussion is available here <r-value.html>`__.
   
Reproduction number R
#####################

- The `Reproduction number R (Wikipedia)
  <https://en.wikipedia.org/wiki/Basic_reproduction_number>`__ [1] expresses how
  many people are infected from one person with COVID19.

Computation of R from measured data
-----------------------------------

The bulletin from the Robert Koch institute [2] reports that an average
infectious period of $\tau = 4$ days is assumed. Based on that information, the
description of the method to compute $R$ is [3]

- compute an average $<n>_1$ of daily new infections over 4 days (say days 0 to 3)
- compute an average $<n>_2$ of daily new infections over 4 subsequent days (say days 4 to 7)
- compute the quotient $<n>_2 / <n>_1$ 

Then we repeat this as a sliding calculation for all subsequent days. This is
the current method used in OSCOVIDA.

A much more `detailed discussion of this calculation is available <r-value.html>`__.

References
----------

[1] https://en.wikipedia.org/wiki/Basic_reproduction_number

[2] [Robert Koch Institute: Epidemiologisches Bulletin 17 | 2020 23. April 2020](https://www.rki.de/DE/Content/Infekt/EpidBull/Archiv/2020/Ausgaben/17_20.html)

[3] "_Bei einer konstanten Generationszeit von 4 Tagen, ergibt sich R als Quotient der Anzahl von Neuerkran- kungen in zwei aufeinander folgenden Zeitabschnitten von jeweils 4 Tagen. Der so ermittelte R-Wert wird dem letzten dieser 8 Tage zugeordnet, weil erst dann die gesamte Information vorhanden ist._"
