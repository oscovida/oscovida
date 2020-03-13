[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fangohr/coronavirus-2020/master?filepath=germany.ipynb)

# coronavirus-2020 (covid2019)

- Offering data in Pandas dataFrame to explore.

- We use data from the files at https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

  Thank you @CSSEGISandData for providing the data!

- An exploration of the early infection numbers in China is described in [this link](readme-old.md).

## See the sample notebook

- [Static view of notebook, germany.ipynb](https://nbviewer.jupyter.org/github/fangohr/coronavirus-2020/blob/master/germany.ipynb)

## Execute and modify the notebook using MyBinder

- [Interactive session germany.ipynb (allows execution and modification of notebook with Binder)](https://mybinder.org/v2/gh/fangohr/coronavirus-2020/master?filepath=germany.ipynb)


# Some plots with global numbers

Note: "Active" cases are those that are infected, not recovered and not dead.

![Global overview](figures/global-overview.svg)

![Global deaths](figures/global-deaths.svg)

![Infections daily change](figures/global-new-infections.svg)

![Deaths daily change](figures/global-new-deaths.svg)

# Some plots for Germany

![Plot](figures/germany-overview.svg)
![Plot](figures/germany-overview-25-feb.svg)
![Plot](figures/new-cases-Germany.svg)
![Plot](figures/new-recovered-Germany.svg)
![Plot](figures/new-active-Germany.svg)
![Plot](figures/new-deaths-Germany.svg)

# Fit model of type n(t) = c*(t-t0)^p + a0

![Plot](figures/infections-with-model-fit.svg)

# Predicting increase in infections

- Based on data since 25 Feb
- Assumes no significant change to containment measures 

[comment]: <> insert table here
<pre>
Predictions for cases in Germany:

Last data point used in prediction from 2020-03-12 00:00:00

Infections in  1 days:   2502 (13 Mar 2020)
Infections in  2 days:   2921 (14 Mar 2020)
Infections in  3 days:   3381 (15 Mar 2020)
Infections in  4 days:   3885 (16 Mar 2020)
Infections in  5 days:   4434 (17 Mar 2020)
Infections in  6 days:   5030 (18 Mar 2020)
Infections in  7 days:   5674 (19 Mar 2020)
Infections in  8 days:   6367 (20 Mar 2020)
Infections in  9 days:   7112 (21 Mar 2020)
Infections in 10 days:   7910 (22 Mar 2020)
Infections in 11 days:   8762 (23 Mar 2020)
Infections in 12 days:   9669 (24 Mar 2020)
Infections in 13 days:  10634 (25 Mar 2020)
Infections in 14 days:  11658 (26 Mar 2020)
Infections in 15 days:  12741 (27 Mar 2020)
Infections in 16 days:  13886 (28 Mar 2020)
Infections in 17 days:  15094 (29 Mar 2020)
Infections in 18 days:  16367 (30 Mar 2020)
Infections in 19 days:  17705 (31 Mar 2020)
Infections in 20 days:  19110 (01 Apr 2020)
Infections in 21 days:  20583 (02 Apr 2020)
Infections in 22 days:  22126 (03 Apr 2020)
Infections in 23 days:  23741 (04 Apr 2020)
Infections in 24 days:  25427 (05 Apr 2020)
Infections in 25 days:  27188 (06 Apr 2020)
Infections in 26 days:  29023 (07 Apr 2020)
Infections in 27 days:  30935 (08 Apr 2020)
Infections in 28 days:  32924 (09 Apr 2020)
Infections in 29 days:  34993 (10 Apr 2020)

Fit parameters: p = 2.711 c = 1.15 t0= -0.000 a0= 3.335</pre>
