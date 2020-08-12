"""Code used for notebooks and data exploration on
https://github.com/oscovida/oscovida"""


import datetime
import os
import time

import joblib
import numpy as np
import pandas as pd
import pytz

LW = 3   # line width



# set up joblib memory to avoid re-fetching files
joblib_location = "./cachedir"
joblib_memory = joblib.Memory(joblib_location, verbose=0)


def clear_cache():
    """Need to run this before new data for the day is created"""
    joblib_memory.clear()


def report_download(url, df):
    print(f"Downloaded data: last data point {df.columns[-1]} from {url}")


@joblib_memory.cache
def fetch_deaths_last_execution():
    """Use to remember at what time and date the last set of deaths was downloaded.
    A bit of a hack as we didn't know how to get this out of joblib.
    """
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


@joblib_memory.cache
def fetch_cases_last_execution():
    """See fetch_deaths_last_execution"""
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


@joblib_memory.cache
def fetch_deaths():
    """Download deaths from Johns Hopkins data repository"""
    url = os.path.join(base_url, "time_series_covid19_" + "deaths" + "_global.csv")
    df = pd.read_csv(url, index_col=1)
    report_download(url, df)
    fetch_deaths_last_execution()
    return df

@joblib_memory.cache
def fetch_deaths_US():
    """Download deaths for US states from Johns Hopkins data repository"""
    url = os.path.join(base_url, "time_series_covid19_" + "deaths" + "_US.csv")
    df = pd.read_csv(url, index_col=1)
    report_download(url, df)
    # fetch_deaths_last_execution_()
    return df


@joblib_memory.cache
def fetch_cases():
    """Download cases from Johns Hopkins data repository"""
    url = os.path.join(base_url, "time_series_covid19_" + "confirmed" + "_global.csv")
    df = pd.read_csv(url, index_col=1)
    report_download(url, df)
    fetch_cases_last_execution()
    return df

@joblib_memory.cache
def fetch_cases_US():
    """Download cases for US status from Johns Hopkins data repository"""
    url = os.path.join(base_url, "time_series_covid19_" + "confirmed" + "_US.csv")
    df = pd.read_csv(url, index_col=1)
    report_download(url, df)
    fetch_cases_last_execution()
    return df


def get_country_data_johns_hopkins(country):
    """Given a country name, return deaths and cases as a tuple of
    pandas time series. Works for all (?) countries in the world, or at least
    those in the Johns Hopkins data set. All rows should contain a datetime
    index and a value.
    """

    deaths = fetch_deaths()
    cases = fetch_cases()

    assert country in deaths.index, f"{country} not in available countries. These are {sorted(deaths.index)}"

    # Some countries report sub areas (i.e. multiple rows per country) such as China, France, United Kingdom
    # Denmark. In that case, we sum over all regions.
    tmp = deaths.loc[country]
    if len(tmp.shape) == 1:
        d = deaths.loc[country]
    elif len(tmp.shape) == 2:   # China, France, United Kingdom, ...
        d = deaths.loc[country].sum()
        d.rename("deaths", inplace=True)
    else:
        raise ValueError("Unknown data set structure for deaths {country}:", tmp)

    tmp = cases.loc[country]
    if len(tmp.shape) == 1:
        c = cases.loc[country]
    elif len(tmp.shape) == 2:
        c = cases.loc[country].sum()
        c.rename("cases", inplace=True)
    else:
        raise ValueError("Unknown data set structure for cases {country}:", tmp)

    # make date string into timeindex
    d.index = pd.to_datetime(d.index, errors="coerce", format="%m/%d/%y")
    c.index = pd.to_datetime(c.index, errors="coerce", format="%m/%d/%y")
    # drop all rows that don't have data
    # sanity check: how many do we drop?
    if c.index.isnull().sum() > 3:
        print(f"about to drop {c.index.isnull().sum()} entries due to NaT in index", c)
    c = c[c.index.notnull()]

    if d.index.isnull().sum() > 3:
        print(f"about to drop {d.index.isnull().sum()} entries due to NaT in index", d)
    d = d[d.index.notnull()]

    # check there are no NaN is in the data
    assert c.isnull().sum() == 0, f"{c.isnull().sum()} NaNs in {c}"
    assert d.isnull().sum() == 0, f"{d.isnull().sum()} NaNs in {d}"

    # label data
    c.name = country + " cases"
    d.name = country + " deaths"

    return c, d


def get_US_region_list():
    """return list of strings with US state names"""
    deaths = fetch_deaths_US()
    return list(deaths.groupby("Province_State").sum().index)


