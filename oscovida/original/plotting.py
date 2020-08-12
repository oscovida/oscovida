from bisect import bisect

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import FuncFormatter, ScalarFormatter


# choose font - can be deactivated
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Inconsolata']

# need many figures for index.ipynb and germany.ipynb
rcParams['figure.max_open_warning'] = 50

plt.style.use('ggplot')


def plot_time_step(ax, series, style="-", labels=None, logscale=True):
    """Plot the series as cumulative cases/deaths, plotted as step function.
    Parameters:
    - ax : axis object from matplotlib
    - series: the actual data as pandas Series
    - style : matplotlib style/Colour
    - labels: tuple of (region_name, kind) where
              both elements are strings, and 'kind' is either 'cases' or 'deaths'.
    - logscale: plot y-axis in logscale (default=True)

    Returns ax object.
    """

    ax.step(series.index, series.values, style, label=series.name, linewidth=LW)
    if logscale:
        ax.set_yscale('log')
    ax.legend()
    ax.set_ylabel("total numbers")
    ax.yaxis.set_major_formatter(ScalarFormatter())
    return ax


def plot_daily_change(ax, series, color, labels=None):
    """Given a series of data and matplotlib axis ax, plot the
    - difference in the series data from day to day as bars and plot a smooth
    - line to show the overall development

    - series is pandas.Series with data as index, and cumulative cases (or
    deaths)
    - color is color to be used for plotting

    See plot_time_step for documentation on other parameters.
    """

    bar_alpha = 0.2
    if labels is None:
        label = ""
        region = ""
    else:
        region, label = labels

    ax_label = region + " new " + label

    (
        (change, change_label),
        (smooth, smooth_label),
        (smooth2, smooth2_label),
    ) = compute_daily_change(series)

    ax.bar(
        change.index,
        change.values,
        color=color,
        label=ax_label,
        alpha=bar_alpha,
        linewidth=LW,
    )

    ax.plot(
        smooth2.index,
        smooth2.values,
        color=color,
        label=ax_label + " " + smooth2_label,
        linewidth=LW,
    )

    ax.legend()
    ax.set_ylabel('daily change')

    # labels on the right y-axis as well
    ax.tick_params(left=True, right=True, labelleft=True, labelright=True)
    ax.yaxis.set_ticks_position('both')

    # data cleaning: For France, there was a huge spike on 12 April with 26849
    # new infections. This sets the scale to be too large.
    # There was also a value of ~-2000 on 22 April. We limit the y-scale to correct
    # manually for this:
    if region == "France" and label == "cases":
        # get current limits
        ymin, ymax = ax.get_ylim()
        ax.set_ylim([max(-500, ymin), min(10000, ymax)])

    return ax


def plot_reproduction_number(
    ax, series, color_g='C1', color_R='C4', yscale_days=28, max_yscale=10, labels=None
):
    """
    - series is expected to be time series of cases or deaths
    - label is 'cases' or 'deaths' or whatever is desired as the description
    - country is the name of the region/country
    - color_g is the colour for the growth factor
    - color_R is the colour for the reproduction number

    See plot_time_step for documentation on other parameters.
    """

    if labels is None:
        region, label = "", ""
    else:
        region, label = labels

    # get smooth data for growth factor from plot 1 to base this plot on
    (f, f_label), (f_smoothed, smoothed_label) = compute_growth_factor(series)

    label_ = region + " " + label + " daily growth factor " + f_label
    ax.plot(f.index, f.values, 'o', color=color_g, alpha=0.3, label=label_)

    label_ = region + " " + label + " daily growth factor " + smoothed_label
    ax.plot(
        f_smoothed.index,
        f_smoothed.values,
        '-',
        color=color_g,
        label=label_,
        linewidth=LW,
        alpha=0.7,
    )

    # data for computation or R
    smooth_diff = series.diff().rolling(7, center=True, win_type='gaussian').mean(std=4)

    R = compute_R(smooth_diff)
    ax.plot(
        R.index,
        R,
        "-",
        color=color_R,
        label=region + f" estimated R (using {label})",
        linewidth=4.5,
        alpha=1,
    )

    # choose y limits so that all data points of R in the last 28 days are visible
    min_, max_ = min_max_in_past_n_days(R, yscale_days)

    # set upper bound for R
    # (Germany data has huge spike in February )
    if max_ > max_yscale:
        max_ = max_yscale

    ax.set_ylim([min_, max_])

    # Plot ylim interval for debugging
    # ax.plot([R.index.min(), R.index.max()], [min_, min_], 'b-')
    # ax.plot([R.index.min(), R.index.max()], [max_, max_], 'b-')

    ax.set_ylabel(f"R & growth factor\n(based on {label})")
    # plot line at 0
    ax.plot(
        [series.index.min(), series.index.max()], [1.0, 1.0], '-C3'
    )  # label="critical value"
    ax.legend()
    return ax


