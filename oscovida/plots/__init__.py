import importlib
import warnings
from typing import Optional, Sequence

import matplotlib.pyplot as plt
from matplotlib.axes._axes import Axes

from ..regions import Region
from . import _matplotlib


class Backend:
    def __init__(self):
        self._backend = "matplotlib"

        self._backends = {
            'matplotlib': _matplotlib,
        }

        if importlib.find_loader('plotly') is not None:
            from . import _plotly

            self._backends['plotly'] = _plotly

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend: str):
        if backend in self._backends.keys():
            self._backend = backend
        else:
            if importlib.find_loader('plotly') is None:
                warnings.warn(
                    "Plotly module not loaded so plotly is not availale as a"
                    "backend. Is plotly installed?"
                )
            raise ValueError(
                f"Invalid backend, backend must be one of {list(self._backends.keys())}"
            )

    @property
    def module(self):
        return self._backends[self.backend]


BACKEND = Backend()


def set_backend(backend):
    BACKEND.backend = backend
    return None


def get_backend():
    return BACKEND.module


def plot_totals(
    region: Region,
    plot_object: Optional[Axes] = None,
    colnames: Sequence[str] = ["confirmed", "deaths"],
    logscale: bool = True,
    label_prepend: Optional[str] = None,
) -> Axes:
    """Plots the total numbers for an oscovida `Region`, by default plots only
    the `confirmed` and `deaths` columns.

    Plots the input series assuming it is a cumulative sum of cases, deaths, or
    recoveries, either onto a new axis or onto a given axis. Plots follow the
    oscovida plotting style.

    Parameters
    ----------
    region : Region
        An oscovida `Region` object to be plotted
    colnames : Sequence[str], optional
        List or tuple of column names to be plotted
        By default ["confirmed", "deaths"]
    plot_object : Optional[Axes], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`. If the plotly
        backend is being used, this can be a `plotly.graph_objects.Figure` instead
        By default `None`
    logscale : bool, optional
        [description], by default True
    label_prepend : Optional[str], optional
        String to prepend to the label, e.g. "GB" would make the labels "GB cases"
        and "GB deaths", instead of just generic "cases" and "deaths". This is
        automatically added when using a Region as an argument, must be manually
        added when passing a series
        By default `""`

    Returns
    -------
    Axes
        Axes with plotted lines
    """
    if label_prepend is None:
        label_prepend = region.admin_1

    #  colnames should be a list or tuple of strings, if it is just a string then
    #  put it into a list here
    if isinstance(colnames, str):
        colnames = [colnames]

    for colname in colnames:
        plot_object = get_backend().plot_totals(
            region.data[colname],
            plot_object,
            logscale=logscale,
            label_prepend=label_prepend,
        )

    return plot_object


def plot_daily(
    region: Region,
    plot_object: Optional[Axes] = None,
    colnames: Sequence[str] = ["confirmed", "deaths"],
    label_prepend: Optional[str] = None,
    smoothing: str = 'weak',
) -> Axes:
    """Plots the daily numbers for an oscovida `Region`, by default plots only
    the `confirmed` and `deaths` columns.

    Works out the daily numbers for a given input series assuming it is a
    cumulative sum of either `cases`, `deaths`, or `recoveries`. Plots a line
    with the smoothed daily numbers, and uses the raw numbers for a bar chart.

    Parameters
    ----------
    region : Region
        An oscovida `Region` object to be plotted
    colnames : Sequence[str], optional
        List or tuple of column names to be plotted
        By default ["confirmed", "deaths"]
    plot_object : Optional[Axes], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`. If the plotly
        backend is being used, this can be a `plotly.graph_objects.Figure` instead
        By default `None`
    label_prepend : Optional[str], optional
        String to prepend to the label, e.g. "GB" would make the labels "GB cases"
        and "GB deaths", instead of just generic "cases" and "deaths". This is
        automatically added when using a Region as an argument, must be manually
        added when passing a series
        By default `""`
    smoothing : str, optional
        Smoothing argument to use, see `oscovida.statistics.smooth` and
        `oscovida.statistics.SMOOTHING_METHODS` for more info
        By default 'weak'

    Returns
    -------
    Axes
        Axes with plotted lines
    """
    if label_prepend is None:
        label_prepend = region.admin_1

    if isinstance(colnames, str):
        colnames = [colnames]

    for colname in colnames:
        plot_object = get_backend().plot_daily(
            region.data[colname],
            plot_object,
            label_prepend=label_prepend,
            smoothing=smoothing,
        )

    return plot_object


