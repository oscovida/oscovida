import pandas as pd
import time
import joblib
import datetime

# set up joblib memory to avoid re-fetching files
joblib_location = "./cachedir"
joblib_memory = joblib.Memory(joblib_location, verbose=0)


@joblib_memory.cache
def fetch_data_hungary_last_execution():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


@joblib_memory.cache
def fetch_data_hungary():
    """
    Fetch data for Hungary from :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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


def get_region_hungary(county):
    """
    Returns cases int time series and label for county in Hungary.

    """
    counties_and_the_capital_city = \
        ['Bács-Kiskun', 'Baranya', 'Békés', 'Borsod-Abaúj-Zemplén', 'Budapest', 'Csongrád', 'Fejér',
         'Győr-Moson-Sopron', 'Hajú-Bihar', 'Heves', 'Jász-Nagykun-Szolnok', 'Komárom-Esztergom', 'Nógrád', 'Pest',
         'Somogy', 'Szabolcs-Szatmár-Bereg', 'Tolna', 'Vas', 'Veszprém', 'Zala']

    if county not in counties_and_the_capital_city:
        raise ValueError(f'{county} must be one of: \n{counties_and_the_capital_city}')

    hungary = fetch_data_hungary()

    hungary.set_index(pd.to_datetime(hungary['Dátum']), inplace=True)
    cases = hungary[county]
    region_label = f'Hungary-{county}'
    cases.name = region_label + "cases"

    return cases, None, region_label
