import datetime
import numpy as np
import pandas as pd
from pandas import DatetimeIndex
import matplotlib.pyplot as plt
import oscovida as c



def mock_get_country_data_johns_hopkins(country="China"):
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


def test_mock_get_country_data_johns_hopkins():
    cases, deaths = mock_get_country_data_johns_hopkins()
    assert cases.shape == (80,)
    assert deaths.shape == (80,)
    assert deaths.label == 'deaths'
    assert deaths.country == 'China'


def test_overview():
    axes, cases, deaths = c.overview("China")
    assert cases.name == 'China cases'
    assert deaths.name == 'China deaths'

    isinstance(deaths, pd.core.series.Series)
    isinstance(deaths, pd.core.series.Series)


def test_US_overview():
    axes, cases, deaths = c.overview(country="US", region="New Jersey")
    assert cases.name == 'US-New Jersey cases'
    assert deaths.name == 'US-New Jersey deaths'

    isinstance(deaths, pd.core.series.Series)
    isinstance(deaths, pd.core.series.Series)


def test_get_US_region_list():
    x = c.get_US_region_list()
    assert x[0] == "Alabama"
    assert "Hawaii" in x
    assert len(x) > 50  # at least 50 states, plus diamond Princess


def test_Hungary_overview():
    axes, cases, deaths = c.overview(country="Hungary", region="Baranya")
    assert cases.name == 'Hungary-Baranya cases'
    assert deaths is None

    isinstance(cases, pd.core.series.Series)
    isinstance(deaths, type(None))


def test_get_Hungary_region_list():
    x = c.get_counties_hungary()
    assert x[0] == "Bács-Kiskun"
    assert "Budapest" in x
    assert len(x) == 20  # 19 county and the capital city


def test_fetch_data_hungary():
    hungary = c.fetch_data_hungary()
    assert type(hungary) == pd.core.frame.DataFrame
    assert hungary.shape[1] == 21  # date, 19 counties, capital city
    assert 'Budapest' in hungary.columns


def test_choose_random_counties():
    # Hungary related
    with_local = c.choose_random_counties(exclude_region="Baranya", size=18)
    print(with_local)
    assert 'Baranya' not in with_local
    assert len(with_local) == 19


def test_make_compare_plot_hungary():
    with_local = c.choose_random_counties(exclude_region="Baranya", size=18)
    axes, cases, deaths = c.make_compare_plot_hungary("Baranya", compare_with_local=with_local)

    assert deaths is None
    assert type(cases) == pd.core.frame.DataFrame
    assert cases.shape[1] == 20  # counties and the capital city


def test_label_from_region_subregion():
    assert c.label_from_region_subregion(("Hamburg", None)) == "Hamburg"
    assert c.label_from_region_subregion("Hamburg") == "Hamburg"
    assert c.label_from_region_subregion(("Schleswig Holstein", "Pinneberg")) == "Schleswig Holstein-Pinneberg"




def test_get_country_data():
    # Germany
    cases, deaths, region_label = c.get_country_data(country="Germany",
                                                     subregion="SK Hamburg")
    print(f"region_label = {region_label}")
    print(f"deaths = {type(deaths)}")
    print(f"empty")
    assert cases.name == 'Germany-SK Hamburg cases'
    assert deaths.name == 'Germany-SK Hamburg deaths'
    assert region_label == 'Germany-SK Hamburg'

    c2, d2, region_label = c.get_country_data(country="United Kingdom")
    assert c2.name == "United Kingdom cases"
    assert d2.name == "United Kingdom deaths"
    assert region_label == "United Kingdom"


def test_compute_daily_change():
    cases, deaths = mock_get_country_data_johns_hopkins()
    change, smooth, smooth2 = c.compute_daily_change(cases)
    assert isinstance(change[0], pd.Series)  # data
    assert isinstance(smooth[0], pd.Series)  # data
    assert isinstance(smooth2[0], pd.Series)  # data
    assert isinstance(change[1], str)  # label
    assert isinstance(smooth[1], str)  # label
    assert isinstance(smooth2[1], str)  # label

    assert change[0].shape == (79,)
    assert smooth[0].shape == (79,)
    assert smooth2[0].shape == (79,)

    # The daily diffs should sum up to be the same as the total number in the
    # original series minus the first data point3
    # The total number is the last data point in the input series, i.e. cases[-1]
    change_data = change[0]
    assert abs(change_data.sum() + cases[0] - cases[-1]) < 1e-8

    # for the mock data: cases[-1] - cases[0] is 82393. Explicitely done:
    assert abs(change_data.sum() - 82393) < 1e-8  

    # assure that we haven't changed the data significantly when averaging and smoothing:
    # some change can come from
    # - nans, where the rolling function will 'create' a data point (but no nan's in this data set)
    # - missing points at the boundary, or interpolation at the boundary not based on 7 points.
    #
    # We just take the current values and assume they are correct. If the smoothing parameters
    # are changed, then these need to be updated.
    smooth_data = smooth[0]
    assert abs(smooth_data.sum() - 82664.7) < 1
    smooth2_data = smooth2[0]
    assert abs(smooth2_data.sum() - 82914.7) < 1


 
