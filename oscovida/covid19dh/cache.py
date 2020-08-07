import appdirs
from datetime import date, datetime
import pandas as pd
import os

CACHE_DIR = appdirs.user_cache_dir('covid19dh')

if not os.path.isdir(CACHE_DIR):
    os.mkdir(CACHE_DIR)

for f in os.listdir(CACHE_DIR):
    cached_data_file = os.path.join(CACHE_DIR, f)
    mtime = os.path.getmtime(cached_data_file)
    #  If a file is over 5 days old, remove it after some checks
    if (mtime / (60 * 60 * 24)) > 5:
        if os.path.splitext(cached_data_file)[1] == '.csv':
            os.remove(cached_data_file)


def construct_cache_id(level: int, dt: datetime, raw: bool, vintage: bool):
    cache_id = dt.strftime("%Y%m%d")
    cache_id += f"_level_{level}"

    if raw:
        cache_id += "_raw"

    return cache_id


def read_cache(level: int, dt: datetime, raw: bool, vintage: bool) -> pd.DataFrame:
    cache_id = construct_cache_id(level=level, dt=dt, raw=raw, vintage=vintage)

    cached_file_path = os.path.join(CACHE_DIR, cache_id + '.csv')
    if os.path.isfile(cached_file_path):
        return pd.read_csv(cached_file_path, index_col='date', parse_dates=['date'])
    else:
        return None


def write_cache(x: pd.DataFrame, level: int, dt: datetime, raw: bool, vintage: bool):
    cache_id = construct_cache_id(level=level, dt=dt, raw=raw, vintage=vintage)
    cached_file_path = os.path.join(CACHE_DIR, cache_id + '.csv')

    x.to_csv(cached_file_path)


__all__ = ["read_cache", "write_cache"]
