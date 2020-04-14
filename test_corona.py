import pandas
from pandas import DatetimeIndex
import coronavirus as c


def mock_get_country(country="China"):
    cases_values = [548, 643, 920, 1406, 2075, 2877, 5509, 6087, 8141, 9802, 11891, 16630, 19716, 23707, 27440, 30587, 34110, 36814, 39829, 42354, 44386, 44759, 59895, 66358, 68413, 70513, 72434, 74211, 74619, 75077, 75550, 77001, 77022, 77241, 77754, 78166, 78600, 78928, 79356, 79932, 80136, 80261, 80386, 80537, 80690, 80770, 80823, 80860, 80887, 80921, 80932, 80945, 80977, 81003, 81033, 81058, 81102, 81156, 81250, 81305, 81435, 81498, 81591, 81661, 81782, 81897, 81999, 82122, 82198, 82279, 82361, 82432, 82511, 82543, 82602, 82665, 82718, 82809, 82883, 82941]
    cases_index = "DatetimeIndex(['2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25',  '2020-01-26', '2020-01-27', '2020-01-28', '2020-01-29',  '2020-01-30', '2020-01-31', '2020-02-01', '2020-02-02',  '2020-02-03', '2020-02-04', '2020-02-05', '2020-02-06',  '2020-02-07', '2020-02-08', '2020-02-09', '2020-02-10',  '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14',  '2020-02-15', '2020-02-16', '2020-02-17', '2020-02-18',  '2020-02-19', '2020-02-20', '2020-02-21', '2020-02-22',  '2020-02-23', '2020-02-24', '2020-02-25', '2020-02-26',  '2020-02-27', '2020-02-28', '2020-02-29', '2020-03-01',  '2020-03-02', '2020-03-03', '2020-03-04', '2020-03-05',  '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09',  '2020-03-10', '2020-03-11', '2020-03-12', '2020-03-13',  '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17',  '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21',  '2020-03-22', '2020-03-23', '2020-03-24', '2020-03-25',  '2020-03-26', '2020-03-27', '2020-03-28', '2020-03-29',  '2020-03-30', '2020-03-31', '2020-04-01', '2020-04-02',  '2020-04-03', '2020-04-04', '2020-04-05', '2020-04-06',  '2020-04-07', '2020-04-08', '2020-04-09', '2020-04-10'], dtype='datetime64[ns]', freq=None)"

    cases = pandas.Series(data=cases_values, index=eval(cases_index))
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

    isinstance(deaths, pandas.core.series.Series)
    isinstance(deaths, pandas.core.series.Series)


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
