from functools import lru_cache
from typing import Optional, List

import pycountry
from covid19dh import covid19, cite
from pandas import DataFrame, Series


def fetch_covid19_data(
    country: str = None, level: int = 1, verbose: bool = False
) -> DataFrame:
    """Wraps the `covid19dh.covid19` function in n `functools.lru_cache`.

    `covid19dh.covid19` caches the downloaded data files to disk so that it does
    not have to download them each time, however it does not cache them
    in-memory, and loading the larger files can be a bit slow.
    """
    return covid19(country, level=level, verbose=verbose)


def _check_admin_level_(admin_1: str, admin_target: str, level: int):
    data = fetch_covid19_data(admin_1, level)
    admin_names = data[f'administrative_area_level_{level}'].unique()
    if not admin_target in admin_names:
        raise LookupError(
            f'{admin_target} not found in data for {admin_1}, availabe '
            f'regions are: {admin_names.tolist()}'
        )

#  Really haven't decided on how to do this yet... subclasses? Pipes? accessors?
#
# class SubclassedSeries(Series):
#     @property
#     def _constructor(self):
#         return SubclassedSeries

#     @property
#     def _constructor_expanddim(self):
#         return SubclassedDataFrame


# class SubclassedDataFrame(DataFrame):
#     @property
#     def _constructor(self):
#         return SubclassedDataFrame


class Region:
    def __init__(
        self,
        admin_1: str,
        admin_2: Optional[str] = None,
        admin_3: Optional[str] = None,
        level: Optional[int] = None,
    ) -> None:
        """
        Parameters
        ----------
        admin_1: str
            Country name string (e.g. 'United States') or alpha_3 string,
            administrative area of top level (e.g. 'USA')
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
            (e.g. 'California')
        admin_3: Optional[str]
            Third-level administrative area, usually cities or municipalities
            (e.g. 'San Francisco')
        level: int
            Level of administrative areas specified

        Raises
        ------
        LookupError
            Raised if the `admin_1` string is too ambiguous. For example,
            `RegionData('UK')` will not work as the country code is GB or GBR,
            and UK matches too many possible places.

        Examples
        --------
        You can create a `RegionData` object by calling it with specific levels,
        which will return a filtered DataTable:

        >>> RegionData('GB')
        RegionData(country='United Kingdom', admin_1='GBR', admin_2=None, admin_3=None, level=1)

        >>> RegionData('United Kingdom', 'England')
        RegionData(country='United Kingdom', admin_1='GBR', admin_2='England', admin_3=None, level=2)

        >>> RegionData('United Kingdom', 'England', 'Westminster')
        RegionData(country='United Kingdom', admin_1='GBR', admin_2='England', admin_3='Westminster', level=3)

        Alternatively you can specify a `level` directly, which will not filter
        the administrative regions. For example, getting all level 2 regions for
        the United Kingdom would be:

        >>> RegionData('GB', level=2)
        RegionData(country='United Kingdom', admin_1='GBR', admin_2='*', admin_3=None, level=2)

        Or all level 3:

        >>> RegionData('GB', level=3)
        RegionData(country='United Kingdom', admin_1='GBR', admin_2='*', admin_3='*', level=3)

        Or an administrative level 2, requesting all level 3 regions in it:
        >>> RegionData('GB', 'England', level=3)
        RegionData(country='United Kingdom', admin_1='GBR', admin_2='England', admin_3='*', level=3)
        """
        try:
            pyc_admin_1: pycountry.db.Country = pycountry.countries.lookup(admin_1)
        except LookupError:
            pyc_admin_1_matches: list = pycountry.countries.search_fuzzy(admin_1)
            if len(pyc_admin_1_matches) > 1:
                raise LookupError(
                    f'{admin_1} too ambiguous, {len(pyc_admin_1_matches)}'
                    f'matches. Please use a more specific region name, or use'
                    f'the ISO country code. Available matches are:'
                    f'\n{[c.name for c in pyc_admin_1_matches]}'
                )
            pyc_admin_1: pycountry.db.Country = pyc_admin_1_matches[0]  # type: ignore

        self.country: str = pyc_admin_1.name
        self.admin_1: str = pyc_admin_1.alpha_3
        self.admin_2: Optional[str] = None
        self.admin_3: Optional[str] = None

        #  If the level has been manually specified that (probably) means the
        #  user wants data for all of the administrative regions at that level
        if level or level == 0:  # Explicitly accept level == 0 to throw exception later
            if not (1 <= level <= 3):
                raise ValueError('Level must be between 1 and 3 (inclusive).')

            #  Specifying a level and an administrative region at or below that
            #  level doesn't make sense, so throw an exception for that here
            if (admin_2 and level <= 2) or (admin_3):
                raise ValueError(
                    '`level` argument is used to return data for all '
                    'administrative regions at that level, so passing a '
                    '`level <= 2` and `admin_2` is not supported, neither is '
                    'passing any level and an `admin_3`.'
                )

            if level >= 2:
                if admin_2:
                    _check_admin_level_(self.country, admin_2, 2)
                    self.admin_2 = admin_2
                else:
                    self.admin_2 = '*'
            if level == 3:
                self.admin_3 = '*'

            self.level = level
        else:
            self.level = 1

            if admin_2:
                _check_admin_level_(self.country, admin_2, 2)
                self.level = 2
                self.admin_2 = admin_2

            if admin_3:
                _check_admin_level_(self.country, admin_3, 3)
                self.level = 3
                self.admin_3 = admin_3

        data = fetch_covid19_data(self.admin_1, level=self.level)

        if self.level == 2 and self.admin_2 != '*' and self.admin_2:
            data = data[data['administrative_area_level_2'] == self.admin_2]
        if self.level == 3 and self.admin_3 != '*' and self.admin_3:
            data = data[data['administrative_area_level_3'] == self.admin_3]

        #  This is kind of hacky, but full subclassing the DataFrame is complete
        #  overkill for our needs. If you just add an attribute to a dataframe
        #  the attribute will not persist through standard pandas operations
        #  (e.g. `.copy()`) unless it is added to `DataFrame.._metadata`
        #  so we add an entry of `_oscovida_metadata` to it, then create the
        #  attribute.
        #  https://pandas.pydata.org/pandas-docs/stable/development/extending.html#define-original-properties
        data._metadata.append('_oscovida_metadata')
        data._oscovida_metadata = {}
        data._oscovida_metadata['columns'] = set()

        self.data = data

    @property
    def cite(self) -> List[str]:
        return cite(self.data)

    def __str__(self) -> str:
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
