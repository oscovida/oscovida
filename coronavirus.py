"""Code used for notebooks and data exploration on
https://github.com/fangohr/coronavirus-2020"""


from functools import lru_cache
import os
import time
import numpy as np
import pandas as pd

# choose font - can be deactivated
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Inconsolata']

import matplotlib.pyplot as plt
plt.style.use('ggplot')

# suppress warning
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

LW = 3   # line width

base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

def double_time_exponential(q2_div_q1, t2_minus_t1=None):
    """ See https://en.wikipedia.org/wiki/Doubling_time"""
    if t2_minus_t1 is None:
        t2_minus_t1 = np.ones(q2_div_q1.shape)
    return t2_minus_t1 * np.log(2) / np.log(q2_div_q1)


def report_download(url, df):
    print(f"Downloaded data: last data point {df.columns[-1]} from {url}")


@lru_cache(maxsize=1)
def fetch_deaths():
    url = os.path.join(base_url, "time_series_covid19_" + "deaths" + "_global.csv")
    df = pd.read_csv(url, index_col=1)
    report_download(url, df)
    return df

@lru_cache(maxsize=1)
def fetch_cases():
    url = os.path.join(base_url, "time_series_covid19_" + "confirmed" + "_global.csv")
    df = pd.read_csv(url, index_col=1)
    report_download(url, df)
    return df


def get_country(country):
    """Given a country name, return deaths and cases as time series.
    All rows should contain a datetime index and a value"""

    deaths = fetch_deaths()
    cases = fetch_cases()

    assert country in deaths.index, f"{country} not in available countries. These are {sorted(deaths.index)}"
        
    # Some countries report sub areas (i.e. multiple rows per country) such as China, France, United Kingdom
    # Denmark. In that case, we sum over all regions.
    tmp = deaths.loc[country]
    if len(tmp.shape) == 1:
        d = deaths.loc[country]
    elif len(tmp.shape) == 2:
        d = deaths.loc[country].sum()
    else:
        raise ValueError("Unknown data set structure for deaths {country}:", tmp)
        
    tmp = cases.loc[country]
    if len(tmp.shape) == 1:
        c = cases.loc[country]
    elif len(tmp.shape) == 2:
        c = cases.loc[country].sum()
    else:
        raise ValueError("Unknown data set structure for cases {country}:", tmp)

    # make date string into timeindex
    d.index = pd.to_datetime(d.index, errors="coerce", format="%m/%d/%y")
    c.index = pd.to_datetime(c.index, errors="coerce", format="%m/%d/%y")
    # drop all rows that don't have data
    # sanity check: how many do we drop?
    if c.index.isnull().sum() > 3:
        print(f"about to drop {c.index.isnull().sum()} entries due to NaT in index", c)
    c = c[c.index.notnull()] 

    if d.index.isnull().sum() > 3:
        print(f"about to drop {d.index.isnull().sum()} entries due to NaT in index", d)
    d = d[d.index.notnull()] 
    
    # check there are no NaN is in the data
    assert c.isnull().sum() == 0, f"{c.isnull().sum()} NaNs in {c}"
    assert d.isnull().sum() == 0, f"{d.isnull().sum()} NaNs in {d}"
    
    # label data
    c.country = country
    c.label = "cases"
    
    d.country = country
    d.label = "deaths"
    
    return c, d


@lru_cache(maxsize=1)
def fetch_data_germany():
    """Data source is https://npgeo-corona-npgeo-de.hub.arcgis.com . The text on the
    webpage implies that the data comes from the Robert Koch Institute. """
    
    datasource = "https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv"
    t0 = time.time()
    print(f"Please be patient - downloading data from {datasource} ...")
    germany = pd.read_csv(datasource)
    delta_t = time.time() - t0
    print(f"Completed downloading {len(germany)} rows in {delta_t:.1f} seconds.")

    ## create new column 'landkreis' and get rid of "SK " and "LK " for this
    ## - this is too simplistic. We have fields like "Region Hannover"
    # germany['landkreis'] = germany['Landkreis'].apply(lambda s: s[3:]) 

    # (at least) the last data from the Robert-Koch-Institute (RKI) seems not to be
    # fully reported the day after. For example, on 3 April, the number of cases
    # from RKI is well below what is expected. Example:
    #
    # From RKI (as of evening of 2020-04-03:)
    # 2020-03-29    62653
    # 2020-03-30    66692
    # 2020-03-31    72333
    # 2020-04-01    77464
    # 2020-04-02    79625
    #
    # From Johns Hopkins (as of evening of 2020-04-03:):
    # 2020-03-29    62095
    # 2020-03-30    66885
    # 2020-03-31    71808
    # 2020-04-01    77872
    # 2020-04-02    84794
    #
    # So we must assume that the RKI data will be corrected later; maybe the next day.
    #
    # To make our plots not inaccurate, we'll remove the last data point from the RKI data:
    g2 = germany.set_index(pd.to_datetime(germany['Meldedatum']))
    g2.index.name = 'date'
    last_day = g2.index.max()
    sel = g2.index == last_day
    cleaned = g2.drop(g2[sel].index, inplace=False)
    return cleaned