def plot_doubling_time(ax, series, color, minchange=0.5, labels=None, debug=False):
    """Plot doubling time of series, assuming series is accumulated cases/deaths as
    function of days.

    Returns axis.

    See plot_time_step for documentation on other parameters.
    """

    if labels is None:
        labels = "", ""
    region, label = labels

    (dtime, dtime_label), (dtime_smooth, dtime_smooth_label) = compute_doubling_time(
        series, minchange=minchange, debug=debug, labels=labels
    )

    if dtime is None:
        if debug:
            print(dtime_label)
        return ax

    ax.plot(dtime.index, dtime.values, 'o', color=color, alpha=0.3, label=dtime_label)

    # good to take maximum value from here
    dtime_smooth.replace(
        np.inf, np.nan, inplace=True
    )  # get rid of x/0 results, which affect max()
    ymax = min(
        dtime_smooth.max() * 1.5, 5000
    )  # China has doubling time of 3000 in between

    ## Adding a little bit of additional smoothing just for visual effects
    dtime_smooth2 = dtime_smooth.rolling(
        3, win_type='gaussian', min_periods=1, center=True
    ).mean(std=1)

    ax.set_ylim(0, ymax)
    ax.plot(
        dtime_smooth2.index,
        dtime_smooth2.values,
        "-",
        color=color,
        alpha=1.0,
        label=dtime_smooth_label,
        linewidth=LW,
    )
    ax.legend()
    ax.set_ylabel("doubling time [days]")
    return ax


def plot_logdiff_time(
    ax,
    df,
    xaxislabel,
    yaxislabel,
    style="",
    labels=True,
    labeloffset=2,
    v0=0,
    highlight={},
    other_lines_alpha=0.4,
):
    """highlight is dictionary: {country_name : color}

    - df: DataFrame with time series to align
    """

    for i, col in enumerate(df.columns):
        # print(f"plot_logdiff: Processing {i} {col}")
        if col in highlight:
            # print(f"Found highlight: {col}")
            alpha = 1.0
            color = highlight[col]
            linewidth = 4
        else:
            alpha = other_lines_alpha
            # have only 10 colours
            color = style + 'C' + str(i % 10)
            linewidth = 2

        ax.plot(
            df.index, df[col].values, color, label=col, linewidth=linewidth, alpha=alpha
        )
        if labels:
            tmp = df[col].dropna()
            if len(tmp) > 0:  # possible we have no data points
                x, y = tmp.index[-1], tmp.values[-1]

                # If we use the 'annotate' function on a data point with value 0 or a negative value,
                # we run into a bizarre bug that the created figure has very large dimensions in the
                # vertical direction when rendered to svg. The next line prevents this.
                #
                # Our fix/hack means that the label of the country will not be visible. That's not so bad
                # at the moment as the situation of zero new deaths causes the problem, and the infections
                # are higher and non-zero, thus we can see the country label in the infections plot.
                #
                # If this stops, we could consider choosing a data point from
                # earlier in the series to put the label there.
                #
                # The comparison for "y < 0" should not be necessary as the new deaths per day can at
                # most be zero. However, for Australia, there is a -1 reported for first of June,
                # which can lead to negative values when computing a rolling mean.
                y = np.NaN if y <= 0 else y

                # Add country/region name as text next to last data point of the line:
                ax.annotate(col, xy=(x + labeloffset, y), textcoords='data')
                ax.plot([x], [y], "o" + color, alpha=alpha)
    # ax.legend()
    ax.set_ylabel(yaxislabel)
    ax.set_xlabel(xaxislabel)
    ax.set_yscale('log')
    # use integer numbers for values > 1, and decimal presentation below
    # from https://stackoverflow.com/questions/21920233/matplotlib-log-scale-tick-label-number-formatting/33213196
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:g}'.format(y)))
    # ax.set_xscale('log')    # also interesting
    ax.set_ylim(bottom=set_y_axis_limit(df, v0))
    ax.set_xlim(left=-1)  # ax.set_xlim(-1, df.index.max())
    ax.tick_params(left=True, right=True, labelleft=True, labelright=True)
    ax.yaxis.set_ticks_position('both')


