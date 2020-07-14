import math


def compute_daily_change(series):
    """returns (change, smooth, smooth2)

    where 'change' is a tuple of (series, label)
    and smooth is a tuple of (series, label).
    and smooth2 is a tuple of (series, label).

    'change' returns the raw data (with nan's dropped)
    'smooth' makes the data smoother
    'smooth2' does some additional smoothing - more artistic than scientific

    The 'change' under consideration, is the day-to-day change of the series.
    We assume that there is one entry per day in the Series.

    """
    diff = series.diff().dropna()
    label = ""
    change = diff, label

    # smoothed curve, technical description
    smooth_label = f"Gaussian window (stddev=3 days)"
    # shorter description
    smooth_label = f"(rolling mean)"
    rolling_series = diff.rolling(9, center=True,
                                  win_type='gaussian',
                                  min_periods=1).mean(std=3)
    smooth = rolling_series, smooth_label

    # extra smoothing for better visual effects
    rolling_series2 = rolling_series.rolling(4, center=True,
                                             win_type='gaussian',
                                             min_periods=1).mean(std=2)
    # extra smooth curve
    smooth2_label = "Smoothed " + smooth_label
    # shorter description
    smooth2_label = smooth_label

    smooth2 = rolling_series2, smooth2_label

    return change, smooth, smooth2


def compute_doubling_time(series, minchange=0.5, labels=None, debug=False):

    """
    Compute and return doubling time of (assumed exponential) growth, based on two
    data points. We use data points from subsequent days.

    returns (dtime, smooth)

    Where 'dtime' is a tuple of (series, label)
    and smooth is a tuple of (series, label).

    'dtime' returns the raw data (with nan's dropped)
    'smooth' makes the data smoother

    The 'dtime' under consideration, is the day-to-day dtime of the series.
    We assume that there is one entry per day in the Series.

    If there is not enough data to compute the doubling time, returns
    ((None, message), (None, None)) where 'message' provides
    data for debugging the analysis.
    """

    if labels is None:
        label = ""
        region = ""
    else:
        region, label = labels


    # only keep values where there is a change of a minumum number
    # get rid of data points where change is small values
    (f, f_label) , (change_smoothed, smoothed_label), _ = compute_daily_change(series)
    sel = change_smoothed < minchange
    reduced = series.drop(f[sel].index, inplace=False)
    if len(reduced) <= 1:   # no data left
        return (None, "no data in reduced data set"), (None, None)

    ratio = reduced.pct_change() + 1  # computes q2/q1 =
    ratio_smooth = reduced.rolling(7, center=True, win_type='gaussian',
                                   min_periods=7).mean(std=3).pct_change() + 1

    if debug:
        print(f"len(ratio) = {len(ratio.dropna())}, {ratio}")
        print(f"len(ratio_smooth) = {len(ratio_smooth.dropna())}, {ratio_smooth}")


    # can have np.inf and np.nan at this point in ratio
    # if those are the only values, then we should stop
    ratio.replace(np.inf, np.nan, inplace=True)
    if ratio.isna().all():
        return (None, "Cannot compute ratio"), (None, None)

    ratio_smooth.replace(np.inf, np.nan, inplace=True)
    if ratio_smooth.isna().all():
        # no useful data in smooth line, but data for dots is okay
        # Give up anyway
        return (None, "Cannot compute smooth ratio"), (None, None)

    # computes q2/q1
    # compute the actual doubling time
    dtime = double_time_exponential(ratio, t2_minus_t1=1)
    dtime_smooth = double_time_exponential(ratio_smooth, t2_minus_t1=1)

    if debug:
        print(f"len(dtime) = {len(dtime.dropna())}, {dtime}")
        print(f"len(dtime_smooth) = {len(dtime_smooth.dropna())}, {dtime_smooth}")

    # can have np.inf and np.nan at this point in dtime_smooth and dtime
    # if those are the only values, then we should stop
    dtime_smooth.replace(np.inf, np.nan, inplace=True)
    if dtime_smooth.isna().all():
        # We could at this point carry on and return the dtime, but not dtime_smooth.
        # This may not be a common use case and not worth the extra complications.
        return (None, "Cannot compute doubling time"), (None, None)

    dtime.replace(np.inf, np.nan, inplace=True)
    if dtime.isna().all():
        return (None, "Cannot compute smooth doubling time"), (None, None)

    dtime_label = region + " doubling time " + label
    dtime_smooth_label = dtime_label + ' 7-day rolling mean (stddev=3)'
    # simplified label
    dtime_smooth_label = dtime_label + ' (rolling mean)'

    return (dtime, dtime_label), (dtime_smooth, dtime_smooth_label)



