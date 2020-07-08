import logging
import os
from itertools import compress

import click
import pandas

import oscovida

from .executors import ReportExecutor
from .reporters import (AllRegions, CountryReport, GermanyReport,
                        HungaryReport, USAReport)

ALL_REGIONS = ["countries", "germany", "usa", "hungary", "all-regions-md", "all"]


def does_wwwroot_exist(wwwroot, create=False):
    if not os.path.exists(wwwroot):
        if create:
            os.mkdir(wwwroot)
            os.mkdir(wwwroot + "/ipynb")
            os.mkdir(wwwroot + "/html")
        else:
            raise FileNotFoundError(
                f"Directory {wwwroot} missing. "
                "To put the html into github repo for webhosting, run "
                "`git clone git@github.com:oscovida/oscovida.github.io.git"
                "wwwroot` or similar"
            )


def get_country_list():
    d = oscovida.fetch_deaths()
    c = oscovida.fetch_cases()

    countries = d.index
    countries2 = c.index
    assert (countries2 == countries).all()

    # Here we should identify regions in countries, and process those.
    # Instead, as a quick hack to get started, we'll just take one country
    # and the current "get_country" method will sum over all regions of one
    # country if only the country name is given.

    return sorted(countries.drop_duplicates())


def generate_reports_countries(
    *, workers, kernel_name, wwwroot, force, disable_pbar, debug
):
    d = oscovida.fetch_deaths()
    c = oscovida.fetch_cases()

    countries = d.index
    countries2 = c.index
    assert (countries2 == countries).all()

    #  TODO: The get_x_list methods should be part of Reporter class
    countries = get_country_list()

    cre = ReportExecutor(
        Reporter=CountryReport,
        kernel_name=kernel_name,
        wwwroot=wwwroot,
        expiry_hours=2,
        attempts=3,
        workers=workers,
        force=force,
        disable_pbar=disable_pbar,
        debug=debug,
    )

    if debug:
        countries = countries[:10]

    cre.create_html_reports(countries)

    cre.create_markdown_index_page()


def get_germany_regions_list():
    data_germany = oscovida.fetch_data_germany()
    land_kreis = data_germany[["Bundesland", "Landkreis"]]
    ordered = land_kreis.sort_values(["Bundesland", "Landkreis"])
    return ordered.drop_duplicates().values.tolist()


def generate_reports_germany(
    *, workers, kernel_name, wwwroot, force, disable_pbar, debug
):
    _ = oscovida.fetch_data_germany()

    #  TODO: The get_x_list methods should be part of Reporter class
    germany_regions = get_germany_regions_list()

    # data cleaning: on 13 April, we had a Landkreis "LK Göttingen (alt)"
    # with only one data point. This causes plots to fail, because there
    # is nothing to plot, and then the legend() command failed.
    # We assume that the RKI labels unusual data with '(alt)', and remove those.

    alt_data_sets = ["(alt)" in r[1].lower() for r in germany_regions]
    if any(alt_data_sets):
        bad_datasets = list(compress(germany_regions, alt_data_sets))

        logging.warning(f"Removing datasets label with '(alt)': {bad_datasets}")

        for bd in bad_datasets:
            c, d, _ = oscovida.germany_get_region(landkreis=bd[1])
            logging.warning(
                f"\tremoved: {bd} : len(cases)={len(c)}, len(deaths)={len(d)}"
            )

        bad_indices = list(compress(range(len(alt_data_sets)), alt_data_sets))

        for i in sorted(bad_indices, reverse=True):
            del germany_regions[i]

    gre = ReportExecutor(
        Reporter=GermanyReport,
        kernel_name=kernel_name,
        wwwroot=wwwroot,
        expiry_hours=2,
        attempts=3,
        workers=workers,
        force=force,
        disable_pbar=disable_pbar,
        debug=debug,
    )

    if debug:
        germany_regions = germany_regions[:10]

    gre.create_html_reports(germany_regions)

    gre.create_markdown_index_page()


def generate_reports_usa(
    *, workers, kernel_name, wwwroot, force, disable_pbar, debug
):
    _ = oscovida.fetch_cases_US()
    _ = oscovida.fetch_deaths_US()

    #  TODO: The get_x_list methods should be part of Reporter class
    states = oscovida.get_US_region_list()

    usre = ReportExecutor(
        Reporter=USAReport,
        kernel_name=kernel_name,
        wwwroot=wwwroot,
        expiry_hours=2,
        attempts=3,
        workers=workers,
        force=force,
        disable_pbar=disable_pbar,
        debug=debug,
    )

    if debug:
        states = states[:10]

    usre.create_html_reports(states)

    usre.create_markdown_index_page()


