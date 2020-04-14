import pandas as pd
from pandas import DatetimeIndex
import matplotlib.pyplot as plt
import coronavirus as c


def mock_get_country(country="China"):
    cases_values = [548, 643, 920, 1406, 2075, 2877, 5509, 6087, 8141, 9802, 11891, 16630, 19716, 23707, 27440, 30587, 34110, 36814, 39829, 42354, 44386, 44759, 59895, 66358, 68413, 70513, 72434, 74211, 74619, 75077, 75550, 77001, 77022, 77241, 77754, 78166, 78600, 78928, 79356, 79932, 80136, 80261, 80386, 80537, 80690, 80770, 80823, 80860, 80887, 80921, 80932, 80945, 80977, 81003, 81033, 81058, 81102, 81156, 81250, 81305, 81435, 81498, 81591, 81661, 81782, 81897, 81999, 82122, 82198, 82279, 82361, 82432, 82511, 82543, 82602, 82665, 82718, 82809, 82883, 82941]
    cases_index = "DatetimeIndex(['2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25',  '2020-01-26', '2020-01-27', '2020-01-28', '2020-01-29',  '2020-01-30', '2020-01-31', '2020-02-01', '2020-02-02',  '2020-02-03', '2020-02-04', '2020-02-05', '2020-02-06',  '2020-02-07', '2020-02-08', '2020-02-09', '2020-02-10',  '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14',  '2020-02-15', '2020-02-16', '2020-02-17', '2020-02-18',  '2020-02-19', '2020-02-20', '2020-02-21', '2020-02-22',  '2020-02-23', '2020-02-24', '2020-02-25', '2020-02-26',  '2020-02-27', '2020-02-28', '2020-02-29', '2020-03-01',  '2020-03-02', '2020-03-03', '2020-03-04', '2020-03-05',  '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09',  '2020-03-10', '2020-03-11', '2020-03-12', '2020-03-13',  '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17',  '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21',  '2020-03-22', '2020-03-23', '2020-03-24', '2020-03-25',  '2020-03-26', '2020-03-27', '2020-03-28', '2020-03-29',  '2020-03-30', '2020-03-31', '2020-04-01', '2020-04-02',  '2020-04-03', '2020-04-04', '2020-04-05', '2020-04-06',  '2020-04-07', '2020-04-08', '2020-04-09', '2020-04-10'], dtype='datetime64[ns]', freq=None)"

    cases = pd.Series(data=cases_values, index=eval(cases_index))
    cases.country = "China"
    deaths = cases.copy(deep=True)
    deaths.values[:] = cases.values * 0.1
    deaths.country = "China"
    deaths.label='deaths'
    cases.label='cases'
    return cases, deaths


def test_mock_get_country():
    cases, deaths = mock_get_country()
    assert cases.shape == (80,)
    assert deaths.shape == (80,)
    assert deaths.label == 'deaths'
    assert deaths.country == 'China'


def test_overview():
    axes, cases, deaths = c.overview("China")
    assert cases.label == 'cases'
    assert cases.country == 'China'
    assert deaths.label == 'deaths'
    assert deaths.country == 'China'

    isinstance(deaths, pd.core.series.Series)
    isinstance(deaths, pd.core.series.Series)


def test_get_country_data():
    # Germany
    cases, deaths = c.get_country_data(country="Germany",
                                       subregion="SK Hamburg")
    assert cases.name == "AnzahlFall"
    assert deaths.name == "AnzahlTodesfall"
    assert cases.country == 'Germany-SK Hamburg'
    assert deaths.country == 'Germany-SK Hamburg'

    c2, d2 = c.get_country_data(country="United Kingdom")
    assert c2.country == "United Kingdom"
    assert c2.label == "cases"
    assert d2.label == "deaths"


def test_compute_plot1():
    cases, deaths = mock_get_country()
    change, smooth, smooth2 = c.compute_plot1(cases)
    assert isinstance(change[0], pd.Series)
    assert isinstance(smooth[0], pd.Series)
    assert isinstance(smooth2[0], pd.Series)
    assert isinstance(change[1], str)
    assert isinstance(smooth[1], str)
    assert isinstance(smooth2[1], str)

    assert change[0].shape == (79,)
    assert smooth[0].shape == (79,)
    assert smooth2[0].shape == (79,)

    # assure that we haven't changed the data significantly; some change can come from
    # - nans, where the rolling function will 'create' a data point (but no nan's in this data set)
    # - missing points at the boundary, or interpolation at the boundary not based on 7 points.
    #
    # We just take the current values and assume they are correct. If the smoothing parameters
    # are changed, then these need to be updated.
    assert abs(change[0].sum() - 82393) < 0.1  # original data, should be the same as cases[-1]
    assert abs(smooth[0].sum() - 82664.7) < 1
    assert abs(smooth2[0].sum() - 82914.7) < 1


def test_plot_change_bar():
    cases, deaths = mock_get_country()
    fig, ax = plt.subplots()
    ax = c.plot_change_bar(ax, cases, 'C1')
    fig.savefig('test-plot1.pdf')


def test_compute_growth_factor():
    cases, deaths = mock_get_country()
    f, smooth = c.compute_growth_factor(cases)
    assert isinstance(f[0], pd.Series)
    assert isinstance(smooth[0], pd.Series)
    assert isinstance(f[1], str)
    assert isinstance(smooth[1], str)

    assert f[0].shape == (79,)
    assert smooth[0].shape == (79,)

    # assure that we haven't changed the data significantly; some change can come from
    # - nans, where the rolling function will 'create' a data point (but no nan's in this data set)
    # - missing points at the boundary, or interpolation at the boundary not based on 7 points.
    #
    # We just take the current values and assume they are correct. If the smoothing parameters
    # are changed, then these need to be updated.
    assert abs(f[0].dropna().sum() - 77.3) < 0.1  # original data, should be the same as cases[-1]
    assert abs(smooth[0].sum() - 78.6) < 0.1



def test_plot_growth_factor():
    cases, deaths = mock_get_country()
    fig, ax = plt.subplots()
    ax = c.plot_growth_factor(ax, cases, 'C1')
    fig.savefig('test-growth_factor.pdf')


def test_plot_growth_factor_fetch_data():
    """Similar to test above, but using fresh data"""
    for country in ["Korea, South", "China", "Germany"]:
        cases, deaths = c.get_country(country)
        fig, ax = plt.subplots()
        c.plot_growth_factor(ax, cases, 'C1');
        c.plot_growth_factor(ax, deaths, 'C0');
        fig.savefig(f'test-growth-factor-{country}.pdf')
