import datetime
import logging
import os
from typing import List

from pandas import DataFrame
import numpy as np

from .index import compose_md_url

### TEMPORARY
import datetime as dt
import pandas as pd

pd.set_option("max_rows", None)
from oscovida import get_population, germany_get_population, get_country_data

from urllib.error import HTTPError
from http.client import RemoteDisconnected


def compute_incidence_rates_countries(region_name: str):
    yesterday = dt.date.today() - dt.timedelta(days=1)

    c, _, _ = get_country_data(region_name)
    if c.index[-1].date() < yesterday:
        origin = c.index[0].date()
        # Fill data series forward up to yesterday
        new_idx = pd.date_range(origin, periods=(yesterday - origin).days, freq="D")
        c.reindex(new_idx, method="pad")

    c = c[-15:]

    try:
        population = get_population(region_name)
        new_cases = int(c[-1] - c[-15])
        incidence = new_cases / population * 100000.0
        return round(incidence, 1)
    except (ValueError, HTTPError, RemoteDisconnected):
        return np.nan


def compute_incidence_rates_germany(subregion_name: str):
    yesterday = dt.date.today() - dt.timedelta(days=1)

    c, _, _ = get_country_data(country="Germany", subregion=subregion_name)
    if c.index[-1].date() < yesterday:
        origin = c.index[0].date()
        # Fill data series forward up to yesterday
        new_idx = pd.date_range(origin, periods=(yesterday - origin).days, freq="D")
        c.reindex(new_idx, method="pad")

    c = c[-15:]

    try:
        population = germany_get_population(landkreis=subregion_name)
        new_cases = int(c[-1] - c[-15])
        incidence = new_cases / population * 100000.0
        return round(incidence, 1)
    except (ValueError, HTTPError, RemoteDisconnected):
        return np.nan


def append_incidence_rates(regions: pd.DataFrame, category: str):
    # This is terrible but it'll have to do since we have to finish this today...
    if category == "countries":
        regions["14-day-incidence-rate"] = regions.index.to_frame().applymap(
            compute_incidence_rates_countries
        )
    elif category == "germany":
        regions["14-day-incidence-rate"] = regions["subregion"].map(
            compute_incidence_rates_germany
        )
    else:
        raise Exception("Unknown caterory")

    regions = regions.sort_values(by=["14-day-incidence-rate"])

    return regions


### TEMPORARY


def create_markdown_incidence_list(regions: DataFrame):
    # Assemble a markdown table like this:
    #
    # | Country/Region                       | Total cases   | Total deaths   |
    # |:-------------------------------------|:--------------|:---------------|
    # | [Afghanistan](html/Afghanistan.html) | 1,351         | 43             |
    # | [Albania](html/Albania.html)         | 678           | 27             |
    # | [Algeria](html/Algeria.html)         | 3,127         | 415            |
    # | [Andorra](html/Andorra.html)         | 731           | 40             |
    #
    # and return as string.

    new_index = regions[["one-line-summary", "html-file"]].apply(compose_md_url, axis=1)
    regions2 = regions.set_index(new_index)
    regions2.index.name = "Location"

    # select columns
    regions3 = regions2[
        ["max-cases", "max-deaths", "cases-last-week", "14-day-incidence-rate"]
    ]
    regions4 = regions3.applymap(
        lambda v: "missing" if v is None else "{:,}".format(v)
    )  # Thousands comma separator

    # rename columns
    rename_dict = {
        "max-cases": "Total cases",
        "max-deaths": "Total deaths",
        "cases-last-week": "New cases last week",
        "14-day-incidence-rate": "14 Day Incidence Rate",
    }
    regions5 = regions4.rename(columns=rename_dict)

    logging.info(f"{len(regions5)} regions in markdown index list")

    return regions5.to_markdown()


def create_markdown_incidence_page(
    regions: DataFrame,
    category: str,
    save_as=None,
    slug=None,
    pelican_file_path=None,
    title_prefix="Tracking plots: ",
):
    """Create pelican markdown file, like this:

    title: Germany
    tags: Data, Plots, Germany
    save-as: germany
    date: 2020-04-11 08:00
    """

    regions = append_incidence_rates(regions, category)

    md_content = create_markdown_incidence_list(regions)

    title_map = {
        "countries": title_prefix + " Countries of the world",
        "germany": title_prefix + " Germany",
        "us": title_prefix + " United States",
        "hungary": title_prefix + " Hungary",
        "all-regions": title_prefix + " All regions and countries",
    }

    title = title_map[category]

    if save_as is None:
        save_as = category
    if slug is None:
        slug = save_as

    if pelican_file_path is None:
        pelican_file_path = f"pelican/content/{category}-incidence-rate.md"

    index_path = os.path.join(pelican_file_path)

    intro_text = f"""These are the 14 day incident rate numbers for {category},
any areas with over 20 cases per 100 000 are considered high risk be EuXFEL and
if you have travelled to one of these regions recently you should self-quarantine
at home for two weeks before returning to EuXFEL.
    """

    with open(index_path, "tw") as f:
        f.write(f"title: {title}\n")
        # f.write(f"category: Data\n")  - have stopped using categories (22 April 2020)
        f.write(f"tags: Data, Plots, {title}\n")
        f.write(f"save-as: {save_as}\n")
        f.write(f"slug: {slug}\n")
        date_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        f.write(f"date: {date_time}\n")
        f.write("\n")
        f.write(intro_text)
        f.write("\n")
        f.write(md_content)
        f.write("\n")

    logging.info(f"Created markdown index file {pelican_file_path}")

    return os.path.join(pelican_file_path)
