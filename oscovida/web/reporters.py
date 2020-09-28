import json
import logging
import os
import threading
from typing import List

import ipynb_py_convert
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.writers import FilesWriter
from tqdm.auto import tqdm

from ..covid19dh import get
from ..regions import Region

__STOP__ = threading.Event()


def all_countries():
    countries = []

    for country in Region(country=None).data['iso_alpha_3'].unique():
        try:
            countries.append(Region(country, level=1, lazy=True))
        except LookupError:
            logging.warn(f"Skipped {country}")
            pass

    return countries


ALL_COUNTRIES = all_countries()


def generate_notebook(
    mapping: dict,
    output_file_path: str,
    template_file_path="./template-report.py",
) -> str:
    with open(template_file_path, "r") as f:
        template_str = f.read()

    template_str = template_str.format_map(mapping)

    notebook = ipynb_py_convert.py2nb(template_str)

    logging.info(f"Written templated notebook to {output_file_path}")
    with open(output_file_path, "tw") as f:
        json.dump(notebook, f, indent=2)

    return output_file_path


def execute_notebook(
    output_file_path: str, input_file_path: str, kernel_name: str = ""
):
    nb_executor = ExecutePreprocessor(kernel_name=kernel_name)
    nb_executor.allow_errors = True

    html_exporter = HTMLExporter()
    html_writer = FilesWriter()

    logging.info(f"Written templated notebook to {output_file_path}")
    with open(input_file_path) as f:
        nb = nbformat.read(f, as_version=4)
        nb = nb_executor.preprocess(nb)[0]
        body, resources = html_exporter.from_notebook_node(nb)
        #  HTML writer automatically adds .html to the end, so get rid of it
        #  from the output file name if it is specified
        html_writer.write(body, resources, output_file_path.replace(".html", ""))


def create_html_report(
    region: Region,
    output_file_path: str,
    template_file_path: str = "./template-report.py",
    attempts: int = 3,
    force: bool = False,
    kernel_name: str = "",
):
    mapping = {
        'TITLE': str(region),
        'BINDER_URL': None,
        'REGION_REPR': region.__repr__(),
    }

    output_file_path_html = output_file_path + ".html"
    output_file_path_ipynb = output_file_path + ".ipynb"

    if (
        os.path.exists(output_file_path_html) or os.path.exists(output_file_path_ipynb)
    ) and not force:
        raise FileExistsError

    for attempt in range(attempts):
        if __STOP__.is_set():
            raise KeyboardInterrupt

        logging.info(f"Processing {region} attempt {attempt}")
        try:
            nb_file = generate_notebook(
                mapping, output_file_path_ipynb, template_file_path
            )
            execute_notebook(output_file_path_html, nb_file, kernel_name)
            break  #  Without this break if force is on it will keep attempting
        except Exception as e:
            if e == KeyboardInterrupt:
                raise e

            if attempt + 1 == attempts:
                logging.warning(f"Processing {region} error\n{e}")
                raise e

            logging.warning(
                f"Processing {region} error {type(e)}, retrying {attempt+1}"
            )


def create_html_reports_serial(
    regions: List[Region],
    output_file_dir: str,
    template_file_path: str = "./template-report.py",
    attempts: int = 3,
    force: bool = False,
    kernel_name: str = "",
    disable_pbar: bool = False,
) -> None:
    if logging.getLogger().level < logging.WARNING:
        logging.info("Disabled pbar due to logging level")
        disable_pbar = True

    #  If logging is set to debug or above then disable the progress bar, to
    #  easiest way to do this is to use a normal range instead of the tqdm bar
    #  object
    if disable_pbar:
        pbar = range(len(regions))
    else:
        pbar = tqdm(range(len(regions)))

    try:
        for i in pbar:
            region = regions[i]

            if disable_pbar:
                logging.info(f"Processing {str(region)}")
            else:
                pbar.set_description(f"Processing {str(region)}")

            html_path = region._path(output_file_dir)

            create_html_report(
                region,
                html_path,
                template_file_path,
                attempts,
                force,
                kernel_name,
            )

    except KeyboardInterrupt:
        logging.warning(f"stopped {KeyboardInterrupt}")