def get_region_US(state, county=None, debug=False):
    """Given a US state name and county, return deaths and cases as a tuple of pandas time
    series. (Johns Hopkins data set)

    If country is None, then sum over all counties in that state (i.e. return
    the numbers for the state.)

    """

    if not county is None:
        raise NotImplementedError("Can only process US states (no counties)")

    deaths = fetch_deaths_US()
    cases = fetch_cases_US()

    assert state in deaths['Province_State'].values, \
        f"{state} not in available states. These are {sorted(deaths['Province_State'])}"

    if county is None:
        tmpd = deaths.groupby('Province_State').sum()
        d = tmpd.loc[state]
        tmpc = cases.groupby('Province_State').sum()
        c = tmpc.loc[state]
    else:
        raise NotImplementedError("Can't do counties yet.")
    # Some countries report sub areas (i.e. multiple rows per country) such as China, France, United Kingdom
    # Denmark. In that case, we sum over all regions.

    # make date string into timeindex
    d.index = pd.to_datetime(d.index, errors="coerce", format="%m/%d/%y")
    c.index = pd.to_datetime(c.index, errors="coerce", format="%m/%d/%y")
    # drop all rows that don't have data
    # sanity check: how many do we drop?
    if c.index.isnull().sum() > 3:
        if debug:
            print(f"about to drop {c.index.isnull().sum()} entries due to NaT in index", c)
    c = c[c.index.notnull()]

    if d.index.isnull().sum() > 3:
        if debug:
            print(f"about to drop {d.index.isnull().sum()} entries due to NaT in index", d)
    d = d[d.index.notnull()]

    # check there are no NaN is in the data
    assert c.isnull().sum() == 0, f"{c.isnull().sum()} NaNs in {c}"
    assert d.isnull().sum() == 0, f"{d.isnull().sum()} NaNs in {d}"

    # label data
    country = f"US-{state}"
    c.name = country + " cases"
    d.name = country + " deaths"

    return c, d


def compose_dataframe_summary(cases, deaths):
    """Used in per-country template to show data table.
    Could be extended.

    Expects series of cases and deaths (time-aligned), combines those in DataFrame and returns it
    """
    df = pd.DataFrame()
    df["total cases"] = cases
    df["daily new cases"] = cases.diff()
    if deaths is not None:
        df["total deaths"] = deaths
        df["daily new deaths"] = deaths.diff()

    # drop first row with nan -> otherwise ints are shows as float in table
    df = df.dropna().astype(int)

    # change index: latest numbers shown first
    df = df[::-1]

    return df


@joblib_memory.cache
def fetch_data_germany_last_execution():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


@joblib_memory.cache
def fetch_data_germany(include_last_day=True):
    """Fetch data for Germany from Robert Koch institute.

    Data source is https://npgeo-corona-npgeo-de.hub.arcgis.com . The text on the
    webpage implies that the data comes from the Robert Koch Institute.

    By default, we omit the last day with data from the retrieved data sets
    (see reasoning below in source), as the data is commonly update one day
    later with more accurate (and typically higher) numbers.

    """

    # outdated: datasource = "https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv"
    datasource = "https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data"
    t0 = time.time()
    print(f"Please be patient - downloading data from {datasource} ...")
    germany = pd.read_csv(datasource)
    delta_t = time.time() - t0
    print(f"Completed downloading {len(germany)} rows in {delta_t:.1f} seconds.")

    ## create new column 'landkreis' and get rid of "SK " and "LK " for this
    ## - this is too simplistic. We have fields like "Region Hannover"
    # germany['landkreis'] = germany['Landkreis'].apply(lambda s: s[3:])

    # (at least) the last data from the Robert-Koch-Institute (RKI) seems not to be
    # fully reported the day after. For example, on 3 April, the number of cases
    # from RKI is well below what is expected. Example:
    #
    # From RKI (as of evening of 2020-04-03:)
    # 2020-03-29    62653
    # 2020-03-30    66692
    # 2020-03-31    72333
    # 2020-04-01    77464
    # 2020-04-02    79625
    #
    # From Johns Hopkins (as of evening of 2020-04-03:):
    # 2020-03-29    62095
    # 2020-03-30    66885
    # 2020-03-31    71808
    # 2020-04-01    77872
    # 2020-04-02    84794
    #
    # So we must assume that the RKI data will be corrected later; maybe the next day.
    #
    # To make our plots not inaccurate, we'll remove the last data point from the RKI data:
    g2 = germany.set_index(pd.to_datetime(germany['Meldedatum']))
    g2.index.name = 'date'

    # get rid of last day in data if desired
    if include_last_day == False:
        last_day = g2.index.max()
        sel = g2.index == last_day
        cleaned = g2.drop(g2[sel].index, inplace=False)
    else:
        cleaned = g2

    fetch_data_germany_last_execution()
    return cleaned


