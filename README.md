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

Last data point used in prediction from 2020-03-22 00:00:00

Infections in  1 days:  29717 (23 Mar 2020)
Infections in  2 days:  34642 (24 Mar 2020)
Infections in  3 days:  40160 (25 Mar 2020)
Infections in  4 days:  46320 (26 Mar 2020)
Infections in  5 days:  53170 (27 Mar 2020)
Infections in  6 days:  60762 (28 Mar 2020)
Infections in  7 days:  69149 (29 Mar 2020)
Infections in  8 days:  78386 (30 Mar 2020)
Infections in  9 days:  88532 (31 Mar 2020)
Infections in 10 days:  99644 (01 Apr 2020)
Infections in 11 days: 111785 (02 Apr 2020)
Infections in 12 days: 125018 (03 Apr 2020)
Infections in 13 days: 139409 (04 Apr 2020)
Infections in 14 days: 155025 (05 Apr 2020)
Infections in 15 days: 171937 (06 Apr 2020)
Infections in 16 days: 190216 (07 Apr 2020)
Infections in 17 days: 209935 (08 Apr 2020)
Infections in 18 days: 231172 (09 Apr 2020)
Infections in 19 days: 254005 (10 Apr 2020)
Infections in 20 days: 278513 (11 Apr 2020)
Infections in 21 days: 304780 (12 Apr 2020)
Infections in 22 days: 332889 (13 Apr 2020)
Infections in 23 days: 362929 (14 Apr 2020)
Infections in 24 days: 394987 (15 Apr 2020)
Infections in 25 days: 429155 (16 Apr 2020)
Infections in 26 days: 465527 (17 Apr 2020)
Infections in 27 days: 504198 (18 Apr 2020)
Infections in 28 days: 545266 (19 Apr 2020)
Infections in 29 days: 588831 (20 Apr 2020)

Fit parameters: p = 4.187 c = 0.0304 t0= -0.000 a0= -223.770</pre>
