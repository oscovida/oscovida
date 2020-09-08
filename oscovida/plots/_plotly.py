from functools import wraps
from html.entities import name2codepoint
from typing import Optional, Sequence

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline
from plotly.graph_objects import Figure

from .. import statistics

plotly.offline.init_notebook_mode()


COLOR_MAPPING = {
    'confirmed': {
        'totals': '#338abd',
        'daily': '#338abd',
        'r_number': '#8eba42',
        'growth_factor': '#338abd',
        'doubling_time': '#338abd',
    },
    'deaths': {
        'totals': '#e24a33',
        'daily': '#e24a33',
        'r_number': '#fbc15e',
        'growth_factor': '#e24a33',
        'doubling_time': '#e24a33',
    },
}


def _standard_plot_formatting(plot_function):
    @wraps(plot_function)
    def formatted_plot(*args, **kwargs) -> Figure:
        fig = plot_function(*args, **kwargs)

        fig.update_layout(
            font=dict(family="Inconsolata"),
            #  Plotly doesn't have auto legend position like matplotlib so we
            #  set it to outside the plot to avoid covering the plot lines
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )

        return fig

    return formatted_plot


@_standard_plot_formatting
def plot_totals(
    series: pd.Series,
    fig: Optional[Figure] = None,
    color: Optional[str] = None,
    label_prepend: str = "",
    logscale: bool = True,
) -> Figure:
    """Plots the total numbers for a given series.

    Plots the input series assuming it is a cumulative sum of cases, deaths, or
    recoveries, either onto a new axis or onto a given axis. Plots follow the
    oscovida plotting style.

    Parameters
    ----------
    series : pd.Series
        Input data to plot, assumes it is a cumulative sum of `cases`, `deaths`,
        or `recovered`
    ax : Optional[Figure], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`
        By default `None`
    color : Optional[str], optional
        Color for the plot line, if `None` then the color is based on the series
        name, e.g. blue for cases, red for deaths
        By default `None`
    logscale : bool, optional
        If the plot should be log-y
        By default True
    label_prepend : [str], optional
        Label for the plotted line

    Returns
    -------
    Axes
        Axes with plotted lines
    """
    if fig is None:
        fig = go.Figure()

    if color is None:
        color = COLOR_MAPPING[str(series.name)]['totals']

    fig.add_trace(
        go.Scatter(
            x=series.index,
            y=series,
            line_shape="vh",
            name=" ".join([label_prepend, str(series.name)]),
            line=dict(color=color),
        )
    )

    if logscale:
        fig.update_layout(yaxis_type="log")

    fig.update_layout(yaxis_title="total numbers")

    return fig


@_standard_plot_formatting
def plot_daily(
    series: pd.Series,
    fig: Optional[Figure] = None,
    color: Optional[str] = None,
    label_prepend: str = "",
    smoothing: str = 'weak',
) -> Figure:
    """Plots the daily numbers as a rolling average line, as well as a bar chart.

    Works out the daily numbers for a given input series assuming it is a
    cumulative sum of either `cases`, `deaths`, or `recoveries`. Plots a line
    with the smoothed daily numbers, and uses the raw numbers for a bar chart.

    Parameters
    ----------
    series : pd.Series
        Input data to plot, assumes it is a cumulative sum of `cases`, `deaths`,
        or `recovered`
    ax : Optional[Figure], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`
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
        By default 'weak'

    Returns
    -------
    Axes
        Axes with plotted lines
    """
    if fig is None:
        fig = go.Figure()

    if color is None:
        color = COLOR_MAPPING[str(series.name)]['daily']

    series_daily = series.pipe(statistics.daily)
    series_daily_s = series_daily.pipe(statistics.smooth, kind=smoothing)

    fig.add_trace(
        go.Bar(
            x=series_daily.index,
            y=series_daily,
            name=str(series_daily.name),
            marker_color=color,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=series_daily_s.index,
            y=series_daily_s.values,
            name=" ".join(
                [label_prepend, f'new {str(series.name)}', f"'{smoothing}' smoothing"]
            ),
            line=dict(color=color),
        )
    )

    fig.update_layout(yaxis_title="daily change")

    return fig


