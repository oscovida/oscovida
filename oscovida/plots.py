from functools import singledispatch
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
from matplotlib.axes._subplots import Axes
from matplotlib.ticker import ScalarFormatter
from oscovida.regions import Region

from . import statistics

# choose font - can be deactivated
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Inconsolata']

# need many figures for index.ipynb and germany.ipynb
rcParams['figure.max_open_warning'] = 50

plt.style.use('ggplot')

COLOR_MAPPING = {
    'cases': {
        'totals': 'C1',
        'daily': 'C1',
        'r_number': 'C5',
        'growth_factor': 'C1',
        'doubling_time': 'C1',
    },
    'deaths': {
        'totals': 'C0',
        'daily': 'C0',
        'r_number': 'C4',
        'growth_factor': 'C0',
        'doubling_time': 'C0',
    },
}


def _standard_plot_formatting(plot_function):
    def formatted_plot(*args, **kwargs) -> Axes:
        ax = plot_function(*args, **kwargs)

        # labels on the right y-axis as well
        ax.tick_params(left=True, right=True, labelleft=True, labelright=True)
        ax.yaxis.set_ticks_position('both')
        ax.legend()

        return ax

    return formatted_plot


@singledispatch
def plot_totals() -> Axes:
    raise NotImplementedError


#  NOTE: If you want to decorate a function when using the singledispatch
#  decorator you have to **explicitly** specify the type to dispatch on as an
#  argument to the decorator, otherwise the dispatch fails as it (I guess?)
#  cannot read the type hinting through a decorated function
@plot_totals.register(pd.DataFrame)
@_standard_plot_formatting
def _(
    region_data: pd.DataFrame,
    ax: Optional[Axes] = None,
    logscale=True,
    label_prepend="",
) -> Axes:
    if ax is None:
        ax = plt.gca()

    ax.step(
        region_data.index,
        region_data['confirmed'],
        label=" ".join([label_prepend, 'cases']),
        color='C1',
    )

    ax.plot(
        region_data.index,
        region_data['deaths'],
        label=" ".join([label_prepend, 'deaths']),
        color='C0',
    )

    if logscale:
        ax.set_yscale('log')

    ax.yaxis.set_major_formatter(ScalarFormatter())

    ax.set_ylabel("total numbers")

    return ax


@plot_totals.register(Region)
def _(
    region: Region, ax: Optional[Axes] = None, logscale=True, label_prepend=None
) -> Axes:
    if label_prepend is None:
        label_prepend = region.admin_1

    return plot_totals(
        region.data, ax=ax, logscale=logscale, label_prepend=label_prepend
    )


@singledispatch
def plot_daily() -> Axes:
    raise NotImplementedError


@plot_daily.register(pd.Series)
@_standard_plot_formatting
def _(
    series: pd.Series,
    ax: Optional[Axes] = None,
    color=None,
    label_prepend="",
    smoothing='weak',
):
    if ax is None:
        ax = plt.gca()

    label = series.name
    if label == 'confirmed':
        label = 'cases'

    if color is None:
        color = COLOR_MAPPING[label]['daily']

    bar_alpha = 0.2

    series_daily = series.pipe(statistics.daily)
    series_daily_s = series_daily.pipe(statistics.smooth, kind=smoothing)

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

    ax.set_ylabel('daily change')

    return ax


@plot_daily.register(Region)
def _(
    region: Region,
    colname: str,
    ax: Optional[Axes] = None,
    label_prepend=None,
    smoothing='weak',
):
    if label_prepend is None:
        label_prepend = region.admin_1

    return plot_daily(
        region.data[colname], ax=ax, label_prepend=label_prepend, smoothing=smoothing,
    )


@singledispatch
def plot_r_number() -> Axes:
    raise NotImplementedError


@plot_r_number.register(pd.Series)
@_standard_plot_formatting
def _(
    series: pd.Series,
    ax: Optional[Axes] = None,
    color=None,
    label_prepend="",
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
) -> Axes:
    if ax is None:
        ax = plt.gca()

    label = series.name
    if label == 'confirmed':
        label = 'cases'

    if color is None:
        color = COLOR_MAPPING[label]['r_number']

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

    ax.set_ylabel(f'r number')

    return ax


@plot_r_number.register(Region)
def _(
    region: Region,
    colname: str,
    ax: Optional[Axes] = None,
    color=None,
    label_prepend=None,
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
) -> Axes:
    if label_prepend is None:
        label_prepend = region.admin_1

    return plot_r_number(
        region.data[colname],
        ax=ax,
        color=color,
        label_prepend=label_prepend,
        smoothing=smoothing,
        yaxis_auto_lim=yaxis_auto_lim,
    )


@singledispatch
def plot_growth_factor() -> Axes:
    raise NotImplementedError


@plot_growth_factor.register(pd.Series)
@_standard_plot_formatting
def _(
    series: pd.Series,
    ax: Optional[Axes] = None,
    color=None,
    label_prepend="",
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
) -> Axes:
    if ax is None:
        ax = plt.gca()

    label = series.name
    if label == 'confirmed':
        label = 'cases'

    if color is None:
        color = COLOR_MAPPING[label]['growth_factor']

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

    ax.set_ylabel(f'growth factor')

    return ax


@plot_growth_factor.register(Region)
def _(
    region: Region,
    colname: str,
    ax: Optional[Axes] = None,
    color=None,
    label_prepend=None,
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
) -> Axes:
    if label_prepend is None:
        label_prepend = region.admin_1

    return plot_growth_factor(
        region.data[colname],
        ax=ax,
        color=color,
        label_prepend=label_prepend,
        smoothing=smoothing,
        yaxis_auto_lim=yaxis_auto_lim,
    )


@singledispatch
def plot_doubling_time() -> Axes:
    raise NotImplementedError


@plot_doubling_time.register(pd.Series)
@_standard_plot_formatting
def _(
    series: pd.Series,
    ax: Optional[Axes] = None,
    color=None,
    label_prepend="",
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
) -> Axes:
    if ax is None:
        ax = plt.gca()

    label = series.name
    if label == 'confirmed':
        label = 'cases'

    if color is None:
        color = COLOR_MAPPING[label]['daily']

    doubling_time = series.pipe(statistics.doubling_time)

    ax.plot(
        doubling_time.pipe(statistics.smooth, kind=smoothing),
        label=" ".join([label_prepend, f'{label} doubling time ({smoothing})']),
        color=color,
    )

    ax.plot(
        doubling_time,
        'o',
        alpha=0.3,
        label=" ".join([label_prepend, f'{label} doubling time']),
        color=color,
    )

    if yaxis_auto_lim:
        y_auto_min, y_auto_max = doubling_time.pipe(statistics.min_max, n=28)
        ax.set_ylim(y_auto_min, y_auto_max)

    return ax

@plot_doubling_time.register(Region)
def _(
    region: Region,
    colname: str,
    ax: Optional[Axes] = None,
    color=None,
    label_prepend=None,
    smoothing='7dayrolling',
    yaxis_auto_lim=True,
) -> Axes:
    if label_prepend is None:
        label_prepend = region.admin_1

    return plot_doubling_time(
        region.data[colname],
        ax=ax,
        color=color,
        label_prepend=label_prepend,
        smoothing=smoothing,
        yaxis_auto_lim=yaxis_auto_lim,
    )
