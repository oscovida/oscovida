import datetime
import math
import os
import re
import zipfile
from functools import lru_cache
from io import BytesIO, StringIO
from typing import List, Optional, Tuple, Union

import appdirs
import pandas as pd
import requests

CACHE_DIR = appdirs.user_cache_dir('covid19dh')


class NoDataAvailable(Exception):
    pass


class Cache:
    def __init__(self) -> None:
        """Class used to manage covid19dh data caching

        Note: the cache automatically cleans itself, data older than one day
        will be deleted unless it is explicitly vintage data

        Parameters
        ----------
        cache_dir : [type], optional Directory to store cache, by default
            appdirs.user_cache_dir('covid19dh')
        """
        self.cache_dir = CACHE_DIR

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
                and 'vintage' not in f
            ):
                os.remove(cached_data_file)

    @staticmethod
    def _cache_id(level: int, dt: datetime.datetime, raw: bool, vintage: bool) -> str:
        cache_id = dt.strftime("%Y%m%d")
        cache_id += f"_level_{level}"

        if raw:
            cache_id += "_raw"
        if vintage:
            cache_id += "_vintage"

        return cache_id

    def _cache_path(
        self, level: int, dt: datetime.datetime, raw: bool, vintage: bool
    ) -> str:
        return os.path.join(
            self.cache_dir, self._cache_id(level, dt, raw, vintage) + '.csv'
        )

    def _cached(
        self, level: int, dt: datetime.datetime, raw: bool, vintage: bool
    ) -> bool:
        return os.path.isfile(self._cache_path(level, dt, raw, vintage))

    @lru_cache
    def read(
        self, level: int, dt: datetime.datetime, raw: bool, vintage: bool
    ) -> pd.DataFrame:
        """Read data from the cache for some given parameters

        Parameters
        ----------
        level : int
            Administrative level
        dt : datetime.datetime
            A dataset containing **all** data up to this date will be fetched
        raw : bool
        vintage : bool

        Returns
        -------
        pd.DataFrame
        """
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
    rawprefix = "raw" if raw else ""
    dataname = f"{rawprefix}data-{level}"

    if vintage:
        dt_str = dt.strftime("%Y-%m-%d")
        two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
        first_vintage_data = datetime.datetime(2020, 4, 14)
        if (dt >= two_days_ago) or (dt < first_vintage_data):
            raise NoDataAvailable(f"vintage data not available for {dt_str}")

        filename = f"{ dt_str }.zip"
    else:
        filename = f"{dataname}.zip"

    return f"https://storage.covid19datahub.io/{filename}", f"{dataname}.csv"


def _parse_date(dt: Union[str, datetime.datetime, datetime.date]) -> datetime.datetime:
    if isinstance(dt, datetime.date):
        return datetime.datetime(dt.year, dt.month, dt.day)

    if isinstance(dt, str):
        return datetime.datetime.strptime(dt, "%Y-%m-%d")

    raise NotImplementedError(f"{type(dt)} is not `str` or `datetime.date`")


def _download(
    level: int, dt: datetime.datetime, raw: bool, vintage: bool
) -> pd.DataFrame:
    url, filename = _get_url(level, dt, raw, vintage)

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    with zipfile.ZipFile(BytesIO(response.content)) as zz:
        with zz.open(filename) as fd:
            df: pd.DataFrame = pd.read_csv(fd, low_memory=False)  # type: ignore

    #  Convert date column from string to datetime object
    df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    if 'iso_numeric' in df.columns:  # Some vintage data does not have this column
        df['iso_numeric'] = df['iso_numeric'].apply(lambda x: float(x))

    df = df.set_index('date')  # type: ignore

    return df


def get(
    country: Optional[str] = None,
    level: int = 1,
    start: datetime.date = datetime.date(2019, 1, 1),
    end: Optional[datetime.datetime] = None,
    cache: Optional[Cache] = Cache(),
    raw: bool = False,
    vintage: bool = False,
) -> pd.DataFrame:
    """Fetches data from [covid19datahub.io](covid19datahub.io) for the specified
    level, and filters by country if one is given.

    Parameters
    ----------
    country : Optional[str], optional
        Country to filter by, returns full table if `None`, by default None
    level : int, optional
        Administrative level of the table, 1 is at the country level, 2 sub-
        country (typically states/regions),and 2 is sub-state level (typically
        individual cities or districts). Only accepts values of 1, 2, or 3, by
        default 1
    start : Optional[datetime.date], optional
        Start of data, by default `datetime.date(2019, 1, 1)`
    end : Optional[datetime.datetime], optional
        End of data, if `None` it is set to the current time, by default `None`
    cache : Optional[Cache], optional
        Cache option to use, by default `oscovida.covid19dh.Cache()`
    raw : bool, optional
        Warning: Experimental. If `True`, downloads the saw data tables, by
        default `False`
    vintage : bool, optional
        Warning: Experimental. If `True`, downloads vintage data, by default `False`

    Returns
    -------
    pd.DataFrame
        DataFrame containing the covid data for a specified level, filtered by
        the specified country. The index is set to `date`, and each row contains
        the cumulative numbers for a region up to the specified date.
    """
    end = datetime.datetime.now() if end is None else end
    end = _parse_date(end)
    start = _parse_date(start)

    if level not in {1, 2, 3}:
        raise IndexError("invalid level, level should be 1, 2, or 3.")

    if start > end:
        raise ValueError(f"start date {start} is later than {end}")

    if cache and cache._cached(level, end, raw, vintage):
        df = cache.read(level, end, raw, vintage)
    else:
        df = _download(level, end, raw, vintage)
        if cache:
            cache.write(df, level, end, raw, vintage)

    if country is not None:
        #  We get all of the columns that give a region its name, check if the
        #  given country argument matches any of the values in those columns
        #  (with the country as given, or all upper case, or all lower case),
        #  then create a mask by finding any columns that match the country
        cols = [
            'iso_alpha_2',
            'iso_alpha_3',
            'iso_numeric',
            'administrative_area_level_1',
        ]
        # Some columns are missing for vintage data so we check they exist here
        cols = list(filter(lambda x: x in df.columns, cols))

        df_mask = df[cols].isin([country, country.upper(), country.lower()]).any(axis=1)

        df = df[df_mask]

        if len(df) == 0:
            raise NoDataAvailable(
                f"No data found for '{country}' in {cols}. Is '{country}' "
                f"a valid country name or ISO country code?"
            )

    if start is not None:
        df = df[df.index >= start]  # type: ignore

    if end is not None:
        df = df[df.index <= end]  # type: ignore

    df = df.sort_values(by=["id", "date"])  # type: ignore

    return df  # type: ignore


def cite(x: pd.DataFrame, raw: bool = False) -> List[str]:
    """Get a list of sources for a given covid19dh DataFrame

    Parameters
    ----------
    x : pd.DataFrame
        Input covid19dh DataFrame
    raw : bool, optional
        Set to `True` if the data is raw data, by default `False`

    Returns
    -------
    List[str]
        List of sources, each element is a string
    """
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
        return unique_sources.count().reset_index().tolist()

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
        "Guidotti, E., Ardia, D., (2020), 'COVID-19 Data Hub', "
        "Working paper, doi: 10.13140/RG.2.2.11649.81763."
    )

    return citations
