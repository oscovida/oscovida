import datetime
from io import StringIO, BytesIO
import math
import sys
import warnings
import zipfile
from typing import Optional, Union

import pandas as pd
import requests

from .cite import cite
from .cache import *


def get_url(level: int, dt: datetime.datetime, raw: bool, vintage: bool):
    # dataname
    rawprefix = "raw" if raw else ""
    dataname = f"{rawprefix}data-{level}"
    # vintage
    if vintage:
        # too new
        if dt >= datetime.datetime.now() - datetime.timedelta(days=2):
            warnings.warn("vintage data not available yet")
            return None, None
        dt_str = dt.strftime("%Y-%m-%d")
        filename = f"{ dt_str }.zip"
    # current data
    else:
        filename = f"{dataname}.zip"
    # url, filename
    return f"https://storage.covid19datahub.io/{filename}", f"{dataname}.csv"


def parseDate(dt: datetime.datetime):
    if isinstance(dt, datetime.date):
        return datetime.datetime(dt.year, dt.month, dt.day)
    if isinstance(dt, str):
        try:
            return datetime.datetime.strptime(dt, "%Y-%m-%d")
        except:
            print("Invalid time format.", file=sys.stderr)
            raise
    return dt


def covid19(
    country: Union[Optional[str], Optional[list]] = None,
    level: int = 1,
    start=datetime.date(2019, 1, 1),
    end: Optional[datetime.datetime] = None,  # default today
    cache: bool = True,
    verbose: bool = False,
    raw: bool = False,
    vintage: bool = False,
):
    """Main function for module. Fetches data from hub.

    Args:
        country (str, optional): ISO country code, default all countries
        level (int, optional): level of data, default 1
            * country-level (1)
            * state-level (2)
            * city-level (3)
        start (datetime | date | str, optional): start date of data (as str in format [%Y-%m-%d]),
                                                 default 2019-01-01
        end (datetime | date | str, optional): end date of data (as str in format [%Y-%m-%d]),
                                               default today (sysdate)
        cache (bool, optional): use cached data if available, default yes
        verbose (bool, optional): prints sources, default true
        raw (bool, optional): download not cleansed data, default using cleansed
        vintage (bool, optional): use hub data (True) or original source, not available in Python covid19dh (only hub)
    """
    # parse arguments
    if country is not None:
        country = [country] if isinstance(country, str) else country
        country = [c.upper() if isinstance(c, str) else c for c in country]

    end = datetime.datetime.now() if end is None else end

    try:
        end = parseDate(end)
        start = parseDate(start)
    except:
        return None

    if level not in {1, 2, 3}:
        warnings.warn(
            "valid options for 'level' are:\n\t1: country-level data\n\t2: state-level data\n\t3: city-level data"
        )
        return None

    if start > end:
        warnings.warn("start is later than end")
        return None

    if raw:
        warnings.warn(
            "raw data not available for covid19dh, fetching precleaned vintage",
            category=ResourceWarning,
        )

    if not vintage:
        warnings.warn(
            "only vintage data available for covid19dh, fetching vintage",
            category=ResourceWarning,
        )

    # cache
    df = read_cache(level, end, raw, vintage)

    if cache is False or df is None:
        # get url from level
        try:
            url, filename = get_url(level=level, dt=end, raw=raw, vintage=vintage)
            if url is None:
                return None
        except KeyError:
            warnings.warn("invalid level")
            return None

        # download
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        except:
            if vintage:
                warnings.warn("vintage data not available yet")
                return None
            else:
                warnings.warn("error to fetch data")
                return None

        # parse
        with zipfile.ZipFile(BytesIO(response.content)) as zz:
            with zz.open(filename) as fd:
                df: pd.DataFrame = pd.read_csv(fd, low_memory=False)

        # cast columns
        df['date'] = df['date'].apply(
            lambda x: datetime.datetime.strptime(x, "%Y-%m-%d")
        )
        df['iso_numeric'] = df['iso_numeric'].apply(lambda x: float(x))

        df = df.set_index('date')

        write_cache(df, level, end, raw, vintage)

    # filter
    if country is not None:
        # elementwise comparison works, but throws warning that it will be
        # working better in the future no idea why, but I found solution to mute
        # it as follows
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            df = df[
                (df['iso_alpha_3'].isin(country))
                | (df['iso_alpha_2'].isin(country))
                | (df['iso_numeric'].isin(country))
                | (
                    df['administrative_area_level_1']
                    .map(lambda s: s.upper())
                    .isin(country)
                )
            ]

    if start is not None:
        df = df[df.index >= start]

    if end is not None:
        df = df[df.index <= end]

    # detect empty
    if df.empty:
        warnings.warn("no data for given settings", category=ResourceWarning)
        return None

    # sort
    df = df.sort_values(by=["id", "date"])

    if verbose:
        sources = cite(df)
        print("\033[1mData References:\033[0m\n", end="")
        for source in sources:
            print("\t" + source, end="\n\n")
        print("\033[33mTo hide the data sources use 'verbose = False'.\033[0m")

    return df


__all__ = ["covid19"]