def set_y_axis_limit(data, current_lim):
    """The function analyses the data set given and lowers
    the y-limit if there are data points below `current_lim`

    :param data: data to plot
    :param current_lim: initial y-axis lower limit
    :return: new y-axis lower limit
    """
    data_0 = data[data.index >= 0]  # from "day 0" only
    limits = [0.1, 1, 10, 100]
    # if we have values within the `limits`, we set the lower `y_limit` on the graph to the value on the left of bisect
    # example: if the minimum value is 3, then y_limit = 1
    index = bisect(limits, data_0.min().min())
    if 0 < index < len(limits):
        return limits[index - 1]
    elif index == 0:
        return limits[0]
    else:
        return current_lim


def make_compare_plot(
    main_country,
    compare_with=[
        "Germany",
        "Australia",
        "Poland",
        "Korea, South",
        "Belarus",
        "Switzerland",
        "US",
    ],
    v0c=10,
    v0d=3,
):
    rolling = 7
    df_c, df_d = get_compare_data([main_country] + compare_with, rolling=rolling)
    res_c = align_sets_at(v0c, df_c)
    res_d = align_sets_at(v0d, df_d)

    # We get NaNs for some lines. This seems to originate in the original data set not having a value recorded
    # for all days.
    # For the purpose of this plot, we'll just interpolate between the last and next known values.
    # We limit the number of fills to 3 days. (Just a guess to avoid accidental
    # filling of too many NaNs.)

    res_c = res_c.interpolate(method='linear', limit=3)
    res_d = res_d.interpolate(method='linear', limit=3)

    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    ax = axes[0]
    plot_logdiff_time(
        ax,
        res_c,
        f"days since {v0c} cases",
        "daily new cases\n(rolling 7-day mean)",
        v0=v0c,
        highlight={main_country: "C1"},
    )
    ax = axes[1]
    plot_logdiff_time(
        ax,
        res_d,
        f"days since {v0d} deaths",
        "daily new deaths\n(rolling 7-day mean)",
        v0=v0d,
        highlight={main_country: "C0"},
    )

    fig.tight_layout(pad=1)
    title = f"Daily cases (top) and deaths (below) for {main_country}"
    axes[0].set_title(title)

    return axes, res_c, res_d


