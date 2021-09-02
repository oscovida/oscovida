import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytest
import oscovida as c
import oscovida.plotting_helpers as oph


def assert_oscovida_object(ax, cases, deaths):
    assert isinstance(ax, np.ndarray)
    assert isinstance(cases, (pd.Series, pd.DataFrame))
    assert isinstance(deaths, (pd.Series, pd.DataFrame))


def mock_get_country_data_johns_hopkins(country="China"):
    cases_values = [548, 643, 920, 1406, 2075, 2877, 5509, 6087, 8141, 9802, 11891, 16630, 19716, 23707, 27440, 30587,
                    34110, 36814, 39829, 42354, 44386, 44759, 59895, 66358, 68413, 70513, 72434, 74211, 74619, 75077,
                    75550, 77001, 77022, 77241, 77754, 78166, 78600, 78928, 79356, 79932, 80136, 80261, 80386, 80537,
                    80690, 80770, 80823, 80860, 80887, 80921, 80932, 80945, 80977, 81003, 81033, 81058, 81102, 81156,
                    81250, 81305, 81435, 81498, 81591, 81661, 81782, 81897, 81999, 82122, 82198, 82279, 82361, 82432,
                    82511, 82543, 82602, 82665, 82718, 82809, 82883, 82941]
    cases_index = pd.date_range("2020-01-22", periods=len(cases_values), freq='D')

    cases = pd.Series(data=cases_values, index=cases_index)
    cases.country = "China"
    deaths = cases.copy(deep=True)
    deaths.values[:] = cases.values * 0.1
    deaths.country = "China"
    deaths.label = 'deaths'
    cases.label = 'cases'
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

    assert_oscovida_object(axes, cases, deaths)
    assert_oscovida_object(*c.overview("Germany", weeks=8))
    assert_oscovida_object(*c.overview("Russia", dates="2020-05-30:2020-06-15"))
    with pytest.raises(ValueError):
        c.overview("Argentina", weeks=8, dates="2020-05-30:2020-06-15")

    days = 10
    dates = pd.date_range("2020-03-01", periods=days, freq='D')
    data1 = np.exp(np.linspace(1, 15, days))
    data2 = np.exp(np.linspace(1, 5, days))

    cases = pd.Series(data1, index=pd.DatetimeIndex(dates))
    deaths = pd.Series(data2, index=pd.DatetimeIndex(dates))

    assert_oscovida_object(*c.overview("Narnia", data=(cases, deaths)))


def test_US_overview():
    axes, cases, deaths = c.overview(country="US", region="New Jersey")
    assert cases.name == 'US-New Jersey cases'
    assert deaths.name == 'US-New Jersey deaths'
    assert_oscovida_object(axes, cases, deaths)


def test_germany_overview():
    axes, cases, deaths = c.overview(country="Germany", region="Hamburg")
    assert cases.name == 'Germany-Hamburg cases'
    assert_oscovida_object(axes, cases, deaths)

    axes, cases, deaths = c.overview(country="Germany", subregion="LK Pinneberg")
    assert deaths.name == 'Germany-LK Pinneberg deaths'
    assert_oscovida_object(axes, cases, deaths)

    axes, cases, deaths = c.overview(country="Germany", subregion="SK Kassel")
    assert cases.name == 'Germany-SK Kassel cases'
    assert deaths.name == 'Germany-SK Kassel deaths'
    assert_oscovida_object(axes, cases, deaths)

    axes, cases, deaths = c.overview(country="Germany", subregion="Städteregion Aachen")
    assert cases.name == 'Germany-Städteregion Aachen cases'
    assert_oscovida_object(axes, cases, deaths)

    axes, cases, deaths = c.overview(country="Germany", subregion="Region Hannover")
    assert cases.name == 'Germany-Region Hannover cases'
    assert deaths.name == 'Germany-Region Hannover deaths'
    assert_oscovida_object(axes, cases, deaths)


def test_get_incidence_rates_german():
    cases, deaths = c.get_incidence_rates_germany()
    number_of_german_districts = 412
    assert len(cases) == len(deaths) == number_of_german_districts


