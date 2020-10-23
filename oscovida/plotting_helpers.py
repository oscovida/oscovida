import numpy as np
from functools import wraps
from matplotlib import pyplot as plt


def align_twinx_ticks(ax_left: plt.Axes, ax_right: plt.Axes) -> np.ndarray:
    """
    Returns an array of ticks for the right axis which match ones on the left.

    There's no easy way of aligning ticks nor a good general solution.
    Lets use a simple linear function that maps the ends of one scale onto ends
    of another. Obviously, we need that
          f(left_min) -> right_min and
          f(left_max) -> right_max,
    and points in between are mapped proportionally.
    """
    left = ax_left.get_ylim()
    right = ax_right.get_ylim()
    f = lambda x: right[0] + (x - left[0]) / (left[1] - left[0]) * (right[1] - right[0])
    return f(ax_left.get_yticks())


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
        l1, l2 = ax.lines   # only two line for a moment
        if "rolling mean" in l1._label:
            mean, data = l1, l2
        else:
            mean, data = l2, l1
        _, ylim = ax.get_ylim()
        ax.set_ylim(top=min(ylim, np.nanmax(mean._y) * max_ratio))
        return ax
    return wrapper