def germany_get_region(state=None, landkreis=None):
    germany = fetch_data_germany()
    """Returns two time series: (cases, deaths)"""
    assert state or landkreis, "Need to provide a value for state or landkreis"

    if state and landkreis:
        raise NotImplementedError
        """We need to check if this is important."""

    if state:
        assert state in germany['Bundesland'].values, \
            f"{state} not in available German states. These are {sorted(germany['Bundesland'].drop_duplicates())}"

        land = germany[germany['Bundesland'] == state]
        land = land.set_index(pd.to_datetime(land['Meldedatum']))
        land.index.name = 'date'
        land.sort_index(inplace=True)

        # group over multiple rows for the same date 
        # (this will also group over the different landkreise in the state)
        cases = land["AnzahlFall"].groupby('date').agg('sum').cumsum()
        cases.country = f'Germany-{state}'
        cases.label = 'cases'

        # group over all multiple entries per day
        deaths = land["AnzahlTodesfall"].groupby('date').agg('sum').cumsum()
        deaths.country = f'Germany-{state}'
        deaths.label = 'deaths'

        return cases, deaths

    if landkreis:
        assert landkreis in germany['Landkreis'].values, \
            f"{state} not in available German states. These are {sorted(germany['Landkreis'].drop_duplicates())}"

        lk = germany[germany["Landkreis"] == landkreis]
        lk.index = pd.to_datetime(lk['Meldedatum'])
        lk.index.name = 'date'
        lk = lk.sort_index()

        cases = lk["AnzahlFall"].groupby('date').agg('sum').cumsum()
        cases.country = f'Germany-{landkreis}'
        cases.label = 'cases'

        deaths = lk["AnzahlTodesfall"].groupby('date').agg('sum').cumsum()
        deaths.country = f'Germany-{landkreis}'
        deaths.label = 'deaths'

        return cases, deaths


def plot_time_step(ax, series, style="-", logscale=True):
    ax.step(series.index, series.values, style, label=series.country + " " + series.label,
           linewidth=LW)
    if logscale:
        ax.set_yscale('log')
    ax.legend()
    ax.set_ylabel("total numbers")
    return ax

def plot_change_bar(ax, series, color, rolling=None):
    change = series.diff().dropna()   # lose one point at beginning

    if rolling:
        rolling_label = f" {rolling}-day rolling mean"
        rolling_series = change.rolling(rolling, center=True).mean()
        bar_alpha = 0.2
    else:
        rolling_label = ""
        bar_alpha = 1.0

    label = series.country + " new " + series.label 
    ax.bar(change.index, change.values, color=color, label=label, alpha=bar_alpha, 
           linewidth=LW)
    if rolling:
        ax.plot(rolling_series.index, rolling_series.values, color=color, label=label + rolling_label,
                linewidth=LW)
    ax.legend()
    ax.set_ylabel('daily change')
    return ax

def plot_doubling_time(ax, series, color, minchange=10):
    # only keep values where there is a change of a minumum number
    sel = series.diff() <= minchange
    series.drop(series[sel].index, inplace=True)
    
    # we assume we have one value for every day - should check XXX
    q2_div_q1 = series.pct_change() + 1  # computes q2/q1
    q2_div_q1.replace(np.inf, np.nan, inplace=True)  # get rid of x/0 results
    q2_div_q1.dropna(inplace=True)
    dtime = double_time_exponential(q2_div_q1, t2_minus_t1=1)
    dtime.dropna(inplace=True)
    label = series.country + " new " + series.label 
    ax.plot(dtime.index, dtime.values, 'o', color=color, alpha=0.3, label=label)
    
    # need rolling average to smooth out weekly variations
    rolling = dtime.rolling(7, center=True).mean()
        
    # good to take maximum value from here
    ymax = min(rolling.max()*1.5, 500)
    if np.isnan(ymax):
        # This happens is rolling is empty, for example for deaths in Austria, Singapore
        print(f"Can't plot doublingtime line for {series.label} in {series.country} due to too small numbers")
        ymax = 10
        
    # some countries require special care
    if series.country == 'China':
            ymax = 100        
        
    ax.set_ylim(0, ymax)
    ax.plot(dtime.index, rolling, "-", color=color, alpha=1.0, label=label + ' 7-day rolling mean',
            linewidth=LW)
    ax.legend()
    ax.set_ylabel("doubling time [days]")
    return ax, rolling, dtime