def plot_r_number(
    region: Region,
    plot_object: Optional[Axes] = None,
    colnames: Sequence[str] = ["confirmed", "deaths"],
    color: Optional[str] = None,
    label_prepend: Optional[str] = None,
    smoothing: str = '7dayrolling',
    yaxis_auto_lim: bool = True,
) -> Axes:
    """Plots the daily r number for an oscovida `Region`, by default plots only
    the `confirmed` and `deaths` columns.

    Works out the daily numbers, applies smoothing, then computes the r number.

    This is then plotted along with a horizontal black line at a y axis value of 1.

    Parameters
    ----------
    region : Region
        An oscovida `Region` object to be plotted
    colnames : Sequence[str], optional
        List or tuple of column names to be plotted
        By default ["confirmed", "deaths"]
    plot_object : Optional[Axes], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`. If the plotly
        backend is being used, this can be a `plotly.graph_objects.Figure` instead
        By default `None`
    color : Optional[str], optional
        Color for the plot line, if `None` then the color is based on the series
        name, e.g. blue for cases, red for deaths
        By default `None`
    label_prepend : [type], optional
        String to prepend to the label, e.g. "GB" would make the labels "GB cases"
        and "GB deaths", instead of just generic "cases" and "deaths". This is
        automatically added when using a Region as an argument, must be manually
        added when passing a series
        By default `""`
    smoothing : str, optional
        Smoothing argument to use, see `oscovida.statistics.smooth` and
        `oscovida.statistics.SMOOTHING_METHODS` for more info
        By default '7dayrolling'
    yaxis_auto_lim : bool, optional
        Uses `oscovida.statistics.min_max` to work out the minimum and maximum
        r number for the past 28 days, limits the y-axis to that range
        By default True

    Returns
    -------
    Axes
        Axes with plotted lines
    """
    if label_prepend is None:
        label_prepend = region.admin_1

    if isinstance(colnames, str):
        colnames = [colnames]

    for colname in colnames:
        plot_object = get_backend().plot_r_number(
            region.data[colname],
            plot_object,
            color=color,
            label_prepend=label_prepend,
            smoothing=smoothing,
            yaxis_auto_lim=yaxis_auto_lim,
        )

    return plot_object


