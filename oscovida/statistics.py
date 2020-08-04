import pandas as pd


@pd.api.extensions.register_series_accessor('covid')
class CovidSeriesAccessor:
    def __init__(self, pandas_object: pd.Series):
        self._obj = pandas_object

    def daily_change(self) -> pd.Series:
        """Computes the daily change for the series

        Returns
        -------
        pd.Series
            Pandas series with

        Examples
        --------
        Expected to be used with Pandas pipe operators:
        >>> region = oscovida.Regions('GBR')
        >>> region.covid.smooth()
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
        return self._obj.diff().dropna()

    # @propagate_metadata
    def smooth(self, kind: str = 'weak') -> pd.Series:
        smoothing_args = {
            'weak': (
                {
                    'window': 9,
                    'center': True,
                    'win_type': 'gaussian',
                    'min_periods': 1,
                },
                {'mean_std': 3,},
            ),
            'strong': (
                {
                    'window': 4,
                    'center': True,
                    'win_type': 'gaussian',
                    'min_periods': 1,
                },
                {'mean_std': 2,},
            ),
        }

        res = self._obj.rolling(**smoothing_args[kind][0]).mean(
            std=smoothing_args[kind][1]['mean_std']
        )

        #  Metadata propagation is broken in Pandas so this doesn't work
        # res.oscovida_metadata = {'smooth': (kind, smoothing_args[kind])}
        # res.attrs['smooth'] = (kind, smoothing_args[kind])

        return res

    def doubling_time(self) -> pd.Series:
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

    def growth_factor(self) -> pd.Series:
        raise NotImplementedError

    def r_number(self) -> pd.Series:
        raise NotImplementedError

    def min_max(self) -> pd.Series:
        raise NotImplementedError


@pd.api.extensions.register_dataframe_accessor('covid')
class CovidDataFrameAccessor:
    def __init__(self, pandas_object):
        self._obj = pandas_object

    # @propagate_metadata
    def daily_change(self) -> pd.DataFrame:
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
        self._obj['tests_daily'] = self._obj['tests'].covid.daily_change()
        self._obj['confirmed_daily'] = self._obj['confirmed'].covid.daily_change()
        self._obj['recovered_daily'] = self._obj['recovered'].covid.daily_change()
        self._obj['deaths_daily'] = self._obj['deaths'].covid.daily_change()

        self._obj.attrs['columns'] |= set(
            ['tests_daily', 'confirmed_daily', 'recovered_daily', 'deaths_daily']
        )

        return self._obj

    # @propagate_metadata
    def smooth(self, kind: str = 'weak') -> pd.DataFrame:
        standard_columns = set(['tests', 'confirmed', 'recovered', 'deaths'])
        oscovida_columns = self._obj.attrs['columns']
        all_columns = oscovida_columns | standard_columns
        for column in all_columns:
            original_column = self._obj[column]
            smoothed_column = original_column.covid.smooth(kind=kind)

            original_attrs = original_column.attrs
            smoothed_attrs = smoothed_column.attrs

            merged_attrs = {**original_attrs, **smoothed_attrs}
            merged_attrs = merged_attrs if merged_attrs else {}
            print("attrs-m: ", id(merged_attrs), " ", merged_attrs)

            # self._obj = self._obj.assign(**{column + '_smoothed': smoothed_column})
            self._obj[column + '_smoothed'] = smoothed_column
            print(
                "attrs-a: ",
                id(self._obj[column + '_smoothed']),
                " ",
                self._obj[column + '_smoothed'].attrs,
            )
            self._obj[column + '_smoothed'].__finalize__(smoothed_column)
            # self._obj[column + '_smoothed'].attrs[randint(0, 100)] = 'rand'
            # self._obj[column + '_smoothed'].attrs = merged_attrs.copy()
            print(
                "attrs-b: ",
                id(self._obj[column + '_smoothed'].attrs),
                " ",
                self._obj[column + '_smoothed'].attrs,
            )
            print()

        for column in all_columns:
            print(column)
            print(
                "attrs-c: ",
                id(self._obj[column + '_smoothed'].attrs),
                " ",
                self._obj[column + '_smoothed'].attrs,
            )
            print()

        return self._obj

    def doubling_time(self) -> pd.DataFrame:
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

    def growth_factor(self) -> pd.DataFrame:
        raise NotImplementedError

    def r_number(self) -> pd.DataFrame:
        raise NotImplementedError

    def min_max(self) -> pd.DataFrame:
        raise NotImplementedError