def plot_growth_factor(ax, series, color, minchange=10):
    """relative change of number of new cases/deaths from day to day
    See https://youtu.be/Kas0tIxDvrg?t=330, 5:30 onwards
    """
    # only keep values where there is a change of a minumum number
    sel = series.diff() <= minchange
    series.drop(series[sel].index, inplace=True)
    
    f = series.diff(1).pct_change() + 1  # compute ratio of subsequent daily changes
                                         # use change over a week
    # division by zero may lead to np.inf in the data: get rid of that
    f.replace(np.inf, np.nan, inplace=True)
    f.dropna(inplace=True)
    
    # for very small case numbers, we get large growth factors (for example 1 death one day, followed by 7 the next)
    # we drop those high values. 
    sel = f > 5
    f.drop(f[sel].index, inplace=True)
    values_dropped = sel.sum()
    if values_dropped >= 5:
        print(f"Dropping {values_dropped} from growth factor plot ({series.country}, {series.label})")
    
    label = series.country + " " + series.label + " growth factor"
    ax.plot(f.index, f.values, 'o', color=color, alpha=0.3, label=label)
    rolling = f.rolling(7, center=True).mean()
    rolling.dropna(inplace=True)
    label = series.country + " " + series.label + " growth factor 7-day mean"
    ax.plot(rolling.index, rolling.values, '-', color=color, label=label, linewidth=LW)
    
    ## looks much nicer - should we use this?
    # rolling2 = rolling.rolling(7, center=True).mean()
    # rolling2.dropna(inplace=True)
    # label = series.country + " " + series.label + " growth factor 7-day mean"
    # ax.plot(rolling2.index, rolling2.values, '-', color='C4', label=label, linewidth=LW)
    
    ax.legend()
    ax.set_ylabel("growth factor")
    ax.set_ylim(0, 2)  # should generally be below 1
    ax.plot([series.index.min(), series.index.max()], [1.0, 1.0], '-C3') # label="critical value"
    return ax, rolling, f


def test_plot_growth_factor():
    c, d = get_country("Korea, South")
    c, d = get_country("China")

    #c, d = get_country("Germany")
    #c, d = get_country("Italy")
    fix, ax = plt.subplots()
    plot_growth_factor(ax, c, 'C1');
    _, rolling, f = plot_growth_factor(ax, d, 'C0');
    return rolling, f
# rolling, f = test_plot_growth_factor()



def overview(country, region=None, subregion=None):
    if country.lower() == 'germany':
        if region == None and subregion == None:
            c, d = get_country(country)  # use johns hopkins data
        else:
            # use German data
            c, d = germany_get_region(state=region, landkreis=subregion)
    else:
        c, d = get_country(country)


    fig, axes = plt.subplots(5, 1, figsize=(10, 15), sharex=False)
    ax = axes[0]
    plot_time_step(ax=ax, series=c, style="-C1")
    plot_time_step(ax=ax, series=d, style="-C0")

    ax = axes[1]
    plot_change_bar(ax=ax, series=c, rolling=7, color="C1")
    if country == "China":
        ax.set_ylim(0, 5000)

    ax = axes[2]
    plot_change_bar(ax=ax, series=d, rolling=7, color="C0")

    ax = axes[3]
    plot_growth_factor(ax, series=d, color="C0")
    plot_growth_factor(ax, series=c, color="C1")

    ax = axes[4]
    plot_doubling_time(ax, series=d, color="C0")
    plot_doubling_time(ax, series=c, color="C1")

    # enforce same x-axis on all plots
    axes[1].set_xlim(axes[0].get_xlim())
    axes[2].set_xlim(axes[0].get_xlim())
    axes[3].set_xlim(axes[0].get_xlim())
    axes[4].set_xlim(axes[0].get_xlim())

    title = f"Overview {c.country}, last data point from {c.index[-1].date().isoformat()}"
    axes[0].set_title(title)

    fig.tight_layout(pad=1)
    filename = os.path.join("figures", c.country.replace(" ", "-").replace(",", "-") + '.svg')
    # fig.savefig(filename)

    return axes, c, d
