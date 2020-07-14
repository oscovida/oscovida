import json
import os

import ipynb_py_convert
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.writers import FilesWriter

import oscovida


class BaseReport:
    def __init__(
        self,
        *,
        country,
        title,
        overview_function,
        overview_args,
        data_load_function,
        data_load_args,
        output_file,
        wwwroot,
        verbose=False,
    ):
        self.verbose = verbose
        self.country = country
        self.title = title

        self.overview_function = overview_function
        self.overview_args = overview_args

        self.data_load_function = data_load_function
        self.data_load_args = data_load_args

        self.output_file_name = self.sanitise(output_file) + ".ipynb"
        self.output_ipynb_path = os.path.join(wwwroot, "ipynb", self.output_file_name)
        self.output_html_path = os.path.join(
            wwwroot, "html", self.sanitise(output_file) + ".html"
        )

        self.metadata = oscovida.MetadataRegion(self.title)

        self.init_metadata()

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
            "OVERVIEW_FUNCTION": self.overview_function,
            "OVERVIEW_ARGS": self.overview_args,
            "DATA_LOAD_FUNCTION": self.data_load_function,
            "DATA_LOAD_ARGS": self.data_load_args,
        }

    def _init_metadata(self, meta):
        [self.metadata.__setitem__(k, v) for (k, v) in meta.items()]

    def init_metadata(self):
        raise NotImplementedError()

    def generate_notebook(self, template_file="./template-report.py"):
        with open(template_file, "r") as f:
            template_str = f.read()

        template_str = template_str.format_map(self.mapping)

        notebook = ipynb_py_convert.py2nb(template_str)

        with open(self.output_ipynb_path, "tw") as f:
            print(self.output_ipynb_path) if self.verbose else None
            json.dump(notebook, f, indent=2)

            print(f"Written file to {self.output_file_name}") if self.verbose else None
            self.metadata["ipynb-name"] = os.path.basename(self.output_ipynb_path)

    def generate_html(self, kernel_name=""):
        nb_executor = ExecutePreprocessor(kernel_name=kernel_name)
        nb_executor.allow_errors = True

        html_exporter = HTMLExporter()
        html_writer = FilesWriter()

        with open(self.output_ipynb_path) as f:
            nb = nbformat.read(f, as_version=4)
            nb = nb_executor.preprocess(nb)[0]
            body, resources = html_exporter.from_notebook_node(nb)
            #  HTML writer automatically adds .html to the end, so get rid of it
            html_writer.write(
                body, resources, self.output_html_path.replace(".html", "")
            )

            print(f"Written file to {self.output_html_path}") if self.verbose else None
            self.metadata["html-file"] = os.path.basename(self.output_html_path)
            self.metadata.mark_as_updated()

    def generate(self, kernel_name="", template_file="./template-report.py"):
        self.generate_notebook(template_file=template_file)
        self.generate_html(kernel_name=kernel_name)


class CountryReport(BaseReport):
    category = "countries"

    def __init__(self, country, wwwroot="wwwroot", verbose=False):
        self.check_country_is_known(country)

        super().__init__(
            country=country,
            title=country,
            overview_function="overview",
            overview_args=f'"{country}"',
            data_load_function="get_country_data",
            data_load_args=f'"{country}"',
            output_file=f"{country}",
            wwwroot=wwwroot,
            verbose=verbose,
        )

    @staticmethod
    def check_country_is_known(country):
        d = oscovida.fetch_deaths()
        assert (
            country in d.index
        ), f"{country} is unknown. Known countries are {sorted(d.index)}"

    def init_metadata(self):
        cases, deaths, region_label = oscovida.get_country_data(self.country)
        one_line_summary = f"{self.country}"

        self._init_metadata(
            meta={
                "source": "CSSE Johns Hopkins",
                "category": self.category,
                "max-deaths": int(deaths[-1]),
                "max-cases": int(cases[-1]),
                "region": str(None),
                "subregion": str(None),
                "one-line-summary": one_line_summary,  # used as title in table
                "cases-last-week": int(oscovida.get_cases_last_week(cases)),
            }
        )


