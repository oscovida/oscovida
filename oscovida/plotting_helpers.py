import numpy as np
from functools import wraps
from matplotlib import pyplot as plt


def linear_mapping(_from, _to, x):
    """
    Lets use a simple linear function that maps the ends of one scale onto ends
    of another. Obviously, we need that
          f(left_min) -> right_min and
          f(left_max) -> right_max,
    and points in between are mapped proportionally.
    """
    return _to[0] + (x - _from[0]) / (_from[1] - _from[0]) * (_to[1] - _to[0])
    
    
def align_twinx_ticks(ax_left: plt.Axes, ax_right: plt.Axes) -> np.ndarray:
    """
    Returns an array of ticks for the right axis which match ones on the left.

    There's no easy way of aligning ticks nor a good general solution.
    """
    left = ax_left.get_ylim()
    right = ax_right.get_ylim()
    return linear_mapping(left, right, ax_left.get_yticks())


def has_twin(ax: plt.Axes) -> bool:
    """ Returns True if the `ax` axis has a twinned axis """
    for other_ax in ax.figure.axes:
        if other_ax is ax:
            continue
        if other_ax.bbox.bounds == ax.bbox.bounds:
            return True
    return False


def limit_to_smoothed(func, max_ratio=1.5):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ax = func(*args, **kwargs)
        lines, means, points, maxpoint = [], [], [], None
        if has_twin(ax):
            graphs = ax.get_shared_x_axes().get_siblings(ax)
            for graph in graphs:
                for line in graph.lines:
                    lines += [line]
        else:
            # no twin axes, everything is great!
            lines = ax.lines
        for line in lines:
            if "rolling mean" in line._label:
                means += [line]
            else:
                points += [line]
        if means:
            maxpoint = max([np.nanmax(line._y) for line in means])

            _, ylim = ax.get_ylim()
            ax.set_ylim(top=min(ylim, maxpoint * max_ratio), bottom=0)
        return ax
    return wrapper