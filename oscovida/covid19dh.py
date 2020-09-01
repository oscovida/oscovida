import datetime
import math
import os
import re
import warnings
import zipfile
from io import BytesIO, StringIO
from typing import Optional, Union, Tuple, List

import appdirs
import pandas as pd
import requests

from functools import lru_cache


class Cache:
    def __init__(self, cache_dir=appdirs.user_cache_dir('covid19dh')) -> None:
        self.cache_dir = cache_dir

        if not os.path.isdir(self.cache_dir):
            os.mkdir(self.cache_dir)

        files_in_cache = os.listdir(self.cache_dir)

        for f in files_in_cache:
            cached_data_file = os.path.join(self.cache_dir, f)
            mtime = os.path.getmtime(cached_data_file)

            now = datetime.datetime.now()

            file_age = now - datetime.datetime.fromtimestamp(mtime)
            try:
                name_age = now - datetime.datetime.strptime(f[:8], "%Y%m%d")
            except ValueError:
                #  Happens if the filename is not formatted like a date
                continue

            #  If a csv file in the cache is over 1 day old then remove it
            if (
                file_age.days > 1
                and name_age.days > 1
                and os.path.splitext(cached_data_file)[1] == '.csv'
            ):
                os.remove(cached_data_file)

    @staticmethod
    def _cache_id(level: int, dt: datetime.datetime, raw: bool, vintage: bool) -> str:
        cache_id = dt.strftime("%Y%m%d")
        cache_id += f"_level_{level}"

        if raw:
            cache_id += "_raw"

        return cache_id

    def _cache_path(
        self, level: int, dt: datetime.datetime, raw: bool, vintage: bool
    ) -> str:
        return os.path.join(
            self.cache_dir, self._cache_id(level, dt, raw, vintage) + '.csv'
        )

    def cached(
        self, level: int, dt: datetime.datetime, raw: bool, vintage: bool
    ) -> bool:
        return os.path.isfile(self._cache_path(level, dt, raw, vintage))

    @lru_cache
    def read(
        self, level: int, dt: datetime.datetime, raw: bool, vintage: bool
    ) -> pd.DataFrame:
        return pd.read_csv(
            self._cache_path(level, dt, raw, vintage),
            index_col='date',
            parse_dates=['date'],
        )  # type: ignore

    def write(
        self,
        x: pd.DataFrame,
        level: int,
        dt: datetime.datetime,
        raw: bool,
        vintage: bool,
    ) -> None:
        x.to_csv(self._cache_path(level, dt, raw, vintage))


def _get_url(
    level: int, dt: datetime.datetime, raw: bool, vintage: bool
) -> Tuple[str, str]:
    # dataname
    rawprefix = "raw" if raw else ""
    dataname = f"{rawprefix}data-{level}"

    # vintage
    if vintage:
        # too new
        if dt >= datetime.datetime.now() - datetime.timedelta(days=2):
            raise Exception("vintage data not available yet")

        dt_str = dt.strftime("%Y-%m-%d")
        filename = f"{ dt_str }.zip"
    # current data
    else:
        filename = f"{dataname}.zip"
    # url, filename
    return f"https://storage.covid19datahub.io/{filename}", f"{dataname}.csv"


def _parse_date(dt: Union[str, datetime.datetime, datetime.date]) -> datetime.datetime:
    if isinstance(dt, datetime.date):
        return datetime.datetime(dt.year, dt.month, dt.day)

    if isinstance(dt, str):
        return datetime.datetime.strptime(dt, "%Y-%m-%d")

    return dt


def _download(
    level: int, dt: datetime.datetime, raw: bool, vintage: bool
) -> pd.DataFrame:
    url, filename = _get_url(level, dt, raw, vintage)

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    with zipfile.ZipFile(BytesIO(response.content)) as zz:
        with zz.open(filename) as fd:
            df: pd.DataFrame = pd.read_csv(fd, low_memory=False)  # type: ignore

    df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    df['iso_numeric'] = df['iso_numeric'].apply(lambda x: float(x))

    df = df.set_index('date')  # type: ignore

    return df


def get(
    country: Union[Optional[str], Optional[list]] = None,
    level: int = 1,
    start: datetime.date = datetime.date(2019, 1, 1),
    end: Optional[datetime.datetime] = None,
    cache: Optional[Cache] = Cache(),
    raw: bool = False,
    vintage: bool = False,
) -> pd.DataFrame:
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
    if country is not None:
        country = [country] if isinstance(country, str) else country
        country = [c.upper() if isinstance(c, str) else c for c in country]

    end = datetime.datetime.now() if end is None else end
    end = _parse_date(end)
    start = _parse_date(start)

    if level not in {1, 2, 3}:
        raise Exception("Invalid level, level should be 1, 2, or 3.")

    if start > end:
        raise Exception("Start is later than end")

    if cache and cache.cached(level, end, raw, vintage):
        df = cache.read(level, end, raw, vintage)
    else:
        df = _download(level, end, raw, vintage)
        if cache:
            cache.write(df, level, end, raw, vintage)

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
        df = df[df.index >= start]  # type: ignore

    if end is not None:
        df = df[df.index <= end]  # type: ignore

    df = df.sort_values(by=["id", "date"])  # type: ignore

    return df


def cite(x: pd.DataFrame, raw: bool = False) -> List[str]:
    # get sources
    url = 'https://storage.covid19datahub.io/src.csv'
    response = requests.get(url)
    sources: pd.DataFrame = pd.read_csv(StringIO(response.text))  # type: ignore

    # transform data
    isos = set(x["iso_alpha_3"].unique())
    params = set(x.columns)
    # add universal
    isos.add(math.nan)

    # collect used references
    sources = sources[
        sources["iso_alpha_3"].isin(isos) & sources["data_type"].isin(params)
    ]
    unique_sources = sources.fillna("").groupby(
        ["title", "author", "year", "institution", "url", "textVersion", "bibtype"]
    )

    if raw:
        return unique_sources.count().reset_index()

    # turn references into citations
    citations = []
    for n, g in unique_sources:
        (title, author, year, institution, url, text_version, bibtype) = n

        if text_version:
            citation = text_version
            citations.append(citation)
            continue

        # pre,post
        pre = author
        post = ""
        if author and title:
            post = title
        elif title:
            pre = title

        # post
        if institution:
            post = ", ".join(filter(None, [post, institution]))

        if url:
            url = re.sub(r"(http://|https://|www\\.)([^/]+)(.*)", r"\1\2/", url)

            post = ", ".join(filter(None, [post, url]))
        else:
            post += "."

        citation = f"{pre} ({year}), {post}"

        citations.append(citation)

    citations.append(
        "Guidotti, E., Ardia, D., (2020), \"COVID-19 Data Hub\", Working paper, doi: 10.13140/RG.2.2.11649.81763."
    )

    return citations
