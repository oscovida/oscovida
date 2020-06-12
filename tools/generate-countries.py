
import datetime
import json
import os
import shutil
import sys
from multiprocessing import Pool, cpu_count

import ipynb_py_convert
import nbformat
import numpy as np
from coronavirus import MetadataRegion
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.writers import FilesWriter


class BaseReport:
    def __init__(self, country, title, overview_function, overview_args,
                 data_load_function, data_load_args, output_file, wwwroot):
        self.country = country
        self.title = title

        self.overview_function = overview_function
        self.overview_args = overview_args

        self.data_load_function = data_load_function
        self.data_load_args = data_load_args

        self.output_file_name = self.sanitise(output_file) + ".ipynb"
        self.output_ipynb_path = os.path.join(
            wwwroot, "ipynb", self.output_file_name)
        self.output_html_path = os.path.join(
            wwwroot, "html", self.output_file_name.replace(".ipynb", ".html"))

        self.create_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.metadata = MetadataRegion(self.title)

    @staticmethod
    def sanitise(name):
        """Given a country name as a string, sanitise it for use as URL and
        filename by getting rid of spaces and commas

        return cleaned string.

        (Leave umlauts for now)
        """
        s = name.replace(" ", "-")
        s = s.replace(",", "-")
        return s

    @property
    def get_binder_url(self):
        """Given a notebook name, compute the path"""
        base = "https://mybinder.org/v2/gh/oscovida/binder/master?filepath=ipynb/"
        return base + self.output_file_name.replace(" ", "%20")

    @property
    def mapping(self):
        return {
            "TITLE": self.title,
            "COUNTRY": self.country,
            "BINDER_URL": self.get_binder_url,
            "CREATION_DATE" : self.create_date,
            "OVERVIEW_FUNCTION": self.overview_function,
            "OVERVIEW_ARGS": self.overview_args,
            "DATA_LOAD_FUNCTION": self.data_load_function,
            "DATA_LOAD_ARGS": self.data_load_args
        }

    def _init_metadata(self, *, source, category, max_deaths, max_cases,
                         subregion, region, one_line_summary, cases_last_week):
        [
            self.metadata.__setitem__(k, v)
            for (k, v)
            in locals().items()
            if k != 'self'
        ]

    def generate_notebook(self, template_file="./template-report.py"):
        with open(template_file, 'r') as f:
            template_str = f.read()

        template_str = template_str.format_map(self.mapping)

        notebook = ipynb_py_convert.py2nb(template_str)

        with open(self.output_ipynb_path, 'tw') as f:
            print(self.output_ipynb_path)
            json.dump(notebook, f, indent=2)

            print(f"Written file to {self.output_file_name}")
            self.metadata['ipynb_name'] = self.output_ipynb_path

    def generate_html(self, kernel_name='python3'):
        nb_executor = ExecutePreprocessor(kernel_name=kernel_name)
        nb_executor.allow_errors = True

        html_exporter = HTMLExporter()
        html_writer = FilesWriter()

        with open(self.output_ipynb_path) as f:
            nb = nbformat.read(f, as_version=4)
            nb = nb_executor.preprocess(nb)[0]
            body, resources = html_exporter.from_notebook_node(nb)
            #  HTML writer automatically adds .html to the end, so get rid of it
            html_writer.write(body, resources,
                self.output_html_path.replace(".html", ""))

            print(f"Written file to {self.output_html_path}")
            self.metadata['html_file'] = self.output_html_path
            self.metadata.mark_as_updated()

    def generate(self, kernel_name='python3', template_file="./template-report.py"):
        self.generate_notebook(template_file=template_file)
        self.generate_html(kernel_name=kernel_name)


class Country(BaseReport):
    def __init__(self, country, wwwroot='wwwroot'):
        title = country
        overview_function = "overview"
        overview_args = f"\"{country}\""
        data_load_function = "get_country_data"
        data_load_args = f"\"{country}\""
        output_file = f"{country}"

        self.check_country_is_known(country)

        super().__init__(country, title, overview_function, overview_args,
                         data_load_function, data_load_args, output_file, wwwroot)

    @staticmethod
    def check_country_is_known(country):
        d = fetch_deaths()
        assert country in d.index, f"{country} is unknown. Known countries are {sorted(d.index)}"

    def init_metadata(self):
        cases, deaths, region_label = get_country_data(self.country)
        one_line_summary = f"{self.country}"

        self._init_metadata(
            source = "CSSE Johns Hopkins",
            category = "world",
            max_deaths = int(deaths[-1]),
            max_cases = int(cases[-1]),
            region = str(None),
            subregion = str(None),
            one_line_summary = one_line_summary,  # used as title in table
            cases_last_week = int(get_cases_last_week(cases)),
        )


class Germany(BaseReport):
    def __init__(self, region, subregion, wwwroot='wwwroot'):
        country = "Germany"
        title = f"{country}: {subregion} ({region})"
        overview_function = "overview"
        overview_args = f"country=\"{country}\", subregion=\"{subregion}\""
        data_load_function = "germany_get_region"
        data_load_args = f"landkreis=\"{subregion}\""
        output_file = f"Germany-{region}-{subregion}"

        self.region = region
        self.subregion = subregion

        self.germany_check_region_is_known(region)
        self.germany_check_subregion__is_known(subregion)

        super().__init__(country, title, overview_function, overview_args,
                         data_load_function, data_load_args, output_file, wwwroot)

    def init_metadata_(self):
        cases, deaths, region_label = get_country_data("Germany", subregion=self.subregion)
        one_line_summary = f"Germany: {self.region} : {self.subregion}"

        self._init_metadata(
            source = "Robert Koch Institute",
            category = "Germany",
            max_deaths = int(deaths[-1]),
            max_cases = int(cases[-1]),
            region = self.region,
            subregion = self.subregion,
            one_line_summary = one_line_summary,  # used as title in table
            cases_last_week = int(get_cases_last_week(cases)),
        )

    @staticmethod
    def germany_check_region_is_known(region):
        d = fetch_data_germany()
        assert region in list(d['Bundesland'].drop_duplicates()), \
            f"{region} is unknown."

    @staticmethod
    def germany_check_subregion__is_known(subregion):
        d = fetch_data_germany()
        assert subregion in list(d['Landkreis'].drop_duplicates()), \
            f"{subregion} is unknown."


class USA(BaseReport):
    def __init__(self, region, wwwroot='wwwroot'):
        country = "USA"
        title = f"United States: {region}"
        overview_function = "overview"
        overview_args = f"country=\"US\", region=\"{region}\")"
        data_load_function = "get_country_data"
        data_load_args = f"\"US\", \"{region}\""
        output_file = f"US-{region}"

        self.region = region

        super().__init__(country, title, overview_function, overview_args,
                         data_load_function, data_load_args, output_file, wwwroot)

    def init_metadata_(self):
        cases, deaths = get_region_US(self.region)
        one_line_summary = f"US: {self.region}"

        self._init_metadata(
            source = "Johns Hopkins University CSSE",
            category = "US",
            max_deaths = int(deaths[-1]),
            max_cases = int(cases[-1]),
            region = self.region,
            subregion = str(None),
            one_line_summary = one_line_summary,  # used as title in table
            cases_last_week = int(get_cases_last_week(cases)),
        )