def test_get_US_region_list():
    x = c.get_US_region_list()
    assert x[0] == "Alabama"
    assert "Hawaii" in x
    assert len(x) > 50  # at least 50 states, plus diamond Princess


def test_Hungary_overview():
    axes, cases, deaths = c.overview(country="Hungary", region="Baranya")
    assert cases.name == 'Hungary-Baranya cases'
    assert deaths is None

    isinstance(cases, pd.Series)
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
    # print(with_local)
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
    cases, deaths = c.get_country_data(country="Germany", region="Bayern")
    assert isinstance(deaths, pd.Series)
    assert cases.name == 'Germany-Bayern cases'
    assert deaths.name == 'Germany-Bayern deaths'

    cases, deaths = c.get_country_data(country="Germany", subregion="SK Hamburg")
    assert isinstance(deaths, pd.Series)
    assert cases.name == 'Germany-SK Hamburg cases'
    assert deaths.name == 'Germany-SK Hamburg deaths'

    c2, d2 = c.get_country_data(country="United Kingdom")
    assert c2.name == "United Kingdom cases"
    assert d2.name == "United Kingdom deaths"


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
    assert abs(smooth_data.sum() - 80740.4) < 1
    smooth2_data = smooth2[0]
    assert abs(smooth2_data.sum() - 76903.86) < 1


def test_plot_daily_change():
    cases, deaths = mock_get_country_data_johns_hopkins()
    fig, ax = plt.subplots()
    ax = c.plot_daily_change(ax, cases, 'C1')
    fig.savefig('test-plot_daily_change.pdf')


def test_plot_incidence_rate():
    cases, deaths = mock_get_country_data_johns_hopkins()
    fig, ax = plt.subplots()
    ax = c.plot_incidence_rate(ax, cases, cases.country)
    assert ax is not None
    assert "per 100K people" in ax.get_ylabel()
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
    assert abs(f[0].dropna().sum() - 70.8) < 0.1  # original data, should be the same as cases[-1]
    assert abs(smooth[0].sum() - 73.05) < 0.1


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
    # print(table)


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


def test_germany_get_population():
    germany = c.germany_get_population()

    assert germany.index.name == 'county'
    assert 'population' in germany.columns
    assert 'cases7_per_100k' in germany.columns

    germany_data = c.fetch_data_germany()
    assert set(germany_data['Landkreis']) == set(germany.index)

    hamburg = germany.loc['SK Hamburg'].population
    assert hamburg > 1800000

    pinneberg = germany.loc['LK Pinneberg'].population
    assert pinneberg > 30000

    # https://github.com/oscovida/oscovida/issues/210
    saarpfalz = germany.loc['LK Saarpfalz-Kreis'].population
    assert saarpfalz > 130000

    aachen = germany.loc['Städteregion Aachen'].population
    assert aachen > 500000


def test_germany_get_population_data_online():
    """If this test passes, then the population data for Germany may be online
    again (see https://github.com/oscovida/oscovida/issues/261)
    Hans, 21 August 2021."""
    population = c.fetch_csv_data_from_url(c.rki_population_url)
    population = population.set_index('county')


def test_germany_get_population_backup_data_raw():
    """Sanity check for backup file"""
    df = c._germany_get_population_backup_data_raw()

    # expect 412 districts
    assert len(df) == 412

    # expect about 83 million inhabitants
    pop = df['EWZ']   # EWZ = EinWohnerZahl = population
    total = pop.sum()

    assert 83e6 < total < 83.3e6   # as of Aug 2021: 83166711



def test_get_population():
    world = c.get_population()

    assert world.index.name == 'Country_Region'
    assert 'population' in world.columns

    # Check that the case regions and population regions match
    try:
        assert set(c.fetch_cases().index) == set(world.index)
    except AssertionError:
        failing_states = {'Western Sahara'}
        if set(c.fetch_cases().index).symmetric_difference(set(world.index)) == failing_states:
            pass
        else:
            raise AssertionError

    # Tests will have to be updated in 20+ years when the populations increase
    # more than the 'sensible' lower bound placed here
    # The lower bound exists in case the summing over regions fails somehow
    # and includes areas multiple times
    assert 140_000_000 * 1.5 > world.loc['Russia'].population > 140_000_000
    assert 120_000_000 * 1.5 > world.loc['Japan'].population > 120_000_000
    assert 320_000_000 * 1.5 > world.loc['US'].population > 320_000_000
    assert 80_000_000 * 1.5 > world.loc['Germany'].population > 80_000_000