def pad_cumulative_series_to_yesterday(series):
    """Given a time series with date as index and cumulative cases/deaths as values:

    - if the last date in the index is older than yesterday, then
    - add that date
    - resample the series with a daily interval, using padding with last known value
    - and return.

    Required for Robert Koch Data, where only a new data point is provided if
    the numbers change, but the plotting algorithms need to know that there is
    no change. Without this padding, the data set looks old as the last plotted
    data point is the last one for which data is provided.
    """
    now = datetime.datetime.now()
    rki_tz = pytz.timezone('Europe/Berlin')
    now_tz = datetime.datetime.now(rki_tz)

    # remove time zone information from datetime, so we can compare against
    # datatime dates from get_country_data which has no timezone information
    # attached.
    now = now.replace(tzinfo=None)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - pd.Timedelta("1D")
    last = series.index.max()
    if last < yesterday:
        # repeat last data point with index for yesterday
        series[yesterday] = series[last]
        series2 = series.resample("1D").pad()
        return series2
    else:
        return series


def germany_get_region(state=None, landkreis=None, pad2yesterday=False):
    """ Returns cases and deaths time series for Germany, and a label for the state/kreis.

    If state is given, return sum of cases (as function of time) in that state (state=Bundesland)

    If Landkreis is given, return data from just that Landkreis.

    Landkreis seems unique, so there is no need to provide state and Landkreis.

    [Should tidy up names here; maybe go to region and subregion in the function argument name, and
    translate later.]
    """
    germany = fetch_data_germany()
    """Returns two time series: (cases, deaths)"""
    assert state or landkreis, "Need to provide a value for state or landkreis"

    if state and landkreis:
        raise NotImplementedError("Try to use 'None' for the state.")
        """We need to check if this is important."""

    if state:
        assert state in germany['Bundesland'].values, \
            f"{state} not in available German states. These are {sorted(germany['Bundesland'].drop_duplicates())}"

        land = germany[germany['Bundesland'] == state]
        land = land.set_index(pd.to_datetime(land['Meldedatum']))
        land.index.name = 'date'
        land.sort_index(inplace=True)

        # group over multiple rows for the same date
        # (this will also group over the different landkreise in the state)
        cases = land["AnzahlFall"].groupby('date').agg('sum').cumsum()
        region_label = f'Germany-{state}'
        cases.name = region_label + " cases"

        # group over all multiple entries per day
        deaths = land["AnzahlTodesfall"].groupby('date').agg('sum').cumsum()
        deaths.name = region_label + " deaths"

        if pad2yesterday:
            deaths = pad_cumulative_series_to_yesterday(deaths)
            cases = pad_cumulative_series_to_yesterday(cases)

        return cases, deaths, region_label

    if landkreis:
        assert landkreis in germany['Landkreis'].values, \
            f"{state} not in available German states. These are {sorted(germany['Landkreis'].drop_duplicates())}"

        lk = germany[germany["Landkreis"] == landkreis]
        lk.index = pd.to_datetime(lk['Meldedatum'])
        lk.index.name = 'date'
        lk = lk.sort_index()

        cases = lk["AnzahlFall"].groupby('date').agg('sum').cumsum()
        region_label = f'Germany-{landkreis}'
        cases.name = region_label + ' cases'

        deaths = lk["AnzahlTodesfall"].groupby('date').agg('sum').cumsum()
        deaths.name = region_label + ' deaths'

        if pad2yesterday:
            deaths = pad_cumulative_series_to_yesterday(deaths)
            cases = pad_cumulative_series_to_yesterday(cases)

        return cases, deaths, region_label

    raise NotImplemented("Should never get to this point.")


@joblib_memory.cache
def fetch_data_hungary_last_execution():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


@joblib_memory.cache
def fetch_data_hungary():
    """
    Fetch data for Hungary from https://github.com/sanbrock/covid19

    Dataset does not contain the number of deaths in each county/capital city.
    """
    datasource = r'https://raw.githubusercontent.com/sanbrock/covid19/master/datafile.csv'

    t0 = time.time()
    print(f"Please be patient - downloading data from {datasource} ...")
    hungary = pd.read_csv(datasource)
    delta_t = time.time() - t0
    print(f"Completed downloading {len(hungary)} rows in {delta_t:.1f} seconds.")

    # Dropping the last row, because it is a duplicate of header.
    hungary.drop(hungary.index[-1], inplace=True)
    # Will be at least one date with no values.
    hungary.dropna(inplace=True)

    hungary = hungary.astype({col_name: int for col_name in hungary.columns[1:]})

    fetch_data_hungary_last_execution()
    return hungary


