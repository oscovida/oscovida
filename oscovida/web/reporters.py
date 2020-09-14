import json
import logging
import os
import threading
from collections import namedtuple
from typing import List

import ipynb_py_convert
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.writers import FilesWriter
from tqdm.auto import tqdm

__STOP__ = threading.Event()


RegionREPR = namedtuple(
    'Region', ['admin_1', 'admin_2', 'admin_3', 'level'], defaults=[None, None, None]
)


def generate_notebook(
    mapping: dict,
    output_file: str,
    template_file="./template-report.py",
) -> str:
    with open(template_file, "r") as f:
        template_str = f.read()

    template_str = template_str.format_map(mapping)

    notebook = ipynb_py_convert.py2nb(template_str)

    logging.info(f"Written templated notebook to {output_file}")
    with open(output_file, "tw") as f:
        json.dump(notebook, f, indent=2)

    return output_file


def execute_notebook(output_file: str, input_file: str, kernel_name: str = ""):
    nb_executor = ExecutePreprocessor(kernel_name=kernel_name)
    nb_executor.allow_errors = True

    html_exporter = HTMLExporter()
    html_writer = FilesWriter()

    logging.info(f"Written templated notebook to {output_file}")
    with open(input_file) as f:
        nb = nbformat.read(f, as_version=4)
        nb = nb_executor.preprocess(nb)[0]
        body, resources = html_exporter.from_notebook_node(nb)
        #  HTML writer automatically adds .html to the end, so get rid of it
        #  from the output file name if it is specified
        html_writer.write(body, resources, output_file.replace(".html", ""))


def create_html_report(
    region: RegionREPR,
    output_file: str,
    template_file: str = "./template-report.py",
    attempts: int = 3,
    force: bool = False,
    kernel_name: str = "",
):
    mapping = {
        'TITLE': str(region),
        'BINDER_URL': None,
        'REGION_REPR': region.__repr__(),
    }

    if os.path.exists(output_file) and not force:
        raise FileExistsError

    for attempt in range(attempts):
        if __STOP__.is_set():
            raise KeyboardInterrupt

        logging.info(f"Processing {region} attempt {attempt}")
        try:
            nb_file = generate_notebook(mapping, output_file, template_file)
            execute_notebook(output_file, nb_file, kernel_name)
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
    regions: List[RegionREPR],
    template_file: str,
    output_file: str,
    attempts: int = 3,
    force: bool = False,
    kernel_name: str = "",
    disable_pbar: bool = False,
) -> None:
    if logging.getLogger(__name__).level <= logging.WARNING:
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

            create_html_report(region)

    except KeyboardInterrupt:
        logging.warning(f"stopped {KeyboardInterrupt}")
