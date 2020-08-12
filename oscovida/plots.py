from os import stat
from oscovida.statistics import smooth
from oscovida.regions import Region
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import FuncFormatter, ScalarFormatter
import pandas as pd
from functools import singledispatch

from . import statistics

# choose font - can be deactivated
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Inconsolata']

# need many figures for index.ipynb and germany.ipynb
rcParams['figure.max_open_warning'] = 50

plt.style.use('ggplot')

# COLOR_MAPPING = {
#     'CASES': {
#         'totals': 'C0',
#         'daily': 'C0',
#         'r number': ''
#     }
#     'DEATHS':
# }


@singledispatch
def plot_totals():
    raise NotImplementedError


@plot_totals.register(pd.DataFrame)
def _(region_data: pd.DataFrame, ax=None, logscale=True, label_prepend=""):
    if ax is None:
        ax = plt.gca()

    ax.step(
        region_data.index,
        region_data.confirmed,
        label=" ".join([label_prepend, 'cases']),
    )

    ax.plot(
        region_data.index,
        region_data.deaths,
        label=" ".join([label_prepend, 'deaths']),
    )

    if logscale:
        ax.set_yscale('log')

    ax.set_ylabel("total numbers")
    ax.yaxis.set_major_formatter(ScalarFormatter())

    # labels on the right y-axis as well
    ax.tick_params(left=True, right=True, labelleft=True, labelright=True)
    ax.yaxis.set_ticks_position('both')
    ax.legend()

    return ax


@plot_totals.register(Region)
def _(region: Region, ax=None, logscale=True):
    return plot_totals(
        region.data, ax=ax, logscale=logscale, label_prepend=region.admin_1
    )


@singledispatch
def plot_daily():
    raise NotImplementedError


@plot_daily.register
def _(
    series: pd.Series,
    ax=None,
    logscale=True,
    color=None,
    label_prepend="",
    smoothing='weak',
):
    if ax is None:
        ax = plt.gca()

    label = series.name
    #  The series for new cases is called 'confirmed', but people usually say
    #  'cases', so here we rename that if required
    if label == 'confirmed':
        label = 'cases'

    bar_alpha = 0.2

    series_daily = series.pipe(statistics.daily)
    series_daily_s = series_daily.pipe(statistics.smooth, kind=smoothing)

    if color is None:
        if label == 'cases':
            color = 'C1'
        elif label == 'deaths':
            color = 'C0'
        elif label == 'recovered':
            color = 'C2'
        else:
            color = 'C3'

    ax.bar(
        series_daily.index,
        series_daily.values,
        label=" ".join([label_prepend, f'new {label}']),
        color=color,
        alpha=bar_alpha,
    )

    ax.plot(
        series_daily_s.index,
        series_daily_s.values,
        label=" ".join([label_prepend, f'new {label}', f"'{smoothing}' smoothing"]),
        color=color,
    )

    ax.legend()
    ax.set_ylabel('daily change')

    # labels on the right y-axis as well
    ax.tick_params(left=True, right=True, labelleft=True, labelright=True)
    ax.yaxis.set_ticks_position('both')

    return ax


@plot_daily.register
def _(
    region: Region,
    colname: str,
    ax=None,
    logscale=True,
    label_prepend="",
    smoothing='weak',
):
    return plot_daily(
        region.data[colname],
        ax=ax,
        logscale=logscale,
        label_prepend=region.admin_1,
        smoothing=smoothing,
    )


@singledispatch
def plot_r_number():
    raise NotImplementedError


@plot_r_number.register
def _(
    series: pd.Series,
    ax=None,
    color='C4',
    label_prepend="",
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
):
    if ax is None:
        ax = plt.gca()

    label = series.name
    #  The series for new cases is called 'confirmed', but people usually say
    #  'cases', so here we rename that if required
    if label == 'confirmed':
        label = 'cases'

    r_number = (
        series.pipe(statistics.daily)
        .pipe(statistics.smooth, kind=smoothing)
        .pipe(statistics.r_number)
    )

    ax.plot(
        r_number,
        label=" ".join([label_prepend, f'{label} daily R number ({smoothing})']),
        color=color,
    )

    if yaxis_auto_lim:
        y_auto_min, y_auto_max = r_number.pipe(statistics.min_max, n=28)
        ax.set_ylim(y_auto_min, y_auto_max)

    ax.plot([series.index.min(), series.index.max()], [1.0, 1.0], '-C3')

    ax.legend()
    ax.set_ylabel(f'r number')

    # labels on the right y-axis as well
    ax.tick_params(left=True, right=True, labelleft=True, labelright=True)
    ax.yaxis.set_ticks_position('both')

    return ax


@plot_r_number.register
def _(
    region: Region,
    colname: str,
    ax=None,
    color='C4',
    label_prepend="",
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
):
    return plot_r_number(
        region.data[colname],
        ax=ax,
        color=color,
        label_prepend=region.admin_1,
        smoothing=smoothing,
        yaxis_auto_lim=yaxis_auto_lim,
    )


@singledispatch
def plot_growth_factor():
    raise NotImplementedError


@plot_growth_factor.register
def _(
    series: pd.Series,
    ax=None,
    color='C1',
    label_prepend="",
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
):
    if ax is None:
        ax = plt.gca()

    label = series.name
    #  The series for new cases is called 'confirmed', but people usually say
    #  'cases', so here we rename that if required
    if label == 'confirmed':
        label = 'cases'

    growth_factor = (
        series.pipe(statistics.daily)
        .pipe(statistics.smooth, kind=smoothing)
        .pipe(statistics.growth_factor)
    )

    ax.plot(
        growth_factor,
        label=" ".join([label_prepend, f'{label} daily growth factor ({smoothing})']),
        color=color,
    )

    if yaxis_auto_lim:
        y_auto_min, y_auto_max = growth_factor.pipe(statistics.min_max, n=28)
        ax.set_ylim(y_auto_min, y_auto_max)

    ax.plot([series.index.min(), series.index.max()], [1.0, 1.0], '-C3')

    ax.legend()
    ax.set_ylabel(f'growth factor')

    # labels on the right y-axis as well
    ax.tick_params(left=True, right=True, labelleft=True, labelright=True)
    ax.yaxis.set_ticks_position('both')

    return ax


@plot_growth_factor.register
def _(
    region: Region,
    colname: str,
    ax=None,
    color='C1',
    label_prepend="",
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
):
    return plot_growth_factor(
        region.data[colname],
        ax=ax,
        color=color,
        label_prepend=region.admin_1,
        smoothing=smoothing,
        yaxis_auto_lim=yaxis_auto_lim,
    )