def generate_reports_hungary(*, workers, kernel_name, wwwroot, force, disable_pbar, debug):
    _ = oscovida.fetch_data_hungary()

    #  TODO: The get_x_list methods should be part of Reporter class
    counties = oscovida.get_counties_hungary()

    hre = ReportExecutor(
        Reporter=HungaryReport,
        kernel_name=kernel_name,
        wwwroot=wwwroot,
        expiry_hours=2,
        attempts=3,
        workers=workers,
        force=force,
        disable_pbar=disable_pbar,
        debug=debug,
    )

    if debug:
        counties = counties[:10]

    hre.create_html_reports(counties)

    hre.create_markdown_index_page()

def generate_markdown_all_regions(
    *, workers, kernel_name, wwwroot, force, disable_pbar, debug
):
    arre = ReportExecutor(Reporter=AllRegions, wwwroot=wwwroot)

    arre.create_markdown_index_page()


def generate(*, region, workers, kernel_name, wwwroot, force, disable_pbar, debug):
    mapping = {
        "countries": generate_reports_countries,
        "germany": generate_reports_germany,
        "usa": generate_reports_usa,
        "hungary": generate_reports_hungary,
        "all-regions-md": generate_markdown_all_regions,
    }

    mapping[region](
        workers=workers,
        kernel_name=kernel_name,
        wwwroot=wwwroot,
        disable_pbar=disable_pbar,
        force=force,
        debug=debug,
    )


@click.command()
@click.option(
    "--regions",
    "-r",
    type=click.Choice(
        ALL_REGIONS,
        case_sensitive=False
    ),
    multiple=True,
    help="Region(s) to generate reports for.",
)
@click.option(
    "--workers",
    default="auto",
    help="Number of workers to use, `auto` uses nproc-2, set to 1 or False to "
         "use a single process.",
)
@click.option(
    "--wwwroot",
    default="./wwwroot",
    help="Root directory for www content."
)
@click.option(
    "--create-wwwroot",
    default=False,
    is_flag=True,
    help="Create wwwroot directory if it does not exist.",
)
@click.option(
    "--kernel-name",
    default="",
    help="Create wwwroot directory if it does not exist.",
)
@click.option(
    "--disable-pbar",
    default=False,
    is_flag=True,
    help="Disable progress bar, print logging output instead.",
)
@click.option(
    "--log-level",
    default="WARNING",
    type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]),
    help="Log level.",
)
@click.option("--log-file", default=None, help="Log file path.")
@click.option(
    "--force",
    default=False,
    is_flag=True,
    help="Force notebook re-execution even if recently executed.",
)
@click.option(
    "--debug",
    default=False,
    is_flag=True,
    help="Enable debug mode, only generates reports for the first 10 regions "
         "and sets the log level to `DEBUG`.",
)
def cli(
    *,
    workers,
    regions,
    kernel_name="",
    wwwroot="wwwroot",
    create_wwwroot=False,
    disable_pbar=False,
    log_level="WARNING",
    log_file=None,
    force=False,
    debug=False,
):
    """
    Command Line Interface used to batch-generate and execute Jupyter
    notebook reports for oscovida.
    """
    #  If log level is set to INFO and debug flag is on, leave it at INFO, DEBUG
    #  level can be wwaaayy too verbose and annoying (e.g. prints off the full
    #  contents of the HTML pages as they get saved)
    if debug and log_level != "INFO":
        log_level = "DEBUG"

    if log_level in ["INFO", "DEBUG"]:
        click.echo("Disabling progress bar due to log level verbosity")
        disable_pbar = True

    handlers = []
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    if disable_pbar:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        format="%(asctime)s %(threadName)s: %(message)s",
        level=log_level,
        handlers=handlers,
        datefmt="%H:%M:%S",
    )

    logging.info(f"Initial args: {locals()}")

    does_wwwroot_exist(wwwroot, create=create_wwwroot)

    #  Disable pandas scientific notation
    pandas.set_option("display.float_format", "{:.2f}".format)

    if workers == "auto":
        workers = max(1, os.cpu_count())
        workers = max(workers - 2, 1)
    elif workers =="max":
        workers = os.cpu_count()

    if workers:
        logging.info(f"Using {workers} processes")

    if "all" in regions:
        if len(regions) > 1:
            raise Exception("Cannot accept multiple regions if 'all' is passed")
        regions = ALL_REGIONS
        regions.remove("all")

    logging.info(f"Processed args: {locals()}")

    for region in regions:
        generate(
            region=region,
            workers=workers,
            kernel_name=kernel_name,
            wwwroot=wwwroot,
            disable_pbar=disable_pbar,
            force=force,
            debug=debug,
        )


if __name__ == "__main__":
    cli()