def test_get_region_label():
    countries = ["China", "Germany", "Hungary", "Russia", "US", "Zimbabwe"]
    for country in countries:
        assert c.get_region_label(country) == country
    assert c.get_region_label(country="US", region="New Jersey") == "United States: New Jersey"
    assert c.get_region_label(country="Germany", region="Hamburg") == "Germany-Hamburg"
    assert c.get_region_label(country="Germany", region="LK Pinneberg") == "Germany-LK Pinneberg"
    assert c.get_region_label(country="Hungary", region="Baranya") == "Hungary-Baranya"


def test_population():
    reference = [("Germany", None, None, 83E6),
                 ("Germany", "Bayern", None, 13E6),
                 ("Germany", None, "LK Pinneberg", 3.1E5),
                 ("Russia", None, None, 1.4E8),
                 ("Japan", "Kyoto", None, 2.6E6),
                 ("US", "New Jersey", None, 8.7E6),
                 ]
    for country, reg, subreg, ref_pop in reference:
        actual_population = c.population(country, reg, subreg)
        print(country)
        assert isinstance(actual_population, int)
        assert 0.8 * ref_pop < actual_population < 1.2 * ref_pop

    # Special cases
    # pass subregion as region for Germany
    pinneberg = c.population("Germany", "LK Pinneberg")
    assert isinstance(pinneberg, int)
    assert 3E5 < pinneberg < 4E5

    # pass both region AND subregion
    with pytest.raises(NotImplementedError):
        c.population("Germany", "Schleswig-Holstein", "LK Pinneberg")


def test_compare_plot():
    assert_oscovida_object(*c.make_compare_plot("Russia"))
    assert_oscovida_object(*c.make_compare_plot("Namibia", normalise=True))


def test_compare_plot_germany():
    assert_oscovida_object(*c.make_compare_plot_germany("Hamburg"))
    assert_oscovida_object(*c.make_compare_plot_germany("Hamburg", normalise=True))
    assert_oscovida_object(*c.make_compare_plot_germany("Hamburg", weeks=7))
    assert_oscovida_object(*c.make_compare_plot_germany("Bayern", normalise=True, weeks=8))
    assert_oscovida_object(*c.make_compare_plot_germany("Bayern", normalise=True, dates="2020-05-10:2020-06-15"))
    with pytest.raises(ValueError):
        c.make_compare_plot_germany("Bayern", normalise=True, weeks=8, dates="2020-05-10:2020-06-15")


def test_cut_dates():
    cases, deaths = mock_get_country_data_johns_hopkins()
    cut1 = oph.cut_dates(cases, "2020-02-01:2020-02-20")
    assert len(cut1) == 20
    cut2 = oph.cut_dates(cases, ":2020-02-20")
    assert len(cut2) == 30
    cut3 = oph.cut_dates(cases, "2020-02-20:")
    assert len(cut3) == 51
    with pytest.raises(ValueError):
        oph.cut_dates(cases, "2020-02-20")


def test_day0atleast():
    cases, deaths = mock_get_country_data_johns_hopkins()
    res = c.day0atleast(100, cases)
    assert type(res) == type(cases)
    assert len(res) == len(cases)
    assert len(res[res.index >= 0]) == len(cases)

    # should cut the first three values:
    res = c.day0atleast(1000, cases)
    assert type(res) == type(cases)
    assert len(res[res.index >= 0]) == len(cases) - 3

    # should return an empty series
    res = c.day0atleast(100000, cases)
    assert type(res) == type(cases)
    assert len(res) == 0


def test_uncertain_tail():
    cases, deaths = mock_get_country_data_johns_hopkins()
    fig, ax = plt.subplots()
    ax = c.plot_daily_change(ax, cases[:-30], 'C1')
    oph.uncertain_tail(ax, cases.diff().dropna(), days=30)
