[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fangohr/coronavirus-2020/master?filepath=germany.ipynb)

# coronavirus-2020 (covid2019)

This page isa little outdated. Nice plots are available at https://ourworldindata.org/coronavirus

What is available here?

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

![Deaths daily change](figures/global-new-deaths.svg)<

# Some plots for Germany

![Plot](figures/germany-overview.svg)
![Plot](figures/germany-overview-25-feb.svg)
![Plot](figures/new-cases-Germany.svg)
![Plot](figures/new-deaths-Germany.svg)

# Fit model of type n(t) = c*(t-t0)^p + a0

![Plot](figures/infections-with-model-fit.svg)

# Fit exponential curves

See [current-trends2.ipynb](current-trends2.ipynb)

# Predicting increase in infections

- Based on data since 25 Feb
- Assumes no significant change to containment measures 

[comment]: <> insert table here
<pre>
Predictions for cases in Germany:

Last data point used in prediction from 2020-03-28 00:00:00

Infections in  1 days:  65558 (29 Mar 2020)
Infections in  2 days:  74143 (30 Mar 2020)
Infections in  3 days:  83551 (31 Mar 2020)
Infections in  4 days:  93835 (01 Apr 2020)
Infections in  5 days: 105047 (02 Apr 2020)
Infections in  6 days: 117244 (03 Apr 2020)
Infections in  7 days: 130481 (04 Apr 2020)
Infections in  8 days: 144819 (05 Apr 2020)
Infections in  9 days: 160318 (06 Apr 2020)
Infections in 10 days: 177040 (07 Apr 2020)
Infections in 11 days: 195048 (08 Apr 2020)
Infections in 12 days: 214408 (09 Apr 2020)
Infections in 13 days: 235188 (10 Apr 2020)
Infections in 14 days: 257456 (11 Apr 2020)
Infections in 15 days: 281284 (12 Apr 2020)
Infections in 16 days: 306744 (13 Apr 2020)
Infections in 17 days: 333910 (14 Apr 2020)
Infections in 18 days: 362858 (15 Apr 2020)
Infections in 19 days: 393666 (16 Apr 2020)
Infections in 20 days: 426413 (17 Apr 2020)
Infections in 21 days: 461181 (18 Apr 2020)
Infections in 22 days: 498052 (19 Apr 2020)
Infections in 23 days: 537112 (20 Apr 2020)
Infections in 24 days: 578447 (21 Apr 2020)
Infections in 25 days: 622145 (22 Apr 2020)
Infections in 26 days: 668296 (23 Apr 2020)
Infections in 27 days: 716993 (24 Apr 2020)
Infections in 28 days: 768328 (25 Apr 2020)
Infections in 29 days: 822398 (26 Apr 2020)

Fit parameters: p = 4.114 c = 0.0372 t0= -0.000 a0= -145.348</pre>
