import hypothesis.strategies as st
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis.extra.pandas import columns, data_frames, range_indexes, series

import oscovida.statistics as statistics

#  Tests here use hypothesis to check if calling the functions with a variety
#  of inputs succeeds, the 'actual' tests for the functions are in a notebook

daily_cases = series(
    index=range_indexes(min_size=30),
    #  Some areas have negative new cases/deaths to correct for previous errors
    elements=st.integers(min_value=-10_000, max_value=100_000),
)


@given(daily_cases=daily_cases)
def test_daily(daily_cases: pd.Series):
    cumulative_cases = daily_cases.cumsum()

    assert all(daily_cases[1:] == statistics.daily(cumulative_cases).to_numpy())


@given(daily_cases=daily_cases)
@settings(deadline=None)
def test_smooth(daily_cases):
    #  Test that the smoothing options work without raising an error
    weak = statistics.smooth(daily_cases, kind='weak')
    strong = statistics.smooth(daily_cases, kind='strong', compound=False)
    strong_compound = statistics.smooth(daily_cases, kind='strong', compound=True)


@given(daily_cases=daily_cases, minchange=st.floats(min_value=0, max_value=100))
def test_doubling_time(daily_cases, minchange):
    statistics.doubling_time(daily_cases, minchange)


@given(daily_cases=daily_cases, tau=st.integers(min_value=0, max_value=100))
def test_r_number(daily_cases, tau):
    statistics.r_number(daily_cases, tau)


@given(daily_cases=daily_cases)
def test_growth_factor(daily_cases):
    statistics.growth_factor(daily_cases)


@given(
    daily_cases=daily_cases,
    n=st.integers(min_value=0, max_value=30),
    at_least=st.tuples(
        st.floats(min_value=0, max_value=100), st.floats(min_value=0, max_value=100)
    ),
)
def test_min_max(daily_cases, n, at_least):
    daily_min, daily_max = statistics.min_max(daily_cases, n, at_least)

    assert daily_min <= at_least[0]
    assert daily_max >= at_least[1]
