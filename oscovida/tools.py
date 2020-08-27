import datetime as dt

import pandas as pd

from oscovida import fetch_data_germany, get_country_data, germany_get_population, fetch_cases, get_population


def two_weeks_cumulative_number_germany() -> pd.DataFrame:
    pd.set_option("max_rows", None)

    # get districts
    germany = fetch_data_germany()
    districts = sorted(germany['Landkreis'].drop_duplicates())

    data = []
    yesterday = dt.date.today() - dt.timedelta(days=1)

    for i, district in enumerate(districts):
        # if i % 100 == 0:
        #     print(f"Processing {i}/412 ({district})")
        c, _, _ = get_country_data(country="Germany", subregion=district)
        if c.index[-1].date() < yesterday:
            # print(f"{district}: last data is from {c.index[-1].date()}")
            origin = c.index[0].date()
            # Fill data series forward up to yesterday
            new_idx = pd.date_range(origin, periods=(yesterday - origin).days, freq='D')
            c.reindex(new_idx, method='pad')
        c = c[-15:]

        population = germany_get_population(landkreis=district)
        new_cases = int(c[-1] - c[-15])
        incidence = new_cases / population * 100000.
        data += [(district, population, new_cases, round(incidence, 1))]

    # sort, and ignore SK and LK for sorting
    data.sort(key=lambda x: x[0].replace("SK ", "").replace("LK ", ""))

    # turn into pandas DataFrame for easier display
    table = pd.DataFrame(data, columns=["district", "population", "new cases", "14-day-incidence"]).set_index(
        "district")

    # Show last update date
    import time
    print(f"Last updated {time.asctime()}")
    return table


def two_weeks_cumulative_number() -> pd.DataFrame:
    pd.set_option("max_rows", None)

    # get a list of all country names
    countries = fetch_cases().index.drop_duplicates()

    data = []
    yesterday = dt.date.today() - dt.timedelta(days=1)

    for region in countries:
        c, _, _ = get_country_data(region)   # get cumulative infections c
        if c.index[-1].date() < yesterday:
            print(f"{region}: last data is from {c.index[-1].date()}")
            origin = c.index[0].date()
            # Fill data series forward up to yesterday
            new_idx = pd.date_range(origin, periods=(yesterday - origin).days, freq='D')
            c.reindex(new_idx, method='pad')
        c = c[-15:]
        try:
            population = get_population(region)
            new_cases = int(c[-1] - c[-15])
            incidence = new_cases / population * 100000.
            data += [(region, population, new_cases, round(incidence, 1))]
        except ValueError:
            print(f"Skip {region}")    # skip regions for which we have no population numbers

    data.sort(key=lambda x: x[3], reverse=True)

    # turn into pandas DataFrame for easier display
    table = pd.DataFrame(data, columns=["country", "population", "new cases", "14-day-incidence"]).set_index("country")

    # Show last update date
    import time
    print(f"Last updated {time.asctime()}")
    return table