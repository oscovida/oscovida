import datetime as dt
import os

import pandas as pd
import pytest

import oscovida.covid19dh as covid19dh

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def test_cache(tmp_path):
    cache_dir = os.path.join(tmp_path, "cache_dir")
    cache = covid19dh.Cache(cache_dir=cache_dir)

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
    os.mkdir(cache_dir)

    old = os.path.join(
        cache_dir,
        covid19dh.Cache._cache_id(1, dt.datetime(2020, 1, 1), False, False) + ".csv",
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
    covid19dh.Cache(cache_dir=cache_dir)

    #  Should have deleted the old cache file
    assert os.path.exists(old) == False

    #  And kept the new one and the non-csv
    assert os.path.exists(new)
    assert os.path.exists(keep)


def test_get(tmp_path):
    cache_dir = os.path.join(tmp_path, "cache_dir")
    tmp_cache = covid19dh.Cache(cache_dir)

    # Cache tests
    #  cache=None should disable caching
    covid19dh.get(None, level=1, cache=None)
    assert len(os.listdir(cache_dir)) == 0

    #  cache should be empty to start with
    assert not tmp_cache._cached(1, dt.datetime.now(), False, False)
    #  first run downloads cache
    covid19dh.get(None, level=1, cache=tmp_cache)
    #  data should now be cached
    assert tmp_cache._cached(1, dt.datetime.now(), False, False)

    # Vintage data
    vintage_data = covid19dh.get(
        None, level=1, end='2020-05-01', vintage=True, cache=tmp_cache
    )
    assert min(vintage_data.index) <= dt.datetime(2020, 5, 1)

    # Filtering tests
    all_data = covid19dh.get(None, level=1, cache=tmp_cache)
    assert len(all_data['iso_alpha_2'].unique()) >= 190

    single_country = covid19dh.get('DEU', level=1, cache=tmp_cache)
    assert len(single_country['iso_alpha_2'].unique()) == 1

    # Date input tests
    before_date_data = covid19dh.get(None, level=1, end='2020-05-01', cache=tmp_cache)
    assert max(before_date_data.index) <= dt.datetime(2020, 5, 1)

    after_date_data = covid19dh.get(
        'DEU', level=1, start=dt.datetime(2020, 5, 1), cache=tmp_cache
    )
    assert min(after_date_data.index) >= dt.datetime(2020, 5, 1)

    between_date_data = covid19dh.get(
        'DEU', level=1, start=dt.datetime(2020, 3, 1), end='2020-06-01', cache=tmp_cache
    )
    assert min(between_date_data.index) >= dt.datetime(2020, 3, 1)
    assert max(between_date_data.index) <= dt.datetime(2020, 6, 1)

    # Level tests
    data_level_1 = covid19dh.get(None, level=1, cache=tmp_cache)
    assert len(data_level_1['administrative_area_level_1'].unique()) == len(
        data_level_1['iso_alpha_3'].unique()
    )

    data_level_2 = covid19dh.get(None, level=2, cache=tmp_cache)
    assert 'Hamburg' in data_level_2['administrative_area_level_2'].unique()
    assert 'California' in data_level_2['administrative_area_level_2'].unique()

    data_level_3 = covid19dh.get(None, level=3, cache=tmp_cache)
    assert 'San Francisco' in data_level_3['administrative_area_level_3'].unique()
    assert 'LK Pinneberg' in data_level_3['administrative_area_level_3'].unique()


def test_get_raises(tmp_path):
    cache_dir = os.path.join(tmp_path, "cache_dir")
    tmp_cache = covid19dh.Cache(cache_dir)

    with pytest.raises(IndexError):
        covid19dh.get(None, level=0, cache=tmp_cache)

    with pytest.raises(IndexError):
        covid19dh.get(None, level=4, cache=tmp_cache)

    with pytest.raises(ValueError):
        covid19dh.get(None, level=1, end=dt.datetime(1990, 1, 1), cache=tmp_cache)

    with pytest.raises(NotImplementedError):
        covid19dh.get(None, level=1, end=['potato'], cache=tmp_cache)

    with pytest.raises(covid19dh.NoDataAvailable):
        covid19dh.get('potato', level=1, cache=tmp_cache)

    with pytest.raises(covid19dh.NoDataAvailable):
        #  By default gets data up to today, vintage not available for today
        covid19dh.get('DEU', level=1, cache=tmp_cache, vintage=True)


def test_cite(tmp_path):
    data = covid19dh.get(None, level=1, cache=None)

    citation = covid19dh.cite(data)

    assert isinstance(citation, list)
    assert all([isinstance(x, str) for x in covid19dh.cite(data)])