def make_compare_plot_germany(
    region_subregion,
    compare_with=[],  # "China", "Italy", "Germany"],
    compare_with_local=[
        'Bayern',
        'Berlin',
        'Bremen',
        'Hamburg',
        'Hessen',
        'Nordrhein-Westfalen',
        'Sachsen-Anhalt',
    ],
    # The 'compare_with_local' subset is chosen to look sensibly on 2 May 2020.
    #                          compare_with_local=['Baden-Württemberg', 'Bayern', 'Berlin',
    #                                              'Brandenburg', 'Bremen', 'Hamburg',
    #                                              'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen',
    #                                              'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland',
    #                                              'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein',  'Thüringen'],
    v0c=10,
    v0d=1,
):
    rolling = 7
    region, subregion = unpack_region_subregion(region_subregion)
    df_c1, df_d1 = get_compare_data_germany(
        (region, subregion), compare_with_local, rolling=rolling
    )
    df_c2, df_d2 = get_compare_data(compare_with, rolling=rolling)

    # need to get index into same timezone before merging
    df_d1.set_index(df_d1.index.tz_localize(None), inplace=True)
    df_c1.set_index(df_c1.index.tz_localize(None), inplace=True)

    df_c = pd.merge(df_c1, df_c2, how='outer', left_index=True, right_index=True)
    df_d = pd.merge(df_d1, df_d2, how='outer', left_index=True, right_index=True)

    res_c = align_sets_at(v0c, df_c)
    res_d = align_sets_at(v0d, df_d)

    # We get NaNs for some lines. This seems to originate in the original data set not having a value recorded
    # for all days.
    # For the purpose of this plot, we'll just interpolate between the last and next known values.
    # We limit the number of fills to 7 days. (Just a guess to avoid accidental
    # filling of too many NaNs.)
    res_c = res_c.interpolate(method='linear', limit=7)
    res_d = res_d.interpolate(method='linear', limit=7)

    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    ax = axes[0]
    plot_logdiff_time(
        ax,
        res_c,
        f"days since {v0c} cases",
        "daily new cases\n(rolling 7-day mean)",
        v0=v0c,
        highlight={res_c.columns[0]: "C1"},
        labeloffset=0.5,
    )
    ax = axes[1]

    plot_logdiff_time(
        ax,
        res_d,
        f"days since {v0d} deaths",
        "daily new deaths\n(rolling 7-day mean)",
        v0=v0d,
        highlight={res_d.columns[0]: "C0"},
        labeloffset=0.5,
    )

    # fig.tight_layout(pad=1)

    title = f"Daily cases (top) and deaths (below) for Germany: {label_from_region_subregion((region, subregion))}"
    axes[0].set_title(title)

    return axes, res_c, res_d


def make_compare_plot_hungary(region: str, compare_with_local: list, v0c=10):
    rolling = 7

    df_c1, _ = get_compare_data_hungary(region, compare_with_local, rolling=rolling)
    # df_c2, _ = get_compare_data(['Germany', 'Italy'], rolling=rolling)

    # need to get index into same timezone before merging
    df_c1.set_index(df_c1.index.tz_localize(None), inplace=True)
    # df_c = pd.merge(df_c1, df_c2, how='outer', left_index=True, right_index=True)

    res_c = align_sets_at(v0c, df_c1)
    res_c = res_c.interpolate(method='linear', limit=7)

    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    plot_logdiff_time(
        axes[0],
        res_c,
        f"days since {v0c} cases",
        "daily new cases\n(rolling 7-day mean)",
        v0=v0c,
        highlight={res_c.columns[0]: "C1"},
        labeloffset=0.5,
    )

    # plot_no_data_available(axes[1], mimic_subplot=axes[0], text="daily new deaths\n(rolling 7-day mean)")
    axes[1].set_visible(False)

    title = f"Daily cases for Hungary: {label_from_region_subregion(region)}"
    axes[0].set_title(title)
    fig.tight_layout(pad=1)
    return axes, res_c, None


def plot_no_data_available(ax, mimic_subplot, text):
    # Hungary county deaths data missing
    xticks = mimic_subplot.get_xticks()
    yticks = mimic_subplot.get_yticks()
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.text(
        xticks.mean(),
        yticks.mean(),
        f'No data available\n to plot {text}',
        horizontalalignment='center',
        verticalalignment='center',
    )
    ax.set_yticklabels([])
    ax.set_xticklabels([])