def test_plot_daily_change():
    cases, deaths = mock_get_country_data_johns_hopkins()
    fig, ax = plt.subplots()
    ax = c.plot_daily_change(ax, cases, 'C1')
    fig.savefig('test-plot_daily_change.pdf')


def test_compute_growth_factor():
    cases, deaths = mock_get_country_data_johns_hopkins()
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



#def test_plot_growth_factor():
#    cases, deaths = mock_get_country()
#    fig, ax = plt.subplots()
#    ax = c.plot_growth_factor(ax, cases, 'C1')
#    fig.savefig('test-growth_factor.pdf')
#
#
#def test_plot_growth_factor_fetch_data():
#    """Similar to test above, but using fresh data"""
#    for country in ["Korea, South", "China", "Germany"]:
#        cases, deaths = c.get_country(country)
#        fig, ax = plt.subplots()
#        c.plot_growth_factor(ax, cases, 'C1');
#        c.plot_growth_factor(ax, deaths, 'C0');
#        fig.savefig(f'test-growth-factor-{country}.pdf')

def test_plot_reproduction_number ():
    cases, deaths = mock_get_country_data_johns_hopkins()
    fig, ax = plt.subplots()
    ax = c.plot_reproduction_number(ax, cases, 'C1')
    fig.savefig('test-reproduction_number.pdf')


def test_plot_reproduction_number_fetch_data():
    """Similar to test above, but using fresh data"""
    for country in ["Korea, South", "China", "Germany"]:
        cases, deaths = c.get_country_data_johns_hopkins(country)
        fig, ax = plt.subplots()
        c.plot_reproduction_number(ax, cases, 'C1', labels=("Germany", "cases"));
        c.plot_reproduction_number(ax, deaths, 'C0', labels=("Germany", "deaths"));
        fig.savefig(f'test-reproduction_number-{country}.pdf')



def test_compose_dataframe_summary():
    cases, deaths = mock_get_country_data_johns_hopkins()

    table = c.compose_dataframe_summary(cases, deaths)
    assert table['total cases'][-1] == 643

    # check that most recent data item is last
    print(table)
    


def test_get_cases_last_week():
    index = pd.date_range(start='1/1/2018', end='1/08/2018', freq='D')
    z = pd.Series(np.zeros(shape=index.shape), index=index)
    assert c.get_cases_last_week(z) == 0

    index = pd.date_range(start='1/1/2018', end='1/08/2018', freq='D')
    z = pd.Series(np.ones(shape=index.shape), index=index)
    assert c.get_cases_last_week(z) == 0
    assert c.get_cases_last_week(z.cumsum()) == 7

    cases, deaths = mock_get_country_data_johns_hopkins(country="China")
    assert c.get_cases_last_week(cases) == 430



def test_pad_cumulative_series_to_yesterday():
    # create fake data
    now = datetime.datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - pd.Timedelta("1D")
    point1 = today - pd.Timedelta("10D")
    point2 = today - pd.Timedelta("3D")
    index = pd.date_range(start=point1, end=point2)

    x = pd.Series(data=range(len(index)), index=index)
    # 2020-05-18    0
	# 2020-05-19    1
	# 2020-05-20    2
	# 2020-05-21    3
	# 2020-05-22    4
	# 2020-05-23    5
	# 2020-05-24    6
	# 2020-05-25    7
	# Freq: D, dtype: int64
    assert x[x.index.max()] == 7

    x2 = c.pad_cumulative_series_to_yesterday(x)
    assert x2.index.max() == yesterday
    assert x2[-1] == 7
    assert x2[-2] == 7
    assert x2[-3] == 7
    assert x2[-4] == 6


    index2 = pd.date_range(start=point1, end=yesterday)

    y = pd.Series(data=range(len(index2)), index=index2)
    y2 = c.pad_cumulative_series_to_yesterday(y)
    assert y.shape == (10,)
    assert y2.shape == y.shape