@_standard_plot_formatting
def plot_r_number(
    series: pd.Series,
    fig: Optional[Figure] = None,
    color: Optional[str] = None,
    label_prepend: str = "",
    smoothing: str = '7dayrolling',
    yaxis_auto_lim: bool = True,
) -> Figure:
    """Plots the daily r number for a given series.

    Works out the daily numbers, applies smoothing, then computes the r number.

    This is then plotted along with a horizontal black line at a y axis value of 1.

    Parameters
    ----------
    series : pd.Series
        Input data to plot, assumes it is a cumulative sum of `cases`, `deaths`,
        or `recovered`
    ax : Optional[Figure], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`
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
    if fig is None:
        fig = go.Figure()

    if color is None:
        color = COLOR_MAPPING[str(series.name)]['r_number']

    r_number = (
        series.pipe(statistics.daily)
        .pipe(statistics.smooth, kind=smoothing)
        .pipe(statistics.r_number)
    )

    fig.add_trace(
        go.Scatter(
            x=r_number.index,
            y=r_number,
            name=" ".join(
                [label_prepend, f'{str(series.name)} daily R number ({smoothing})']
            ),
            line=dict(color=color),
        )
    )

    if yaxis_auto_lim:
        y_auto_min, y_auto_max = r_number.pipe(statistics.min_max, n=28)
        fig.update_layout(yaxis=dict(range=[y_auto_min, y_auto_max]))

    fig.update_layout(
        shapes=[
            dict(
                type='line',
                yref='y',
                y0=1,
                y1=1,
                xref='x',
                x0=series.index.min(),
                x1=series.index.max(),
            )
        ]
    )

    fig.update_layout(yaxis_title="r number")

    return fig


@_standard_plot_formatting
def plot_growth_factor(
    series: pd.Series,
    fig: Optional[Figure] = None,
    color: Optional[str] = None,
    label_prepend: str = "",
    smoothing: str = '7dayrolling',
    yaxis_auto_lim: bool = True,
) -> Figure:
    """Plots the daily growth factor for a given series.

    Works out the daily numbers for a given input series assuming it is a
    cumulative sum of either `cases`, `deaths`, or `recoveries`. Smooths the
    data, then computes the growth factor. Plots a line for the growth factor
    and a line at y = 0.

    Parameters
    ----------
    series : pd.Series
        Input data to plot, assumes it is a cumulative sum of `cases`, `deaths`,
        or `recovered`
    ax : Optional[Figure], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`
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
    if fig is None:
        fig = go.Figure()

    if color is None:
        color = COLOR_MAPPING[str(series.name)]['growth_factor']

    growth_factor = series.pipe(statistics.smooth, kind=smoothing).pipe(
        statistics.growth_factor
    )

    fig.add_trace(
        go.Scatter(
            x=growth_factor.index,
            y=growth_factor,
            name=" ".join(
                [label_prepend, f'{str(series.name)} daily growth factor ({smoothing})']
            ),
            line=dict(color=color),
        )
    )

    if yaxis_auto_lim:
        y_auto_min, y_auto_max = growth_factor.pipe(statistics.min_max, n=28)
        fig.update_layout(yaxis=dict(range=[y_auto_min, y_auto_max]))

    fig.update_layout(
        shapes=[
            dict(
                type='line',
                yref='y',
                y0=1,
                y1=1,
                xref='x',
                x0=series.index.min(),
                x1=series.index.max(),
            )
        ]
    )

    fig.update_layout(yaxis_title="growth factor")

    return fig


@_standard_plot_formatting
def plot_doubling_time(
    series: pd.Series,
    fig: Optional[Figure] = None,
    color: Optional[str] = None,
    label_prepend: str = "",
    smoothing: str = 'strong',
    yaxis_auto_lim: bool = True,
) -> Figure:
    """Plots the doubling time for a given series.

    Works out the doubling time and plots it as a scatter plot, then smooths the
    doubling times and plots a rolling average as a line.

    Parameters
    ----------
    series : pd.Series
        Input data to plot, assumes it is a cumulative sum of `cases`, `deaths`,
        or `recovered`
    ax : Optional[Figure], optional
        Axes to plot onto, if `None` then defaults to `plt.gca()`
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
    if fig is None:
        fig = go.Figure()

    if color is None:
        color = COLOR_MAPPING[str(series.name)]['daily']

    doubling_time = series.pipe(statistics.doubling_time)

    smoothed_doubling_time = doubling_time.pipe(statistics.smooth, kind=smoothing)

    fig.add_trace(
        go.Scatter(
            x=smoothed_doubling_time.index,
            y=smoothed_doubling_time,
            name=" ".join(
                [label_prepend, f'{str(series.name)} doubling time ({smoothing})']
            ),
            line=dict(color=color),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=doubling_time.index,
            y=doubling_time,
            name=" ".join([label_prepend, f'{str(series.name)} doubling time']),
            mode='markers',
            opacity=0.2,
            marker=dict(
                color=color,
            ),
        )
    )

    if yaxis_auto_lim:
        y_auto_min, y_auto_max = doubling_time.pipe(statistics.min_max, n=28)
        fig.update_layout(yaxis=dict(range=[y_auto_min, y_auto_max]))

    fig.update_layout(yaxis_title="doubling time")

    return fig