def overview(country, region=None, subregion=None, savefig=False):
    c, d, region_label = get_country_data(country, region=region, subregion=subregion)
    print(c.name)
    fig, axes = plt.subplots(6, 1, figsize=(10, 15), sharex=False)

    plot_time_step(ax=axes[0], series=c, style="-C1", labels=(region_label, "cases"))
    plot_daily_change(ax=axes[1], series=c, color="C1", labels=(region_label, "cases"))
    # data cleaning
    if country == "China":
        axes[1].set_ylim(0, 5000)
    elif country == "Spain":  # https://github.com/oscovida/oscovida/issues/44
        axes[1].set_ylim(bottom=0)
    plot_reproduction_number(
        axes[3], series=c, color_g="C1", color_R="C5", labels=(region_label, "cases")
    )
    plot_doubling_time(axes[5], series=c, color="C1", labels=(region_label, "cases"))

    if d is not None:
        plot_time_step(
            ax=axes[0], series=d, style="-C0", labels=(region_label, "deaths")
        )
        plot_daily_change(
            ax=axes[2], series=d, color="C0", labels=(region_label, "deaths")
        )
        plot_reproduction_number(
            axes[4],
            series=d,
            color_g="C0",
            color_R="C4",
            labels=(region_label, "deaths"),
        )
        plot_doubling_time(
            axes[5], series=d, color="C0", labels=(region_label, "deaths")
        )
    if d is None:
        plot_no_data_available(
            axes[2], mimic_subplot=axes[1], text='daily change in deaths'
        )
        plot_no_data_available(
            axes[4], mimic_subplot=axes[3], text='R & growth factor (based on deaths)'
        )
        # axes[2].set_visible(False)
        # axes[4].set_visible(False)

    # ax = axes[3]
    # plot_growth_factor(ax, series=d, color="C0")
    # plot_growth_factor(ax, series=c, color="C1")

    # enforce same x-axis on all plots
    for i in range(1, axes.shape[0]):
        axes[i].set_xlim(axes[0].get_xlim())
    for i in range(0, axes.shape[0]):
        axes[i].tick_params(left=True, right=True, labelleft=True, labelright=True)
        axes[i].yaxis.set_ticks_position('both')

    title = f"Overview {country}, last data point from {c.index[-1].date().isoformat()}"
    axes[0].set_title(title)

    # tight_layout gives warnings, for example for Heinsberg
    # fig.tight_layout(pad=1)

    filename = os.path.join(
        "figures", region_label.replace(" ", "-").replace(",", "-") + '.svg'
    )
    if savefig:
        fig.savefig(filename)

    if not subregion and not region:  # i.e. not a region of Germany
        axes_compare, res_c, res_d = make_compare_plot(country)
        return_axes = np.concatenate([axes, axes_compare])

    elif country == "Germany":  # Germany specific plots
        # On 11 April, Mecklenburg Vorpommern data was missing from data set.
        # We thus compare only against those Laender, that are in the data set:
        # germany = fetch_data_germany()
        # laender = list(germany['Bundesland'].drop_duplicates().sort_values())
        axes_compare, res_c, red_d = make_compare_plot_germany((region, subregion))
        return_axes = np.concatenate([axes, axes_compare])
    elif country == "US" and region is not None:
        # skip comparison plot for the US states at the moment
        return_axes = axes
        return return_axes, c, d

    elif country == 'Hungary':
        # choosing random counties. not sure if this make sense or not because not every county has enough data.
        with_local = choose_random_counties(exclude_region=region, size=18)
        axes_compare, res_c, red_d = make_compare_plot_hungary(
            region, compare_with_local=with_local
        )
        return_axes = np.concatenate([axes, axes_compare])
        return return_axes, c, d
    else:
        raise NotImplementedError

    fig2 = plt.gcf()

    if savefig:
        filename = os.path.join(
            "figures", region_label.replace(" ", "-").replace(",", "-") + '2.svg'
        )
        fig2.savefig(filename)

    return return_axes, c, d
