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
from oscovida import (
    get_population,
    germany_get_population,
    fetch_cases,
    fetch_deaths,
    fetch_data_germany,
)

from urllib.error import HTTPError
from http.client import RemoteDisconnected


def get_incidence_rates_countries(period=14):
    cases = fetch_cases()
    deaths = fetch_deaths()

    #  Sanity checks that the column format is as expected
    assert all(cases.columns == deaths.columns)
    assert all(cases.columns[:3] == ["Province/State", "Lat", "Long"])

    yesterday = dt.datetime.now() - dt.timedelta(days=1)
    fortnight_ago = yesterday - dt.timedelta(days=period)
    periods = (fortnight_ago < pd.to_datetime(cases.columns[3:])) & (
        pd.to_datetime(cases.columns[3:]) < yesterday
    )
    periods = np.concatenate((np.full(3, False), periods))  # Add the 3 ignored columns

    assert len(periods) == len(cases.columns)

    cases_sum = (
        cases[cases.columns[periods]]
        .diff(axis=1)
        .sum(axis=1)
        .to_frame(f"{period}-day-sum")
    )
    deaths_sum = (
        deaths[deaths.columns[periods]]
        .diff(axis=1)
        .sum(axis=1)
        .to_frame(f"{period}-day-sum")
    )

    # Now we have tables like:
    #                     14-day-sum
    # Country/Region
    # Afghanistan              841.0
    # ...                        ...
    # Zimbabwe                1294.0
    #
    # [266 rows x 1 columns]
    # Where the values are the total cases/deaths in the past `period` days

    population = (
        get_population()
        .set_index('Combined_Key')
        .rename(columns={"Population": "population"})
        .population
    )

    cases_incidence = cases_sum.join(population)
    cases_incidence.index.name = "Country"
    cases_incidence["incidence"] = (
        cases_incidence[f"{period}-day-sum"] / cases_incidence["population"] * 100_000
    )
    deaths_incidence = deaths_sum.join(population)
    deaths_incidence.index.name = "Country"
    deaths_incidence["incidence"] = (
        deaths_incidence[f"{period}-day-sum"] / deaths_incidence["population"] * 100_000
    )

    # We could join the tables, but it's easier to join them than to split so
    # we'll just return two instead
    return cases_incidence, deaths_incidence


def get_incidence_rates_germany(period=14):
    germany = fetch_data_germany()
    germany = germany.rename(
        columns={"AnzahlFall": "cases", "AnzahlTodesfall": "deaths"}
    )

    yesterday = dt.datetime.now() - dt.timedelta(days=1)
    fortnight_ago = yesterday - dt.timedelta(days=period)
    periods = (fortnight_ago < germany.index) & (germany.index < yesterday)
    germany = germany.iloc[periods]

    cases = germany[["Landkreis", "cases"]]
    deaths = germany[["Landkreis", "deaths"]]

    cases_sum = (
        cases.groupby("Landkreis")
        .sum()
        .rename(columns={"cases": f"{period}-day-sum"})
    )
    deaths_sum = (
        deaths.groupby("Landkreis")
        .sum()
        .rename(columns={"deaths": f"{period}-day-sum"})
    )

    # Now we have tables like:
    #                            cases
    # Landkreis
    # LK Ahrweiler                       32
    # ...                               ...
    # StadtRegion Aachen                109
    # [406 rows x 1 columns]
    # Where the values are the total cases/deaths in the past `period` days

    population = (
        germany_get_population()
        .set_index('county')
        .rename(columns={"EWZ": "population"})
        .population
        .to_frame()
    )

    cases_incidence = cases_sum.join(population)
    cases_incidence["incidence"] = (
        cases_incidence[f"{period}-day-sum"] / cases_incidence["population"] * 100_000
    )
    deaths_incidence = deaths_sum.join(population)
    deaths_incidence["incidence"] = (
        deaths_incidence[f"{period}-day-sum"] / deaths_incidence["population"] * 100_000
    )

    # We could join the tables, but it's easier to join them than to split so
    # we'll just return two instead
    return cases_incidence, deaths_incidence


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
    save-as: germany-incidence-rate
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
        save_as = category + "-incidence-rate"
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
