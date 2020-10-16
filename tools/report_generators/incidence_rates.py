import datetime
import logging
import os
from typing import List

from pandas import DataFrame
import numpy as np

from .index import compose_md_url


def create_markdown_incidence_list(regions: DataFrame, threshold):
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

    period = [x for x in regions.columns if x.endswith("-day-incidence-rate")][0]
    period = period.strip("-day-incidence-rate")

    # select columns
    regions3 = regions2[
        ["population", f"{period}-day-sum", f"{period}-day-incidence-rate"]
    ]

    regions3[f"{period}-day-sum"] = regions3[f"{period}-day-sum"].astype(int)
    regions3[f"population"] = regions3[f"population"].astype(int)
    regions3[f"{period}-day-incidence-rate"] = regions3[
        f"{period}-day-incidence-rate"
    ].round(1)
    regions3[f"{period}-day-incidence-rate"][regions3[f"{period}-day-incidence-rate"].isnull()] = -1

    regions4 = regions3.applymap(
        lambda v: "missing" if v is None else "{:,}".format(v)
    )  # Thousands comma separator

    # rename columns
    rename_dict = {
        f"{period}-day-sum": f"Cases in last {period} days",
        "population": "Population",
        f"{period}-day-incidence-rate": f"{period} Day Incidence Rate",
    }
    regions5 = regions4.rename(columns=rename_dict)

    #  Stupid workaround to fix colours for the DataTables JS rendering.
    #  Basically, datatables can format rows based on the **row** values, but it
    #  does not know the name of the column for some reason, so there's no way
    #  to check "If the 3rd column is >= 20 AND it is called 'incidence rate'",
    #  instead we add a flag column and check if this flag column is True, and
    #  if it is the row is coloured red...
    regions5['FLAG'] = regions5[[f"{period} Day Incidence Rate"]].replace(',', '').astype(float) >= threshold

    logging.info(f"{len(regions5)} regions in markdown index list")

    return regions5.to_markdown()


def create_markdown_incidence_page(
    incidence_rates: DataFrame,
    category: str,
    save_as=None,
    slug=None,
    pelican_file_path=None,
    title_prefix="Tracking plots: ",
    period=14,
    threshold=20
):
    """Create pelican markdown file, like this:

    title: Germany
    tags: Data, Plots, Germany
    save-as: germany-incidence-rate
    date: 2020-04-11 08:00
    """

    md_content = create_markdown_incidence_list(incidence_rates, threshold)

    title_map = {
        "countries": title_prefix + " Countries of the world",
        "germany": title_prefix + " Districts (Landkreise) in Germany",
        "us": title_prefix + " United States",
        "hungary": title_prefix + " Hungary",
        "all-regions": title_prefix + " All regions and countries",
    }

    title = title_map[category]

    if save_as is None:
        save_as = f"{category}-incidence-rate-{period}day-{threshold}cases"
    if slug is None:
        slug = save_as

    if pelican_file_path is None:
        pelican_file_path = f"pelican/content/{category}-incidence-rate-{period}day-{threshold}cases.md"

    index_path = os.path.join(pelican_file_path)

    intro_text = f"""The searchable table below shows {period}-day incidence
rate per 100,000. ([An explanation of the calculation is
available](./14-day-incidence-rate.html)), entries with this incidence rate
greater than {threshold} are highlighted.

Two of these pages are provided:

- [German region incidence rates](./germany-incidence-rate-{period}day-{threshold}cases.html)

- [Worldwide incidence rates](./countries-incidence-rate-{period}day-{threshold}cases.html)
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
        f.write("\n")
        f.write("You can view our data sources [here](./data-sources.html).")
        f.write("\n")

    logging.info(f"Created markdown index file {pelican_file_path}")

    return os.path.join(pelican_file_path)
