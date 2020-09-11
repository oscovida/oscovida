import datetime
from collections import namedtuple
from typing import List, Optional

import pandas as pd
import pycountry
from pandas import DataFrame

from . import covid19dh

# TODO: Use world bank data (world-bank-data pypi)


class Region:
    def __init__(
        self,
        admin_1: Optional[str],
        admin_2: Optional[str] = None,
        admin_3: Optional[str] = None,
        level: Optional[int] = None,
        start: datetime.date = datetime.date(2019, 1, 1),
        end: Optional[datetime.datetime] = None,
        raw: bool = False,
        vintage: bool = False,
    ) -> None:
        """
        Parameters
        ----------
        admin_1: str
            Country name string (e.g. 'United States') or alpha_3 string,
            administrative area of top level
            (e.g. 'USA')
        admin_2: Optional[str] = None
            Second-level administrative area, usually states, regions or cantons
            (e.g. 'California')
        admin_3: Optional[str] = None
            Third-level administrative area, usually cities or municipalities
            (e.g. 'San Francisco')
        level: Optional[int] = None
            Level is automatically detected from the number of administrative
            levels passed. Optionally you can specify the level to return a
            dataframe containing the information for all administrative regions
            up to and including the specified level
            (e.g. `Region('USA', level=2)` returns all USA states)

        Attributes
        -------
        data: DataFrame
            Pandas dataframe containing the data for the specified region
        cite: list[str]
            Returns a list of sources for the data
        country: str
            Country name string (e.g. 'United States')
        admin_1: str
            Country alpha_3 string, administrative area of top level (e.g. 'USA')
        admin_2: Optional[str]
            Second-level administrative area, usually states, regions or cantons
        admin_3: Optional[str]
            Third-level administrative area, usually cities or municipalities
        level: int
            Level of administrative areas specified

        Raises
        ------
        LookupError
            Raised if an administrative level string is too ambiguous. For example,
            `Region('UK')` will not work as the country code is GB or GBR, and UK
            matches too many possible places.

        Examples
        --------
        You can create a `Region` object by calling it with specific levels, which
        will return a filtered DataTable:

        >>> Region('USA')
        Region(country='United States', admin_1='USA', admin_2=None, admin_3=None, level=1)

        >>> Region('USA', 'California')
        Region(country='United States', admin_1='USA', admin_2='California', admin_3=None, level=2)

        >>> Region('USA', 'California', 'San Francisco')
        Region(country='United States', admin_1='USA', admin_2='California', admin_3='San Francisco', level=3)

        Alternatively you can specify a `level` directly, which will not filter
        the administrative regions. For example, getting all level 2 regions for
        the United Kingdom would be:

        >>> Region('USA', level=2)
        Region(country='United States', admin_1='USA', admin_2='*', admin_3=None, level=2)

        Or all level 3:

        >>> Region('USA', level=3)
        Region(country='United States', admin_1='USA', admin_2='*', admin_3='*', level=3)

        Or an administrative level 2, requesting all level 3 regions in it:
        >>> Region('USA', 'California', level=3)
        Region(country='United States', admin_1='USA', admin_2='California', admin_3='*', level=3)
        """
        self.admin_1 = self._top_level_region_parser(admin_1).alpha_3
        self.country = self._top_level_region_parser(admin_1).name

        self.admin_2 = admin_2
        self.admin_3 = admin_3

        if not level is None:
            if not (1 <= level <= 3):
                raise ValueError('Level must be between 1 and 3 (inclusive).')

            #  Specifying a level and an administrative region at or below that
            #  level doesn't make sense, so throw an exception for that here
            if (self.admin_2 and level <= 2) or (self.admin_3):
                raise ValueError(
                    '`level` argument is used to return data for all '
                    'administrative regions at that level, so passing a '
                    '`level <= 2` and `admin_2` is not supported, neither is '
                    'passing any level and an `admin_3`.'
                )
        else:
            if self.admin_1 is None:
                level = 1
            else:
                #  Sets level to the highest specified administrative region
                level = max(
                    [
                        i + 1
                        for (i, v) in enumerate(
                            (self.admin_1, self.admin_2, self.admin_3)
                        )
                        if not v is None
                    ]
                )

        self.level = level

        #  The full data is always stored even if you end up filtering it down
        self.data = covid19dh.get(
            self.admin_1,
            level=self.level,
            start=start,
            end=end,
            raw=raw,
            vintage=vintage,
        )

        if self.level >= 2:
            if admin_2:
                if admin_2 != '*':
                    self._check_admin_level(admin_2, level=2)
                self._admin_2 = admin_2

                self.data = self.data[
                    self.data['administrative_area_level_2'] == self._admin_2
                ]
            else:
                self._admin_2 = '*'
        else:
            self._admin_2 = None

        if self.level == 3:
            if admin_3:
                if admin_3 != '*':
                    self._check_admin_level(admin_3, level=3)
                self._admin_3 = admin_3

                self.data = self.data[
                    self.data['administrative_area_level_3'] == self.admin_3
                ]
            else:
                self._admin_3 = '*'
        else:
            self._admin = None

    @staticmethod
    def _top_level_region_parser(region: Optional[str]):
        if region is None:
            #  If `admin_1` was set to `None`, then we return the entire unfiltered
            #  dataset, so no checks need to be performed
            return namedtuple('Country', ['alpha_3', 'name'])(None, None)

        try:
            pyc_admin_1: pycountry.db.Country = pycountry.countries.lookup(region)  # type: ignore
        except LookupError:
            pyc_region_matches: list = pycountry.countries.search_fuzzy(region)
            if len(pyc_region_matches) > 1:
                raise LookupError(
                    f'{region} too ambiguous, {len(pyc_region_matches)}'
                    f'matches. Please use a more specific region name, or use'
                    f'the ISO country code. Available matches are:'
                    f'\n{[c.name for c in pyc_region_matches]}'
                )
            pyc_admin_1: pycountry.db.Country = pyc_region_matches[0]  # type: ignore

        return pyc_admin_1

    def _check_admin_level(self, admin_target: str, level: int):
        admin_names = self.data[f'administrative_area_level_{level}'].unique()
        if not admin_target in admin_names:
            raise LookupError(
                f'{admin_target} not found in data for {self.admin_1}, availabe '
                f'regions are: {admin_names.tolist()}'
            )

        return True

    @property
    def cite(self) -> List[str]:
        return covid19dh.cite(self.data)  # type: ignore

    def __str__(self) -> str:
        if self.country is None:
            return f"All level {self.level} regions"

        a = f"{self.country} ({self.admin_1})"

        b = ", ".join([r for r in [self.admin_2, self.admin_3] if not r is None])

        if b == '':
            return a
        else:
            return ": ".join([a, b])

    def __repr__(self):
        fields = {
            f: getattr(self, f)
            for f in ['country', 'admin_1', 'admin_2', 'admin_3', 'level']
        }
        fields = ', '.join('%s=%r' % i for i in fields.items())
        return f'{self.__class__.__name__}({fields})'
