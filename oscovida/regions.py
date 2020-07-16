from covid19dh import covid19
import pycountry
from functools import lru_cache
from typing import NamedTuple, Optional
import pandas.core.frame.DataFrame


@lru_cache(maxsize=32)
def fetch_covid19_data(
    country: str = None, level: int = 1, verbose: bool = False
) -> pandas.core.frame.DataFrame:
    """Wraps the `covid19dh.covid19` function in n `functools.lru_cache`.

    `covid19dh.covid19` caches the downloaded data files to disk so that it does
    not have to download them each time, however it does not cache them
    in-memory, and loading the larger files can be a bit slow.
    """
    return covid19(country, level=level, verbose=verbose)


class RegionInfo(NamedTuple):
    """Contains information that specifies a region.

    Parameters
    ----------
    country: str
        Country name string (e.g. "United States")
    admin_1: str
        Country alpha_3 string, administrative area of top level (e.g. "USA")
    admin_2: str = ""
        Second-level administrative area, usually states, regions or cantons (e.g. "California")
    admin_3: str = ""
        Third-level administrative area, usually cities or municipalities (e.g. "San Francisco")
    level: int = -1
        Level of administrative areas specified
    """

    country: Optional[str] = None
    admin_1: Optional[str] = None
    admin_2: Optional[str] = None
    admin_3: Optional[str] = None
    level: int = -1


def region_info(
    admin_1: str, admin_2: Optional[str] = None, admin_3: Optional[str] = None
) -> RegionInfo:
    """Returns a RegionInfo named tuple

    Parameters
    ----------
    admin_1: str
        Country name string (e.g. "United States") or alpha_3 string,
        administrative area of top level (e.g. "USA")
    admin_2: str = ""
        Second-level administrative area, usually states, regions or cantons (e.g. "California")
    admin_3: str = ""
        Third-level administrative area, usually cities or municipalities (e.g. "San Francisco")

    Returns
    -------
    RegionInfo
        RegionInfo: see `oscovida.data.RegionInfo` docs

    Raises
    ------
    LookupError
        Raised if the `admin_1` string is too ambiguous. For example,
        `region_info("UK")` will not work as the country code is GB or GBR, and
        UK matches too many possible places.

    Examples
    --------
    >>> region_info("GB")
    RegionInfo(country='United Kingdom', admin_1='GBR', admin_2=None, admin_3=None, level=1)

    >>> region_info("United Kingdom", "England")
    RegionInfo(country='United Kingdom', admin_1='GBR', admin_2='England', admin_3=None, level=2)

    >>> region_info("United Kingdom", "England", "Westminster")
    RegionInfo(country='United Kingdom', admin_1='GBR', admin_2='England', admin_3='Westminster', level=3)
    """
    if admin_1.strip().lower() == "world":
        return RegionInfo("world", "world", level=0)

    try:
        pyc_admin_1: pycountry.db.Country = pycountry.countries.lookup(admin_1)
    except LookupError:
        pyc_admin_1_matches: list = pycountry.countries.search_fuzzy(admin_1)  # type: ignore
        if len(pyc_admin_1_matches) > 1:
            raise LookupError(
                f"{admin_1} too ambiguous, {len(pyc_admin_1_matches)} possible options,"
                f"please specify one of:"
                f"\n{[c.name for c in pyc_admin_1_matches]}"
            )
        pyc_admin_1: pycountry.db.Country = pyc_admin_1_matches[0]  # type: ignore

    level = 1

    if admin_2:
        level = 2

    if admin_3:
        level = 3

    return RegionInfo(
        country=pyc_admin_1.name,
        admin_1=pyc_admin_1.alpha_3,
        admin_2=admin_2,
        admin_3=admin_3,
        level=level,
    )
