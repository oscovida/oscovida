import datetime as dt
import os

import pandas as pd
import pytest

import oscovida.covid19dh as covid19dh

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def fresh_cache(tmp_path):
    cache_dir = os.path.join(tmp_path, "cache_dir")
    return covid19dh.Cache(cache_dir=cache_dir)


@pytest.fixture(scope="module")
def reused_cache(tmp_path_factory):
    cache_dir = tmp_path_factory.mktemp("cache_dir")
    return covid19dh.Cache(cache_dir=cache_dir)


def test_cache(fresh_cache):
    #  Cache should automatically create the cache dir if it is missing
    assert os.path.exists(fresh_cache.cache_dir)

    t = dt.datetime(2020, 1, 1)
    assert fresh_cache._cache_id(1, t, False, False) == "20200101_level_1"
    assert fresh_cache._cache_id(1, t, True, False) == "20200101_level_1_raw"
    assert fresh_cache._cache_id(1, t, False, True) == "20200101_level_1_vintage"

    assert fresh_cache._cached(1, t, False, False) == False

    test_data = pd.read_csv(os.path.join(TEST_DIR, "test_data", "20200901_level_1.csv"))
    #  Test writing data to cache
    fresh_cache.write(test_data, 1, t, False, False)
    assert fresh_cache._cached(1, t, False, False)

    #  Test reading data from cache
    test_read = fresh_cache.read(1, t, False, False)
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


def test_get_cache(reused_cache):
    # Cache tests
    #  cache=None should disable caching
    covid19dh.get(None, level=1, cache=None)
    assert len(os.listdir(reused_cache.cache_dir)) == 0

    #  cache should be empty to start with
    assert not reused_cache._cached(1, dt.datetime.now(), False, False)
    #  first run downloads cache
    covid19dh.get(None, level=1, cache=reused_cache)
    #  data should now be cached
    assert reused_cache._cached(1, dt.datetime.now(), False, False)


def test_get_vintage(reused_cache):
    # Vintage data
    vintage_data = covid19dh.get(
        None, level=1, end='2020-05-01', vintage=True, cache=reused_cache
    )
    assert min(vintage_data.index) <= dt.datetime(2020, 5, 1)


def test_get_all(reused_cache):
    # Filtering tests
    all_data = covid19dh.get(None, level=1, cache=reused_cache)
    assert len(all_data['iso_alpha_2'].unique()) >= 190


def test_get_country(reused_cache):
    single_country = covid19dh.get('DEU', level=1, cache=reused_cache)
    assert len(single_country['iso_alpha_2'].unique()) == 1


def test_get_before_date(reused_cache):
    # Date input tests
    before_date_data = covid19dh.get(
        None, level=1, end='2020-05-01', cache=reused_cache
    )
    assert max(before_date_data.index) <= dt.datetime(2020, 5, 1)


def test_get_after_date(reused_cache):
    after_date_data = covid19dh.get(
        'DEU', level=1, start=dt.datetime(2020, 5, 1), cache=reused_cache
    )
    assert min(after_date_data.index) >= dt.datetime(2020, 5, 1)


def test_get_between_date(reused_cache):
    between_date_data = covid19dh.get(
        'DEU',
        level=1,
        start=dt.datetime(2020, 3, 1),
        end='2020-06-01',
        cache=reused_cache,
    )
    assert min(between_date_data.index) >= dt.datetime(2020, 3, 1)
    assert max(between_date_data.index) <= dt.datetime(2020, 6, 1)


def test_get_level_1(reused_cache):
    # Level tests
    data_level_1 = covid19dh.get(None, level=1, cache=reused_cache)
    assert len(data_level_1['administrative_area_level_1'].unique()) == len(
        data_level_1['iso_alpha_3'].unique()
    )


def test_get_level_2(reused_cache):
    data_level_2 = covid19dh.get(None, level=2, cache=reused_cache)
    assert 'Hamburg' in data_level_2['administrative_area_level_2'].unique()
    assert 'California' in data_level_2['administrative_area_level_2'].unique()


def test_get_level_3(reused_cache):
    data_level_3 = covid19dh.get(None, level=3, cache=reused_cache)
    assert 'San Francisco' in data_level_3['administrative_area_level_3'].unique()
    assert 'LK Pinneberg' in data_level_3['administrative_area_level_3'].unique()


def test_get_raises_bad_level(reused_cache):
    with pytest.raises(IndexError):
        covid19dh.get(None, level=0, cache=reused_cache)

    with pytest.raises(IndexError):
        covid19dh.get(None, level=4, cache=reused_cache)


def test_get_raises_bad_date(reused_cache):
    with pytest.raises(ValueError):
        covid19dh.get(None, level=1, end=dt.datetime(1990, 1, 1), cache=reused_cache)

    with pytest.raises(NotImplementedError):
        covid19dh.get(None, level=1, end=['potato'], cache=reused_cache)


def test_get_raises_bad_country(reused_cache):
    with pytest.raises(covid19dh.NoDataAvailable):
        covid19dh.get('potato', level=1, cache=reused_cache)


def test_get_raises_bad_vintage(reused_cache):
    with pytest.raises(covid19dh.NoDataAvailable):
        #  By default gets data up to today, vintage not available for today
        covid19dh.get('DEU', level=1, cache=reused_cache, vintage=True)


def test_cite(tmp_path):
    data = covid19dh.get(None, level=1, cache=None)

    citation = covid19dh.cite(data)

    assert isinstance(citation, list)
    assert all([isinstance(x, str) for x in covid19dh.cite(data)])