def get_counties_hungary():
    # return fetch_data_hungary().columns[1:]
    return ['Bács-Kiskun', 'Baranya', 'Békés', 'Borsod-Abaúj-Zemplén', 'Budapest', 'Csongrád', 'Fejér',
            'Győr-Moson-Sopron', 'Hajú-Bihar', 'Heves', 'Jász-Nagykun-Szolnok', 'Komárom-Esztergom', 'Nógrád', 'Pest',
            'Somogy', 'Szabolcs-Szatmár-Bereg', 'Tolna', 'Vas', 'Veszprém', 'Zala']


def get_region_hungary(county):
    """
    Returns cases int time series and label for county in Hungary.

    """
    counties_and_the_capital_city = get_counties_hungary()

    if county not in counties_and_the_capital_city:
        raise ValueError(f'{county} must be one of: \n{counties_and_the_capital_city}')

    hungary = fetch_data_hungary()

    hungary.set_index(pd.to_datetime(hungary['Dátum']), inplace=True)
    cases = hungary[county]
    region_label = f'Hungary-{county}'
    cases.name = region_label + " cases"

    return cases, None, region_label


def get_country_data(country, region=None, subregion=None, verbose=False, pad_RKI_data_to_yesterday=True):
    """Given the name of a country, get the Johns Hopkins data for cases and deaths,
    and return them as a tuple of pandas.Series objects and a string describing the region:
    (cases, deaths, region_label)

    If the country is "Germany", use the region (=Land) and subregion (=Kreis)
    to select the appropriate subset from the Robert Koch Institute. If only
    the region is provided, the data from all subregions in that region is
    accumulated.

    If the country is "US", get US data (states are available as regions) from Johns Hopkins
    repository.

    Returns "cases, deaths, country_region" where country region is a string
    describing the country and region.

    The series are resampled at a daily interval. Missing data points are replaced
    by the last provided value (seems reasonable for a data set representing
    cumulative numbers as a function of time: where no new data point is provided,
    assume the change was zero, thus the last data point can be re-used).

    Data from Johns Hopkins is reported daily, even if there is no change in numbers.

    Data from Robert Koch Institute (RKI) is only provided if the cumulative
    numbers change. We thus resample the data set if the last provided data
    point is not from yesterday, up to yesterday (which is the most recent day
    for which data could be available).

    Note that some data sets are updated retrospectively (in particular data
    from RKI), so the numbers for the a particular date may increase after one
    or two days (or even later in extreme cases).

    """

    if country.lower() == 'germany':
        if region == None and subregion == None:
            c, d = get_country_data_johns_hopkins(country)  # use johns hopkins data
            country_region = country
        else:
            # use German data
            c, d, country_region = germany_get_region(state=region, landkreis=subregion,
                                                      pad2yesterday=pad_RKI_data_to_yesterday)
    elif country.lower() == 'us' and region != None:
        # load US data
        c, d = get_region_US(region)
        country_region = f"United States: {region}"

    elif country.lower() == 'hungary':
        # region -> térség
        # subregion -> kistérség
        # county -> megye

        if region is not None:
            c, d, country_region = get_region_hungary(county=region)

        else:
            c, d = get_country_data_johns_hopkins(country)
            country_region = country

    else:
        c, d = get_country_data_johns_hopkins(country)
        country_region = country

    len_cases1 = len(c)
    # hungarian county data doesn't contain number of deaths
    len_deaths1 = 0 if d is None else len(d)
    # resample data so we have one value per day
    c = c.resample("D").pad()
    d = None if d is None else d.resample("D").pad()

    len_cases2 = len(c)
    len_deaths2 = 0 if d is None else len(d)

    if verbose:
        print(f"get_country_data: cases [{len_cases1}] -> [{len_cases2}]")
        print(f"get_country_data: deaths[{len_deaths1}] -> [{len_deaths2}]")
    return c, d, country_region

#######################

def day0atleast(v0, series):
    try:
        day0 = series[series > v0].index[0]
    except IndexError:  # means no days found for which series.values > v0
        # print(f"Haven't found value > {v0} is Series {series.name}")
        result = pd.Series(dtype=object)
        return result

    # compute timedelta
    timedelta = series.index - day0
    # convert to int as index
    t = pd.to_numeric(timedelta.astype("timedelta64[D]").astype(int))
    # Assemble new series
    result = pd.Series(index=t, data=series.values)

    return result