def compute_growth_factor(series):
    """returns (growth, smooth)

    where 'growth' is a tuple of (series, label)
    and smooth is a tuple of (series, label).

    'growth' returns the raw data (with nan's dropped)
    'smooth' makes the data smoother

    """

    # start from smooth diffs as used in plot 1
    (change, change_label) , (smooth, smooth_label), \
        (smooth2, smooth2_label) = compute_daily_change(series)

    # Compute ratio of yesterday to day
    f = smooth.pct_change() + 1  # compute ratio of subsequent daily changes
                                 # f for growth Factor
    label = ""
    growth = (f, label)

    # division by zero may lead to np.inf in the data: get rid of that
    f.replace(np.inf, np.nan, inplace=True)  # seems not to affect plot

    # Compute smoother version for line in plots
    f_smoothed = f.rolling(7, center=True, win_type='gaussian', min_periods=3).mean(std=2)
    smooth_label = f"Gaussian window (stddev=2 days)"
    # simplified label
    smooth_label = "(rolling mean)"

    smoothed = f_smoothed, smooth_label

    return growth, smoothed


def compute_R(daily_change, tau=4):
    """Given a time series s, estimate R based on description from RKI [1].

    [1] [Robert Koch Institute: Epidemiologisches Bulletin 17 | 2020 23. April 2020]
    https://www.rki.de/DE/Content/Infekt/EpidBull/Archiv/2020/Ausgaben/17_20.html

    Steps:

    1. Compute change from day to day
    2. Take tau-day averages (tau=4 is recommended as of April/May 2020)
    3. divide average from days 4 to 7 by averages from day 0 to 3, and use this data point for day[7]

    """
    # change = s.diff()
    change = daily_change
    mean4d = change.rolling(tau).mean()
    R = mean4d / mean4d.shift(tau)
    R2 = R.shift(-tau)  # this is not the RKI method, but seems more appropriate:
                        # we centre the reported value between the 2-intervals of length tau
                        # that have been used to compute it.

    # Can we create an R-value of 1.0 for small numbers (approaching 0)
    # of new cases/deaths? At least if we have no new cases, then
    # R=1 seems a reasonable outcome.
    R2[(mean4d.shift(tau) == 0.0) & (mean4d == 0)] = 1.0

    return R2


def min_max_in_past_n_days(series, n, at_least = [0.75, 1.25], alert=[0.1, 100], print_alert=False):
    """Given a time series, find the min and max values in the time series within the last n days.

    If those values are within the interval `at_least`, then use the values in at_least as the limits.
    if those values are outside the interval `at_least` then exchange the interval accordingly.

    If the values exceed the min and max value in 'alerts', then print an error message.
    Return min, max.
    """
    if n > len(series):
        n = len(series)

    series = series.replace(math.inf, math.nan)

    min_ = series[-n:].min() - 0.1    # the -0.1 is to make extra space because the line we draw is thick
    max_ = series[-n:].max() + 0.1

    if min_ < at_least[0]:
        min_final = min_
    else:
        min_final = at_least[0]

    if max_ > at_least[1]:
        max_final = max_
    else:
        max_final = at_least[1]

    if print_alert:
        if max_final > alert[1]:
            # print(f"Large value for R_max = {max_final} > {alert[1]} in last {n} days: \n", series[-n:])
            print(f"Large value for R_max = {max_final} > {alert[1]} in last {n} days: \n")
        if min_final < alert[0]:
            # print(f"Small value for R_min = {min_final} < {alert[0]} in last {n} days: \n", series[-n:])
            print(f"Small value for R_min = {min_final} < {alert[0]} in last {n} days: \n")


    # print(f"DDD: min_={min_}, max_={max_}")
    return min_final, max_final
