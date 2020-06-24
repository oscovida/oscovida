import logging
from os import cpu_count

import click

from oscovida import *

from .executors import ReportExecutor
from .index import create_markdown_index_page
from .reporters import CountryReport, GermanyReport, USAReport


def does_wwwroot_exist(wwwroot, create=False):
    if not os.path.exists(wwwroot):
        msg = "To put the html into github repo for webhosting, run "
        msg += '"git clone git@github.com:oscovida/oscovida.github.io.git wwwroot" or similar'
        if create:
            os.mkdir(wwwroot)
            os.mkdir(wwwroot+"/ipynb")
            os.mkdir(wwwroot+"/html")
        else:
            raise ValueError(f"directory {wwwroot} missing.")


def get_country_list():
    d, c = fetch_deaths(), fetch_cases()

    countries = d.index
    countries2 = c.index
    assert (countries2 == countries).all()

    # Here we should identify regions in countries, and process those.
    # Instead, as a quick hack to get started, we'll just take one country
    # and the current "get_country" method will sum over all regions of one country if only
    # the country name is given.

    return sorted(countries.drop_duplicates())

def generate_reports_countries(*, workers, kernel_name, wwwroot, disable_pbar):
    d, c = fetch_deaths(), fetch_cases()

    countries = d.index
    countries2 = c.index
    assert (countries2 == countries).all()

    countries = get_country_list()

    cre = ReportExecutor(Reporter=CountryReport,
        wwwroot=wwwroot, expiry_hours=2, attempts=3, workers=workers, force=True,
        disable_pbar=disable_pbar)

    cre.create_html_reports(countries)

    create_markdown_index_page(cre)


def get_germany_regions_list():
    data_germany = fetch_data_germany()
    land_kreis = data_germany[['Bundesland', 'Landkreis']]
    ordered = land_kreis.sort_values(['Bundesland', 'Landkreis'])
    return ordered.drop_duplicates().values.tolist()

def generate_reports_germany(*, workers, kernel_name, wwwroot, disable_pbar):
    germany = fetch_data_germany()

    germany_regions = get_germany_regions_list()

    # data cleaning: on 13 April, we had a Landkreis "LK Göttingen (alt)"
    # with only one data point. This causes plots to fail, because there
    # is nothing to plot, and then the legend() command failed.
    # We assume that the RKI labels unusual data with '(alt)', and remove those.

    alt_data_sets = ["(alt)" in r[1].lower() for r in germany_regions]
    if sum(alt_data_sets) > 0:
        bad_datasests = list(compress(germany_regions, alt_data_sets))

        print(f"Removing datasets label with '(alt)': {bad_datasests}")

        for bd in bad_datasests:
            c, d, _ = germany_get_region(landkreis=bd[1])
            print(f"\tremoved: {bd} : len(cases)={len(c)}, len(deaths)={len(d)}")

        bad_indecies = list(compress(range(len(alt_data_sets)), alt_data_sets))

        [germany_regions.pop(i) for i in bad_indecies]

    gre = ReportExecutor(Reporter=GermanyReport, kernel_name=kernel_name,
        wwwroot=wwwroot, expiry_hours=2, attempts=3, workers=workers, force=True,
        disable_pbar=disable_pbar)

    gre.create_html_reports(germany_regions)

    create_markdown_index_page(gre)


def generate_reports_usa(*, workers, kernel_name, wwwroot, disable_pbar):
    data_US_cases = fetch_cases_US()
    data_US_deaths = fetch_deaths_US()

    states = get_US_region_list()

    usre = ReportExecutor(Reporter=USAReport,
        wwwroot=wwwroot, expiry_hours=2, attempts=3, workers=workers, force=True,
        disable_pbar=disable_pbar)

    usre.create_html_reports(states)

    create_markdown_index_page(usre)


def generate(*, region, workers, kernel_name, wwwroot, disable_pbar):
    mapping = {
        'countries': generate_reports_countries,
        'germany': generate_reports_germany,
        'usa': generate_reports_usa,
    }

    mapping[region](
        workers=workers, kernel_name=kernel_name, wwwroot=wwwroot,
        disable_pbar=disable_pbar
    )


@click.command()
@click.option(
    '--regions', '-r',
    type=click.Choice(['countries', 'germany', 'usa'], case_sensitive=False),
    multiple=True,
    help='Region(s) to generate reports for.'
)
@click.option(
    '--workers', default='auto',
    help="Number of workers to use, 'auto' uses nproc-2, set to 1 or False to "
         "use a single process."
)
@click.option(
    '--wwwroot', default='./wwwroot',
    help='Root directory for www content.'
)
@click.option(
    '--create-wwwroot', default=False,
    is_flag=True,
    help='Create wwwroot directory if it does not exist.'
)
@click.option(
    '--kernel-name', default='',
    help='Create wwwroot directory if it does not exist.'
)
@click.option(
    '--disable-pbar', default=False,
    is_flag=True,
    help='Disable progress bar, print logging output instead.'
)
@click.option(
    '--log-level', default='WARNING',
    type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']),
    help='Log level.'
)
@click.option(
    '--log-file', default=None,
    help='Log file.'
)
def cli(*,
    workers, regions,
    kernel_name='', wwwroot="wwwroot", create_wwwroot=False,
    disable_pbar=False, log_level=logging.WARNING, log_file=None,
):
    click.echo(locals())

    handlers = []
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    if disable_pbar:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        format="%(asctime)s %(threadName)s: %(message)s",
        level=log_level,
        handlers=handlers,
        datefmt="%H:%M:%S"
    )

    does_wwwroot_exist(wwwroot, create=create_wwwroot)

    #  Disable pandas scientific notation
    pd.set_option('display.float_format', '{:.2f}'.format)

    if workers == 'auto':
        workers = max(1, cpu_count())
        # try at most 4 to reduce probability of error message like
        # the one shown at https://github.com/jupyter/jupyter_client/issues/541
        workers = max(workers-2, 1)

    if workers:
        print(f'Using {workers} processes')

    for region in regions:
        generate(
            region=region,
            workers=workers,
            kernel_name=kernel_name,
            wwwroot=wwwroot,
            disable_pbar=disable_pbar,
        )

if __name__ == '__main__':
    cli()
