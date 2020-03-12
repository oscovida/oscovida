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

Last data point used in prediction from 2020-03-11 00:00:00

Infections in  1 days:   2206 (12 Mar 2020)
Infections in  2 days:   2623 (13 Mar 2020)
Infections in  3 days:   3088 (14 Mar 2020)
Infections in  4 days:   3605 (15 Mar 2020)
Infections in  5 days:   4175 (16 Mar 2020)
Infections in  6 days:   4801 (17 Mar 2020)
Infections in  7 days:   5487 (18 Mar 2020)
Infections in  8 days:   6233 (19 Mar 2020)
Infections in  9 days:   7044 (20 Mar 2020)
Infections in 10 days:   7920 (21 Mar 2020)
Infections in 11 days:   8866 (22 Mar 2020)
Infections in 12 days:   9883 (23 Mar 2020)
Infections in 13 days:  10974 (24 Mar 2020)
Infections in 14 days:  12140 (25 Mar 2020)
Infections in 15 days:  13386 (26 Mar 2020)
Infections in 16 days:  14712 (27 Mar 2020)
Infections in 17 days:  16122 (28 Mar 2020)
Infections in 18 days:  17618 (29 Mar 2020)
Infections in 19 days:  19202 (30 Mar 2020)
Infections in 20 days:  20877 (31 Mar 2020)
Infections in 21 days:  22645 (01 Apr 2020)
Infections in 22 days:  24509 (02 Apr 2020)
Infections in 23 days:  26470 (03 Apr 2020)
Infections in 24 days:  28532 (04 Apr 2020)
Infections in 25 days:  30696 (05 Apr 2020)
Infections in 26 days:  32966 (06 Apr 2020)
Infections in 27 days:  35342 (07 Apr 2020)
Infections in 28 days:  37829 (08 Apr 2020)
Infections in 29 days:  40428 (09 Apr 2020)

Fit parameters: p = 2.908 c = 0.661 t0= -0.257 a0= 9.350</pre>
