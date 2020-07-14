import datetime
import logging
import os
from typing import List

from pandas import DataFrame


# change index to contain URLs and one-line summary in markdown syntax
def compose_md_url(x: List[str]):
    """
    Function is applied to a pandas DataTable along axis=1, expects a list with
    two elements: a lone line summary of the markdown table, as well as its html
    name.

    Returns a string like `[one_line_summary](html_path)` to serve as a
    hyperlink to the generated markdown page.
    """
    one_line_summary, html = x
    if isinstance(html, str):
        return "[" + one_line_summary + "](" + os.path.join("html", html) + ")"
    # if html was not produced, then variable html is np.nan
    elif repr(html) == "nan":
        logging.warn(
            f"Missing html for {one_line_summary} - will not add link to "
            f"html: \n{x}"
        )
        return one_line_summary
    else:
        raise NotImplementedError(
            "Don't know how to proceed: ", one_line_summary, html, x
        )


def create_markdown_index_list(regions: DataFrame):
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
    regions3 = regions2[["max-cases", "max-deaths", "cases-last-week"]]
    regions4 = regions3.applymap(
        lambda v: "missing" if v is None else "{:,}".format(v)
    )  # Thousands comma separator

    # rename columns
    rename_dict = {
        "max-cases": "Total cases",
        "max-deaths": "Total deaths",
        "cases-last-week": "New cases last week",
    }
    regions5 = regions4.rename(columns=rename_dict)

    logging.info(f"{len(regions5)} regions in markdown index list")

    return regions5.to_markdown()


def create_markdown_index_page(
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

    md_content = create_markdown_index_list(regions)

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
        pelican_file_path = f"pelican/content/{category}.md"

    index_path = os.path.join(pelican_file_path)

    with open(index_path, "tw") as f:
        f.write(f"title: {title}\n")
        # f.write(f"category: Data\n")  - have stopped using categories (22 April 2020)
        f.write(f"tags: Data, Plots, {title}\n")
        f.write(f"save-as: {save_as}\n")
        f.write(f"slug: {slug}\n")
        date_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        f.write(f"date: {date_time}\n")
        f.write("\n")
        f.write("\n")
        f.write(md_content)
        f.write("\n")

    logging.info(f"Created markdown index file {pelican_file_path}")

    return os.path.join(pelican_file_path)
