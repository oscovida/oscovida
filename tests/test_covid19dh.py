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

    assert cache.cached(1, t, False, False) == False

    test_data = pd.read_csv(os.path.join(TEST_DIR, "test_data", "20200901_level_1.csv"))
    #  Test writing data to cache
    cache.write(test_data, 1, t, False, False)
    assert cache.cached(1, t, False, False)

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