def plot_growth_factor(
    region: Region,
    plot_object: Optional[Axes] = None,
    colnames: Sequence[str] = ["confirmed", "deaths"],
    color: Optional[str] = None,
    label_prepend: Optional[str] = None,
    smoothing: str = '7dayrolling',
    yaxis_auto_lim: bool = True,
) -> Axes:
    """Plots the daily growth factor for for an oscovida `Region`, by default
    plots only the `confirmed` and `deaths` columns.

    Parameters
    ----------
    region : Region
        An oscovida `Region` object to be plotted
    colnames : Sequence[str], optional
        List or tuple of column names to be plotted
        By default ["confirmed", "deaths"]
    plot_object : Optional[Axes], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`. If the plotly
        backend is being used, this can be a `plotly.graph_objects.Figure` instead
        By default `None`
    color : Optional[str], optional
        Color for the plot line, if `None` then the color is based on the series
        name, e.g. blue for cases, red for deaths
        By default `None`
    label_prepend : [type], optional
        String to prepend to the label, e.g. "GB" would make the labels "GB cases"
        and "GB deaths", instead of just generic "cases" and "deaths". This is
        automatically added when using a Region as an argument, must be manually
        added when passing a series
        By default `""`
    smoothing : str, optional
        Smoothing argument to use, see `oscovida.statistics.smooth` and
        `oscovida.statistics.SMOOTHING_METHODS` for more info
        By default '7dayrolling'
    yaxis_auto_lim : bool, optional
        Uses `oscovida.statistics.min_max` to work out the minimum and maximum
        r number for the past 28 days, limits the y-axis to that range
        By default True

    Returns
    -------
    Axes
        [description]
    """
    if label_prepend is None:
        label_prepend = region.admin_1

    if isinstance(colnames, str):
        colnames = [colnames]

    for colname in colnames:
        plot_object = get_backend().plot_growth_factor(
            region.data[colname],
            plot_object,
            color=color,
            label_prepend=label_prepend,
            smoothing=smoothing,
            yaxis_auto_lim=yaxis_auto_lim,
        )

    return plot_object


def plot_doubling_time(
    region: Region,
    plot_object: Optional[Axes] = None,
    colnames: Sequence[str] = ["confirmed", "deaths"],
    color: Optional[str] = None,
    label_prepend: Optional[str] = None,
    smoothing: str = 'strong',
    yaxis_auto_lim: bool = True,
) -> Axes:
    """Plots the doubling time for an oscovida `Region`, by default plots only
    the `confirmed` and `deaths` columns.

    Works out the doubling time and plots it as a scatter plot, then smooths the
    doubling times and plots a rolling average as a line.

    Parameters
    ----------
    region : Region
        An oscovida `Region` object to be plotted
    colnames : Sequence[str], optional
        List or tuple of column names to be plotted
        By default ["confirmed", "deaths"]
    plot_object : Optional[Axes], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`. If the plotly
        backend is being used, this can be a `plotly.graph_objects.Figure` instead
        By default `None`
    color : Optional[str], optional
        Color for the plot line, if `None` then the color is based on the series
        name, e.g. blue for cases, red for deaths
        By default `None`
    label_prepend : [type], optional
        String to prepend to the label, e.g. "GB" would make the labels "GB cases"
        and "GB deaths", instead of just generic "cases" and "deaths". This is
        automatically added when using a Region as an argument, must be manually
        added when passing a series
        By default `""`
    smoothing : str, optional
        Smoothing argument to use, see `oscovida.statistics.smooth` and
        `oscovida.statistics.SMOOTHING_METHODS` for more info
        By default 'strong'
    yaxis_auto_lim : bool, optional
        Uses `oscovida.statistics.min_max` to work out the minimum and maximum
        r number for the past 28 days, limits the y-axis to that range
        By default True

    Returns
    -------
    Axes
        Axes with plotted lines
    """
    if label_prepend is None:
        label_prepend = region.admin_1

    if isinstance(colnames, str):
        colnames = [colnames]

    for colname in colnames:
        plot_object = get_backend().plot_doubling_time(
            region.data[colname],
            plot_object,
            color=color,
            label_prepend=label_prepend,
            smoothing=smoothing,
            yaxis_auto_lim=yaxis_auto_lim,
        )

    return plot_object


def _plot_summary_matplotlib(region: Region, label_prepend: Optional[str] = None):
    fig, ax = plt.subplots(6, 1, figsize=(10, 15), sharex=False)

    plot_totals(region, ax[0], label_prepend=label_prepend)

    plot_daily(region, ax[1], colnames=['confirmed'], label_prepend=label_prepend)
    ax[1].set_ylabel("daily change\n(confirmed)")
    plot_daily(region, ax[2], colnames=['deaths'], label_prepend=label_prepend)
    ax[2].set_ylabel("daily change\n(deaths)")

    plot_r_number(region, ax[3], colnames=['confirmed'], label_prepend=label_prepend)
    plot_growth_factor(
        region, ax[3], colnames=['confirmed'], label_prepend=label_prepend
    )
    ax[3].set_ylabel("r & growth factor\n(confirmed)")

    plot_r_number(region, ax[4], colnames=['deaths'], label_prepend=label_prepend)
    plot_growth_factor(region, ax[4], colnames=['deaths'], label_prepend=label_prepend)
    ax[4].set_ylabel("r & growth factor\n(deaths)")

    plot_doubling_time(region, ax[5], label_prepend=label_prepend)
    ax[5].set_ylabel("doubling time")

    return ax


