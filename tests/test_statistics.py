import hypothesis.strategies as st
import numpy as np
import pandas as pd
from hypothesis import given, settings
from hypothesis.extra.pandas import range_indexes, series

import oscovida.statistics as statistics

daily_cases = series(
    index=range_indexes(min_size=30),
    #  Some areas have negative new cases/deaths to correct for previous errors
    elements=st.integers(min_value=-10_000, max_value=100_000),
)


@given(daily_cases=daily_cases)
def test_daily_hypothesis(daily_cases: pd.Series):
    cumulative_cases = daily_cases.cumsum()

    assert all(daily_cases[1:] == statistics.daily(cumulative_cases).to_numpy())


@given(daily_cases=daily_cases)
@settings(deadline=None)
def test_smooth_hypothesis(daily_cases):
    #  Test that the smoothing options work without raising an error
    weak = statistics.smooth(daily_cases, kind='weak')
    strong = statistics.smooth(daily_cases, kind='strong', compound=False)
    strong_compound = statistics.smooth(daily_cases, kind='strong', compound=True)


@given(daily_cases=daily_cases)
def test_doubling_time_hypothesis(daily_cases):
    statistics.doubling_time(daily_cases)


def test_doubling_time_exp():
    exponential_series = pd.Series(np.exp(np.linspace(0, 100, 101)))

    doubling_time = statistics.doubling_time(exponential_series).dropna()

    #  Doubling time of an exponential series should be constant
    assert len(doubling_time.round(5).unique()) == 1


@given(daily_cases=daily_cases, tau=st.integers(min_value=0, max_value=100))
def test_r_number_hypothesis(daily_cases, tau):
    statistics.r_number(daily_cases, tau)


def test_r_number_exp():
    exponential_series = pd.Series(np.exp(np.linspace(0, 100, 101)))

    r_number = statistics.r_number(exponential_series).dropna()

    #  As before, r number time of an exponential series should be constant
    assert len(r_number.round(5).unique()) == 1


@given(daily_cases=daily_cases)
def test_growth_factor_hypothesis(daily_cases):
    statistics.growth_factor(daily_cases)


def test_growth_factor_exp():
    exponential_series = pd.Series(np.exp(np.linspace(0, 100, 101)))

    growth_factor = statistics.growth_factor(exponential_series).dropna()

    #  As before, growth factor of an exponential series should be constant
    assert len(growth_factor.round(5).unique()) == 1


@given(
    daily_cases=daily_cases,
    n=st.integers(min_value=0, max_value=30),
    at_least=st.tuples(
        st.floats(min_value=0, max_value=100), st.floats(min_value=0, max_value=100)
    ),
)
def test_min_max_hypothesis(daily_cases, n, at_least):
    daily_min, daily_max = statistics.min_max(daily_cases, n, at_least)

    assert daily_min <= at_least[0]
    assert daily_max >= at_least[1]
