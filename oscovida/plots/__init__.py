import importlib
import warnings
from typing import Optional, Sequence

from matplotlib.axes._axes import Axes

from ..regions import Region
from . import _matplotlib


class Backend:
    def __init__(self):
        self._backend = "matplotlib"

        self._backends = {
            'matplotlib': _matplotlib,
            '__test__': None,
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


def plot_totals(
    region: Region,
    colnames: Sequence[str] = ["confirmed", "deaths"],
    plot_object: Optional[Axes] = None,
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
        plot_object = BACKEND.module.plot_totals(
            region.data[colname],
            plot_object,
            logscale=logscale,
            label_prepend=" ".join([label_prepend, colname]),
        )

    return plot_object


def plot_daily(
    region: Region,
    colnames: Sequence[str] = ["confirmed", "deaths"],
    plot_object: Optional[Axes] = None,
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
        plot_object = BACKEND.module.plot_daily(
            region.data[colname],
            plot_object,
            label_prepend=label_prepend,
            smoothing=smoothing,
        )

    return plot_object


def plot_r_number(
    region: Region,
    colnames: Sequence[str] = ["confirmed", "deaths"],
    plot_object: Optional[Axes] = None,
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
        plot_object = BACKEND.module.plot_r_number(
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
    colnames: Sequence[str] = ["confirmed", "deaths"],
    plot_object: Optional[Axes] = None,
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
        plot_object = BACKEND.module.plot_growth_factor(
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
    colnames: Sequence[str] = ["confirmed", "deaths"],
    plot_object: Optional[Axes] = None,
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

    for colname in colnames:
        plot_object = BACKEND.module.plot_doubling_time(
            region.data[colname],
            plot_object,
            color=color,
            label_prepend=label_prepend,
            smoothing=smoothing,
            yaxis_auto_lim=yaxis_auto_lim,
        )

    return plot_object