def _plotly_subplot_insert(main_figure, subplot, row, col):
    #  Subplots in plotly are far more awkward than in matplotlib... far as
    #  I could find, there's no way to add a figure to a subplot, so you
    #  have to add in the data the figure contains, which then loses stuff
    #  like axis limits that you have to add back in... hopefully I'm an
    #  idiot and there's a better way to do this
    #  https://github.com/plotly/plotly.py/issues/2647
    #  Also there are no per-plot legends so everything is squished at the top
    #  https://github.com/plotly/plotly.js/issues/1668

    main_figure.add_traces(subplot.data, row, col)

    main_figure.update_yaxes(subplot.layout['yaxis'], row=row, col=col)


def _plot_summary_plotly(
    region: Region, label_prepend: Optional[str] = None, shared_xaxes=False
):
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=6, cols=1, shared_xaxes=shared_xaxes)

    totals = plot_totals(region, label_prepend=label_prepend)
    _plotly_subplot_insert(fig, totals, 1, 1)

    daily_confirmed = plot_daily(
        region, colnames=['confirmed'], label_prepend=label_prepend
    )
    _plotly_subplot_insert(fig, daily_confirmed, 2, 1)
    fig.update_yaxes(title="daily change<br>(confirmed)", row=2, col=1)

    daily_deaths = plot_daily(region, colnames=['deaths'], label_prepend=label_prepend)
    _plotly_subplot_insert(fig, daily_deaths, 3, 1)
    fig.update_yaxes(title="daily change<br>(deaths)", row=3, col=1)

    r_number_confirmed = plot_r_number(
        region, colnames=['confirmed'], label_prepend=label_prepend
    )
    _plotly_subplot_insert(fig, r_number_confirmed, 4, 1)

    growth_factor_confirmed = plot_growth_factor(
        region, colnames=['confirmed'], label_prepend=label_prepend
    )
    _plotly_subplot_insert(fig, growth_factor_confirmed, 4, 1)
    fig.update_yaxes(title="r & growth factor<br>(confirmed)", row=4, col=1)

    r_number_deaths = plot_r_number(
        region, colnames=['deaths'], label_prepend=label_prepend
    )
    _plotly_subplot_insert(fig, r_number_deaths, 5, 1)
    growth_factor_deaths = plot_growth_factor(
        region, colnames=['deaths'], label_prepend=label_prepend
    )
    _plotly_subplot_insert(fig, growth_factor_deaths, 5, 1)
    fig.update_yaxes(title="r & growth factor<br>(deaths)", row=5, col=1)

    doubling_time = plot_doubling_time(region, label_prepend=label_prepend)
    _plotly_subplot_insert(fig, doubling_time, 6, 1)

    fig.update_layout(
        font=dict(family="Inconsolata"),
        #  Plotly doesn't have auto legend position like matplotlib so we
        #  set it to outside the plot to avoid covering the plot lines
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=1160,
        width=880,
    )

    return fig


def plot_summary(
    region: Region,
    label_prepend: Optional[str] = None,
):
    if label_prepend is None:
        label_prepend = region.admin_1

    summary_functions = {
        'matplotlib': _plot_summary_matplotlib,
        'plotly': _plot_summary_plotly,
    }

    return summary_functions[BACKEND._backend](region, label_prepend)
