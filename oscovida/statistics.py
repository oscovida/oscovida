import pandas as pd

from functools import singledispatch


def daily_change(df: pd.DataFrame) -> pd.DataFrame:
    """Computes the daily change for the following columns:
    - `tests` -> `tests_daily`
    - `confirmed` -> `confirmed_daily`
    - `recovered` -> `recovered_daily`
    - `deaths` -> `deaths_daily`

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing a table formatted as per the Covid19DataHub standard

    Returns
    -------
    pd.DataFrame
        DataFrame with daily change columns added

    Examples
    --------
    Expected to be used with Pandas pipe operators:
    >>> region = oscovida.Regions('GBR')
    >>> (region.data
            .pipe(daily_change)
            .filter(regex='(daily)')
            .describe()
        )
            tests_daily  confirmed_daily  recovered_daily  deaths_daily
    count     193.00000        193.00000       193.000000    193.000000
    mean    41710.73057       1532.73057         1.782383    235.756477
    std     45077.23326       1715.23285        16.026485    306.731913
    min         0.00000          0.00000         0.000000      0.000000
    25%         0.00000          6.00000         0.000000      0.000000
    50%     19316.00000        807.00000         0.000000    111.000000
    75%     81402.00000       2706.00000         0.000000    365.000000
    max    157696.00000       5490.00000       209.000000   1173.000000
    """
    df['tests_daily'] = df.tests.diff().dropna()
    df['confirmed_daily'] = df.confirmed.diff().dropna()
    df['recovered_daily'] = df.recovered.diff().dropna()
    df['deaths_daily'] = df.deaths.diff().dropna()

    df._oscovida_metadata['columns'] |= set(
        ['tests_daily', 'confirmed_daily', 'recovered_daily', 'deaths_daily']
    )
    return df


@singledispatch
def smooth(*args, **kwargs):
    raise NotImplementedError("`smooth` requires a Pandas `DataFrame` or `Series`")


@smooth.register
def _(df: pd.DataFrame, kind: str = 'weak') -> pd.DataFrame:
    standard_columns = set(['tests', 'confirmed', 'recovered', 'deaths'])
    oscovida_columns = df._oscovida_metadata['columns']
    all_columns = oscovida_columns | standard_columns
    for column in all_columns:
        ds = df[column]
        df[column + '_smoothed'] = ds.pipe(smooth, kind=kind)

    return df


@smooth.register
def _(ds: pd.Series, kind: str = 'weak') -> pd.Series:
    smoothing_args = {
        'weak': (
            {'window': 9, 'center': True, 'win_type': 'gaussian', 'min_periods': 1,},
            {'mean_std': 3,},
        ),
        'strong': (
            {'window': 4, 'center': True, 'win_type': 'gaussian', 'min_periods': 1,},
            {'mean_std': 2,},
        ),
    }

    return ds.rolling(**smoothing_args[kind][0]).mean(
        std=smoothing_args[kind][1]['mean_std']
    )


@singledispatch
def doubling_time(*args, **kwargs):
    """Computes the doubling time for a Pandas `DataFrame` or `Series`

    If called on a `DataFrame`, assumes that `daily_change` has already been
    computed, and adds the following columns:
    - `tests_daily` -> 'tests_doubling_time`
    - `confirmed_daily` -> 'confirmed_doubling_time`
    - `recovered_daily` -> 'recovered_doubling_time`
    - `deaths_daily` -> 'deaths_doubling_time`

    If called on a `Series`, computes the doubling time for the values of that
    series

    Parameters
    ----------
    df: Union[pd.DataFrame, pd.Series]
        - pd.DataFrame containing a table formatted as per the Covid19DataHub standard
        - pd.Series of numbers

    Returns
    -------
    df: Union[pd.DataFrame, pd.Series]
        - pd.DataFrame with daily change columns added
        - pd.Series of doubling time

    Raises
    ------
    ValueError
        Raised if the first argument is not a `DataFrame` or `Series`

    Examples
    --------
    Expected to be used with Pandas pipe operators, called with a `DataFrame`:
    >>> region = oscovida.Regions('GBR')
    >>> (region.data
            .pipe(daily_change)
            .pipe(doubling_time)
        )

    Or called with a `Series`:
    >>> deaths_daily = oscovida.Regions('GBR').pipe(daily_change).deaths_daily
    >>> deaths_daily.pipe(doubling_time)
    """
    raise NotImplementedError(
        "`doubling_time` requires a Pandas `DataFrame` or `Series`"
    )


@doubling_time.register
def _(df: pd.DataFrame) -> pd.DataFrame:
    print("DF!")


@doubling_time.register
def _(ds: pd.Series) -> pd.Series:
    print("Series!")


def growth_factor(df: pd.DataFrame) -> pd.DataFrame:
    pass


def r_number(df: pd.DataFrame) -> pd.DataFrame:
    pass


def min_max(df: pd.DataFrame) -> pd.DataFrame:
    pass