def align_sets_at(v0, df):
    """Accepts data frame, and aligns so that all enttries close to v0 are on the same row.

    Returns new dataframe with integer index (representing days after v0).
    """
    res = pd.DataFrame()

    for col in df.columns:
        # res[col] = day0for(v0, df[col])
        series = day0atleast(v0, df[col])
        series.name = col
        res = pd.merge(res, series, how='outer', left_index=True, right_index=True)

    return res


def get_compare_data(countrynames, rolling=7):
    """Given a list of country names, return two dataframes: one with cases and one with deaths
    where
    - each column is one country
    - data in the column is the diff of accumulated numbers
    - any zero values are removed for italy (data error)
    - apply some smoothing
    """
    df_c = pd.DataFrame()
    df_d = pd.DataFrame()

    for countryname in countrynames:
        c, d = get_country_data_johns_hopkins(countryname)

        df_c[countryname] = c.diff().rolling(rolling, center=True).mean()  # cases
        df_d[countryname] = d.diff().rolling(rolling, center=True).mean()  # deaths

    return df_c, df_d


def label_from_region_subregion(region_subregion):
    region, subregion = unpack_region_subregion(region_subregion)
    if subregion:
        if region:
            label = f"{region}-{subregion}"
        else:
            label = f"{subregion}"
    else:
        label = f"{region}"
    return label


def unpack_region_subregion(region_subregion):
    """Convention for regions in Germany (could also be useful for other countries later):

    - region_subregion is either
      - a tuple of strings (region, subregion) or
      - a string "region"

    Return a a tuple (region, subregion), where subregion is None if not provided.
    """
    if isinstance(region_subregion, tuple):
        if len(region_subregion) == 1:
            region = region_subregion[0]
            subregion = None
        elif len(region_subregion) == 2:
            region, subregion = region_subregion
        else:
            raise ValueError("region_subregion must be single value or 2-valued tuple", region_subregion)
    else:
        # assume it is just the region
        assert isinstance(region_subregion, str)
        region, subregion = region_subregion, None
    return region, subregion


def get_compare_data_germany(region_subregion, compare_with_local, rolling=7):
    """Given a region_subregion for Germany, and a list of region_subregion to compare with,
    return two dataframes: one with cases and one with deaths
    where
    - each column is one country
    - data in the column is the diff of accumulated numbers
    - any zero values are removed for italy (data error)
    - apply some smoothing

    See unpack_region_subregion for details on region_subregion.
    """
    df_c = pd.DataFrame()
    df_d = pd.DataFrame()

    for reg_subreg in [region_subregion] + compare_with_local:

        region, subregion = unpack_region_subregion(reg_subreg)
        c, d, country_subregion = germany_get_region(state=region, landkreis=subregion)

        label = label_from_region_subregion((region, subregion))
        df_c[label] = c.diff().rolling(rolling, center=True).mean()  # cases
        df_d[label] = d.diff().rolling(rolling, center=True).mean()  # deaths

    return df_c, df_d


def get_compare_data_hungary(region, compare_with_local: list, rolling=7):
    """Given a region for Hungary, and a list of regions to compare with,
    return two dataframes: one with cases and one with deaths
    where
    - each column is one country
    - data in the column is the diff of accumulated numbers
    - any zero values are removed for italy (data error)
    - apply some smoothing

    """
    df_c = pd.DataFrame()
    # df_d = pd.DataFrame()
    for reg in [region] + compare_with_local:
        c, d, country_subregion = get_region_hungary(county=reg)
        label = str(reg)
        df_c[label] = c.diff().rolling(rolling, center=True).mean()  # cases
        # df_d[label] = d.diff().rolling(rolling, center=True).mean()  # deaths
    return df_c, None


def choose_random_counties(exclude_region, size) -> list:
    counties = get_counties_hungary()
    assert exclude_region in counties

    counties.remove('Budapest')
    if exclude_region != 'Budapest':
        counties.remove(exclude_region)

    indices = np.arange(len(counties))
    np.random.shuffle(indices)

    counties = np.array(counties)
    choosen = counties[indices[:size]]
    choosen = list(np.concatenate((choosen, ['Budapest'])))
    return choosen


def get_cases_last_week(cases):
    """Given cumulative cases time series, return the number of cases from the last week.
    """
    # make sure we have one value for every day
    c2 = cases.resample('D').pad()
    # last week is difference between last value, and the one 7 days before
    cases_last_week = c2[-1] - c2[-8]
    return cases_last_week
