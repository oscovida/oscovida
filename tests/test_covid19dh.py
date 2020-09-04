import datetime as dt
import os
from unittest import mock

import pandas as pd
import pytest

import oscovida.covid19dh as covid19dh

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def test_cache_methods(mock_cache_dir_fresh):
    cache = covid19dh.Cache()

    #  Cache should automatically create the cache dir if it is missing
    assert os.path.exists(cache.cache_dir)

    t = dt.datetime(2020, 1, 1)
    assert cache._cache_id(1, t, False, False) == "20200101_level_1"
    assert cache._cache_id(1, t, True, False) == "20200101_level_1_raw"
    assert cache._cache_id(1, t, False, True) == "20200101_level_1_vintage"

    assert cache._cached(1, t, False, False) == False

    test_data = pd.read_csv(os.path.join(TEST_DIR, "test_data", "20200901_level_1.csv"))
    #  Test writing data to cache
    cache.write(test_data, 1, t, False, False)
    assert cache._cached(1, t, False, False)

    #  Test reading data from cache
    test_read = cache.read(1, t, False, False)
    assert test_read.index.name == 'date'
    assert test_read.index.dtype == 'datetime64[ns]'


def test_cache_clean(tmp_path):
    cache_dir = os.path.join(tmp_path, "cache_dir")
    with mock.patch('oscovida.covid19dh.CACHE_DIR', cache_dir):
        os.mkdir(cache_dir)

        old = os.path.join(
            cache_dir,
            covid19dh.Cache._cache_id(1, dt.datetime(2020, 1, 1), False, False)
            + ".csv",
        )
        os.system(f'touch -d "2 weeks ago" {old}')

        new = os.path.join(
            cache_dir,
            covid19dh.Cache._cache_id(1, dt.datetime.now(), False, False) + ".csv",
        )
        os.system(f'touch -d "2 weeks ago" {new}')

        keep = os.path.join(cache_dir, "keep.doc")
        os.system(f'touch -d "2 weeks ago" {keep}')

        #  Initialising `Cache` runs the old file cleaning at the start
        covid19dh.Cache()

        #  Should have deleted the old cache file
        assert os.path.exists(old) == False

        #  And kept the new one and the non-csv
        assert os.path.exists(new)
        assert os.path.exists(keep)


def test_get_cache(mock_cache_dir_fresh):
    cache = covid19dh.Cache()
    # Cache tests
    #  cache=None should disable caching
    covid19dh.get(None, level=1, cache=None)
    assert len(os.listdir(cache.cache_dir)) == 0
    #  cache should be empty to start with
    assert not cache._cached(1, dt.datetime.now(), False, False)
    #  first run downloads cache
    covid19dh.get(None, level=1)
    #  data should now be cached
    assert cache._cached(1, dt.datetime.now(), False, False)


def test_get_vintage(mock_cache_dir):
    # Vintage data
    vintage_data = covid19dh.get(None, level=1, end='2020-05-01', vintage=True)
    assert min(vintage_data.index) <= dt.datetime(2020, 5, 1)


def test_get_all(mock_cache_dir):
    # Filtering tests
    all_data = covid19dh.get(None, level=1)
    assert len(all_data['iso_alpha_2'].unique()) >= 190


def test_get_country(mock_cache_dir):
    single_country = covid19dh.get('DEU', level=1)
    assert len(single_country['iso_alpha_2'].unique()) == 1


def test_get_before_date(mock_cache_dir):
    # Date input tests
    before_date_data = covid19dh.get(None, level=1, end='2020-05-01')
    assert max(before_date_data.index) <= dt.datetime(2020, 5, 1)


def test_get_after_date(mock_cache_dir):
    after_date_data = covid19dh.get('DEU', level=1, start=dt.datetime(2020, 5, 1))
    assert min(after_date_data.index) >= dt.datetime(2020, 5, 1)


def test_get_between_date(mock_cache_dir):
    between_date_data = covid19dh.get(
        'DEU',
        level=1,
        start=dt.datetime(2020, 3, 1),
        end='2020-06-01',
    )
    assert min(between_date_data.index) >= dt.datetime(2020, 3, 1)
    assert max(between_date_data.index) <= dt.datetime(2020, 6, 1)


def test_get_level_1(mock_cache_dir):
    # Level tests
    data_level_1 = covid19dh.get(None, level=1)
    assert len(data_level_1['administrative_area_level_1'].unique()) == len(
        data_level_1['iso_alpha_3'].unique()
    )


def test_get_level_2(mock_cache_dir):
    data_level_2 = covid19dh.get(None, level=2)
    assert 'Hamburg' in data_level_2['administrative_area_level_2'].unique()
    assert 'California' in data_level_2['administrative_area_level_2'].unique()


def test_get_level_3(mock_cache_dir):
    data_level_3 = covid19dh.get(None, level=3)
    assert 'San Francisco' in data_level_3['administrative_area_level_3'].unique()
    assert 'LK Pinneberg' in data_level_3['administrative_area_level_3'].unique()


def test_get_raises_bad_level(mock_cache_dir):
    with pytest.raises(IndexError):
        covid19dh.get(None, level=0)

    with pytest.raises(IndexError):
        covid19dh.get(None, level=4)


def test_get_raises_bad_date(mock_cache_dir):
    with pytest.raises(ValueError):
        covid19dh.get(None, level=1, end=dt.datetime(1990, 1, 1))

    with pytest.raises(NotImplementedError):
        covid19dh.get(None, level=1, end=['potato'])


def test_get_raises_bad_country(mock_cache_dir):
    with pytest.raises(covid19dh.NoDataAvailable):
        covid19dh.get('potato', level=1)


def test_get_raises_bad_vintage(mock_cache_dir):
    with pytest.raises(covid19dh.NoDataAvailable):
        #  By default gets data up to today, vintage not available for today
        covid19dh.get('DEU', level=1, vintage=True)


def test_cite(tmp_path):
    data = covid19dh.get(None, level=1, cache=None)

    citation = covid19dh.cite(data)

    assert isinstance(citation, list)
    assert all([isinstance(x, str) for x in covid19dh.cite(data)])