class GermanyReport(BaseReport):
    category = "germany"

    def __init__(self, region, wwwroot="wwwroot", verbose=False):
        self.region = region[0]  #  Bundesland
        self.subregion = region[1]  #  Kreis

        self.germany_check_region_is_known(self.region)
        self.germany_check_subregion__is_known(self.subregion)

        super().__init__(
            country="Germany",
            title=f"Germany: {self.subregion} ({self.region})",
            overview_function="overview",
            overview_args=f'country="Germany", subregion="{self.subregion}"',
            data_load_function="germany_get_region",
            data_load_args=f'landkreis="{self.subregion}"',
            output_file=f"Germany-{self.region}-{self.subregion}",
            wwwroot=wwwroot,
            verbose=verbose,
        )

    def init_metadata(self):
        #  TODO: region_label unused, what was this for?
        cases, deaths, region_label = oscovida.get_country_data(
            "Germany", subregion=self.subregion
        )
        one_line_summary = f"Germany: {self.region} : {self.subregion}"

        self._init_metadata(
            meta={
                "source": "Robert Koch Institute",
                "category": self.category,
                "max-deaths": int(deaths[-1]),
                "max-cases": int(cases[-1]),
                "region": self.region,
                "subregion": self.subregion,
                "one-line-summary": one_line_summary,  # used as title in table
                "cases-last-week": int(oscovida.get_cases_last_week(cases)),
            }
        )

    @staticmethod
    def germany_check_region_is_known(region):
        d = oscovida.fetch_data_germany()
        assert region in list(
            d["Bundesland"].drop_duplicates()
        ), f"{region} is unknown."

    @staticmethod
    def germany_check_subregion__is_known(subregion):
        d = oscovida.fetch_data_germany()
        assert subregion in list(
            d["Landkreis"].drop_duplicates()
        ), f"{subregion} is unknown."


class USAReport(BaseReport):
    category = "us"

    def __init__(self, region, wwwroot="wwwroot", verbose=False):
        self.region = region

        super().__init__(
            country="USA",
            title=f"United States: {region}",
            overview_function="overview",
            overview_args=f'country="US", region="{region}"',
            data_load_function="get_country_data",
            data_load_args=f'"US", "{region}"',
            output_file=f"US-{region}",
            wwwroot=wwwroot,
            verbose=verbose,
        )

    def init_metadata(self):
        cases, deaths = oscovida.get_region_US(self.region)
        one_line_summary = f"US: {self.region}"

        self._init_metadata(
            meta={
                "source": "Johns Hopkins University CSSE",
                "category": self.category,
                "max-deaths": int(deaths[-1]),
                "max-cases": int(cases[-1]),
                "region": self.region,
                "subregion": str(None),
                "one-line-summary": one_line_summary,  # used as title in table
                "cases-last-week": int(oscovida.get_cases_last_week(cases)),
            }
        )


class HungaryReport(BaseReport):
    category = "hungary"

    def __init__(self, region, wwwroot="wwwroot", verbose=False):
        self.region = region

        super().__init__(
            country="Hungary",
            title=f"Hungary: {region}",
            overview_function="overview",
            overview_args=f'country="Hungary", region="{region}"',
            data_load_function="get_region_hungary",
            data_load_args=f'county="{region}"',
            output_file=f"Hungary-{region}",
            wwwroot=wwwroot,
            verbose=verbose,
        )

    @staticmethod
    def hungary_check_region_name_is_known(region):
        counties = oscovida.get_counties_hungary()
        assert region in counties, f"{region} is unknown. Known regions are {counties}"

    def init_metadata(self):
        cases, _, _ = oscovida.get_country_data("Hungary", region=self.region)

        self._init_metadata(
            meta={
                "source": "https://github.com/sanbrock/covid19",
                "category": self.category,
                "max-deaths": None,
                "max-cases": int(cases[-1]),
                "region": self.region,
                "subregion": str(None),
                "one-line-summary": f"Hungary: {self.region}",  # used as title in table
                "cases-last-week": int(oscovida.get_cases_last_week(cases)),
            }
        )


class AllRegions(BaseReport):
    category = "all-regions"

    def __init__(self):
        pass
